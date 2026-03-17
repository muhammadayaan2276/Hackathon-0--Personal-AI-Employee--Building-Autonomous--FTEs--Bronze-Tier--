"""
Orchestrator Module

Main orchestration script for the AI Employee system.
Monitors the vault for items needing action and triggers Claude Code processing.

For Bronze Tier: Processes files in /Needs_Action and updates Dashboard.md
"""

import sys
import subprocess
import logging
import hashlib
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Set
import re


class Orchestrator:
    """
    Main orchestrator for the AI Employee system.
    
    Responsibilities:
    - Monitor /Needs_Action folder for new items
    - Trigger Claude Code processing
    - Update Dashboard.md with current stats
    - Manage task lifecycle (pending -> in_progress -> done)
    """
    
    def __init__(self, vault_path: str, check_interval: int = 30):
        """
        Initialize the orchestrator.

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 30)
        """
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        
        # Folder paths (Bronze Tier: Only 3 folders)
        self.inbox = self.vault_path / 'Inbox'
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'

        # Ensure directories exist
        for folder in [self.inbox, self.needs_action, self.done, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Track processed files
        self.processed_files: set = set()
    
    def _setup_logging(self):
        """Setup logging to file and console."""
        log_file = self.logs / f'orchestrator_{datetime.now().strftime("%Y-%m-%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('Orchestrator')
    
    def count_files(self, folder: Path) -> int:
        """Count .md files in a folder."""
        if not folder.exists():
            return 0
        return len(list(folder.glob('*.md')))
    
    def get_pending_items(self) -> List[Path]:
        """Get list of pending items in Needs_Action folder."""
        if not self.needs_action.exists():
            return []
        
        items = []
        for filepath in self.needs_action.glob('*.md'):
            if filepath not in self.processed_files:
                items.append(filepath)

        return sorted(items, key=lambda x: x.stat().st_mtime)

    # Note: get_approved_items() removed - not used in Bronze Tier

    def update_dashboard(self):
        """Update the Dashboard.md with current statistics."""
        if not self.dashboard.exists():
            self.logger.warning('Dashboard.md not found, creating...')
            self._create_default_dashboard()
            return

        try:
            content = self.dashboard.read_text(encoding='utf-8')
            
            # Count items in each folder
            pending_count = self.count_files(self.needs_action)
            in_progress_count = 0  # Not used in Bronze Tier
            approval_count = 0  # Not used in Bronze Tier
            done_today = self._count_files_modified_today(self.done)
            done_week = self._count_files_modified_this_week(self.done)
            inbox_count = self.count_files(self.inbox)

            # Update stats section
            content = self._update_table_row(content, '**Pending Actions**', str(pending_count))
            content = self._update_table_row(content, '**In Progress**', str(in_progress_count))
            content = self._update_table_row(content, '**Awaiting Approval**', str(approval_count))
            content = self._update_table_row(content, '**Completed Today**', str(done_today))
            content = self._update_table_row(content, '**Completed This Week**', str(done_week))

            # Update folder status table
            content = re.sub(r'(\| `/Inbox` \|) \d+ (\|)', rf'\1 {inbox_count} \2', content)
            content = re.sub(r'(\| `/Needs_Action` \|) \d+ (\|)', rf'\1 {pending_count} \2', content)
            content = re.sub(r'(\| `/Done` \|) \d+ (\|)', rf'\1 {self.count_files(self.done)} \2', content)

            # Update last_updated timestamp
            content = re.sub(
                r'last_updated:.*',
                f'last_updated: {datetime.now().isoformat()}',
                content
            )

            # Write updated content
            self.dashboard.write_text(content, encoding='utf-8')
            self.logger.info('Dashboard updated')

        except Exception as e:
            self.logger.error(f'Error updating dashboard: {e}')
    
    def _update_table_row(self, content: str, metric_name: str, value: str) -> str:
        """Update a specific row in a markdown table."""
        lines = content.split('\n')
        new_lines = []
        
        for i, line in enumerate(lines):
            if f'| **{metric_name}**' in line or f'| {metric_name}' in line:
                # Keep the same table structure, update the value
                parts = line.split('|')
                if len(parts) >= 3:
                    # Reconstruct the line with new value
                    new_line = f'{parts[0]}| {parts[1].strip()} | {value} |{parts[3] if len(parts) > 3 else ""}'
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def _update_folder_status(self, content: str, folder_name: str, count: int) -> str:
        """Update folder status in dashboard."""
        # Simple replacement for folder counts
        pattern = rf'(\| `{folder_name}` \|) \d+ (\|)'
        replacement = rf'\1 {count} \2'
        return re.sub(pattern, replacement, content)
    
    def _count_files_modified_today(self, folder: Path) -> int:
        """Count files modified today."""
        if not folder.exists():
            return 0
        
        today = datetime.now().date()
        count = 0
        for filepath in folder.glob('*.md'):
            if datetime.fromtimestamp(filepath.stat().st_mtime).date() == today:
                count += 1
        return count
    
    def _count_files_modified_this_week(self, folder: Path) -> int:
        """Count files modified this week."""
        if not folder.exists():
            return 0
        
        from datetime import timedelta
        week_ago = datetime.now() - timedelta(days=7)
        count = 0
        for filepath in folder.glob('*.md'):
            if datetime.fromtimestamp(filepath.stat().st_mtime) >= week_ago:
                count += 1
        return count
    
    def _create_default_dashboard(self):
        """Create a default dashboard if none exists."""
        dashboard_content = '''---
last_updated: 2026-03-16T00:00:00Z
version: 0.1-bronze
---

# 📊 Personal AI Employee Dashboard

> **Status:** 🟢 Operational | **Tier:** Bronze

---

## 🎯 Quick Stats

| Metric | Value | Trend |
|--------|-------|-------|
| **Pending Actions** | 0 | ➖ |
| **In Progress** | 0 | ➖ |
| **Awaiting Approval** | 0 | ➖ |
| **Completed Today** | 0 | ➖ |
| **Completed This Week** | 0 | ➖ |

---

## 📥 Inbox Status

| Folder | Count | Last Activity |
|--------|-------|---------------|
| `/Inbox` | 0 | - |
| `/Needs_Action` | 0 | - |
| `/Pending_Approval` | 0 | - |

---

## 💰 Financial Summary

### Current Month (March 2026)

| Metric | Amount |
|--------|--------|
| **Revenue MTD** | $0 |
| **Expenses MTD** | $0 |
| **Net** | $0 |

---

## 📋 Active Projects

| Project | Status | Due Date | Progress |
|---------|--------|----------|----------|
| *No active projects* | - | - | - |

---

*Last generated: 2026-03-16*
*AI Employee v0.1 (Bronze Tier)*
'''
        self.dashboard.write_text(dashboard_content)
    
    def process_pending_items(self):
        """Process items in Needs_Action folder and move through workflow."""
        # First: Move files from Inbox to Needs_Action (automatic)
        self._process_inbox_files()
        
        # Second: Process Needs_Action items
        pending_items = self.get_pending_items()

        if not pending_items:
            self.logger.debug('No pending items to process')
            return

        self.logger.info(f'Found {len(pending_items)} pending item(s)')

        for item in pending_items:
            try:
                self._process_single_item(item)
            except Exception as e:
                self.logger.error(f'Error processing {item.name}: {e}')
    
    def _process_inbox_files(self):
        """
        Automatically move files from Inbox to Needs_Action.
        Tracks processed files to avoid duplicates.
        """
        if not self.inbox.exists():
            return
        
        # Load processed files cache
        processed_cache = self._load_processed_cache()
        
        for filepath in self.inbox.glob('*.md'):
            try:
                # Calculate file hash
                content = filepath.read_text(encoding='utf-8')
                file_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
                
                # Check if already processed (has original_hash or in cache)
                if 'original_hash:' in content:
                    self.logger.debug(f'File already processed: {filepath.name}')
                    continue
                
                # Check cache
                if file_hash in processed_cache:
                    self.logger.debug(f'File already processed (cached): {filepath.name}')
                    continue
                
                # Create action file in Needs_Action
                self._create_action_file(filepath, file_hash)
                
                # Add to cache
                processed_cache.add(file_hash)
                self._save_processed_cache(processed_cache)
                
                self.logger.info(f'Moved {filepath.name} from Inbox to Needs_Action')
            except Exception as e:
                self.logger.error(f'Error processing inbox file {filepath.name}: {e}')
    
    def _load_processed_cache(self) -> set:
        """Load processed file hashes from cache."""
        cache_file = self.vault_path / '.processed_cache.txt'
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return set(line.strip() for line in f)
        return set()
    
    def _save_processed_cache(self, cache: set):
        """Save processed file hashes to cache."""
        cache_file = self.vault_path / '.processed_cache.txt'
        with open(cache_file, 'w') as f:
            for file_hash in cache:
                f.write(f'{file_hash}\n')
    
    def _create_action_file(self, source_file: Path, file_hash: str):
        """
        Create an action file in Needs_Action from an inbox file.
        """
        import shutil
        
        # Read file content
        content = source_file.read_text(encoding='utf-8')
        stat = source_file.stat()
        
        # Create action file content
        from datetime import datetime
        action_content = f'''---
type: inbox_item
original_name: {source_file.name}
original_hash: {file_hash}
size_bytes: {stat.st_size}
created: {datetime.fromtimestamp(stat.st_ctime).isoformat()}
received: {datetime.now().isoformat()}
status: pending
priority: medium
---

## Inbox Item for Processing

**Original File:** `{source_file.name}`
**Size:** {self._format_size(stat.st_size)}
**Received:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## File Content

```
{content[:2000]}
```

---

## Suggested Actions

- [ ] Review content
- [ ] Categorize item type
- [ ] Take appropriate action
- [ ] Mark as complete

---

## Processing Notes

*Add notes here during processing*

'''
        
        # Create action file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        action_filename = f'INBOX_{file_hash}_{timestamp}.md'
        action_filepath = self.needs_action / action_filename
        action_filepath.write_text(action_content, encoding='utf-8')
        
        # Copy original file to Files folder
        files_folder = self.vault_path / 'Files'
        files_folder.mkdir(parents=True, exist_ok=True)
        dest_path = files_folder / f'{file_hash}_{source_file.name}'
        shutil.copy2(source_file, dest_path)
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f'{size_bytes:.1f} {unit}'
            size_bytes /= 1024
        return f'{size_bytes:.1f} TB'
    
    def _process_single_item(self, item: Path):
        """
        Process a single item.
        
        For Bronze Tier: This would trigger Claude Code to read and process the file.
        In a full implementation, this would invoke Claude via CLI.
        """
        self.logger.info(f'Processing: {item.name}')
        
        # Read the file to understand its type
        content = item.read_text()
        
        # Extract type from frontmatter if present
        item_type = self._extract_frontmatter_value(content, 'type')
        status = self._extract_frontmatter_value(content, 'status')
        
        self.logger.info(f'Item type: {item_type}, status: {status}')
        
        # For Bronze Tier: Log the processing
        # In Silver/Gold tiers, this would invoke Claude Code
        self._log_action('process', item.name, item_type)
        
        # Mark as processed
        self.processed_files.add(item)
        
        self.logger.info(f'Completed processing: {item.name}')
    
    def _extract_frontmatter_value(self, content: str, key: str) -> str:
        """Extract a value from YAML frontmatter."""
        match = re.search(rf'^{key}:\s*(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return 'unknown'
    
    def _log_action(self, action_type: str, target: str, item_type: str):
        """Log an action to the logs folder."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'actor': 'orchestrator',
            'target': target,
            'item_type': item_type,
            'result': 'success'
        }
        
        log_file = self.logs / f'actions_{datetime.now().strftime("%Y-%m-%d")}.json'
        
        # Append to log file
        import json
        if log_file.exists():
            logs = json.loads(log_file.read_text())
        else:
            logs = []
        
        logs.append(log_entry)
        log_file.write_text(json.dumps(logs, indent=2))
    
    def run(self):
        """Main run loop for the orchestrator."""
        # Print welcome banner
        print('')
        print('╔═══════════════════════════════════════════════════════════╗')
        print('║                                                           ║')
        print('║   🥉 BRONZE TIER - PERSONAL AI EMPLOYEE                  ║')
        print('║                                                           ║')
        print('║   ✅ Orchestrator Started Successfully!                  ║')
        print('║                                                           ║')
        print('║   ⏱️  Auto-update: Every 30 seconds                      ║')
        print('║                                                           ║')
        print('╚═══════════════════════════════════════════════════════════╝')
        print('')
        
        self.logger.info('Starting Orchestrator')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval} seconds')
        
        # Initial dashboard update
        self.update_dashboard()
        
        try:
            while True:
                try:
                    # Update dashboard
                    self.update_dashboard()

                    # Process pending items
                    self.process_pending_items()

                except Exception as e:
                    self.logger.error(f'Error in orchestration loop: {e}')
                
                import time
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('Orchestrator stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}')
            raise
    
    def run_once(self):
        """Run a single orchestration cycle (useful for testing)."""
        self.logger.info('Running single orchestration cycle')
        self.update_dashboard()
        self.process_pending_items()


def main():
    """Main entry point for the orchestrator."""
    if len(sys.argv) < 2:
        print('Usage: python orchestrator.py <vault_path> [check_interval]')
        print('')
        print('Arguments:')
        print('  vault_path       Path to the Obsidian vault')
        print('  check_interval   Seconds between checks (default: 30)')
        print('')
        print('Options:')
        print('  --run-once       Run a single cycle and exit')
        print('')
        print('Example:')
        print('  python orchestrator.py "C:/Users/pc/Desktop/AI_Employee_Vault"')
        print('  python orchestrator.py "C:/Users/pc/Desktop/AI_Employee_Vault" --run-once')
        print('  python orchestrator.py "C:/Users/pc/Desktop/AI_Employee_Vault" 30')
        sys.exit(1)

    vault_path = sys.argv[1]

    # Parse optional arguments
    check_interval = 30
    run_once = False

    for arg in sys.argv[2:]:
        if arg == '--run-once':
            run_once = True
        elif arg.isdigit():
            check_interval = int(arg)
    
    # Validate vault path
    if not Path(vault_path).exists():
        print(f'Error: Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    # Create and run orchestrator
    orchestrator = Orchestrator(vault_path, check_interval)
    
    if run_once:
        orchestrator.run_once()
    else:
        orchestrator.run()


if __name__ == '__main__':
    main()
