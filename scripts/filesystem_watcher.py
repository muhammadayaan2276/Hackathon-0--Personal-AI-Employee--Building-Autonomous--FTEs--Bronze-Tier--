"""
File System Watcher Module

Monitors a drop folder for new files and creates action files in the Obsidian vault.
This is the Bronze Tier watcher - simple, reliable, and doesn't require API credentials.

Usage:
    python filesystem_watcher.py /path/to/vault /path/to/drop_folder
"""

import sys
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from base_watcher import BaseWatcher


class FileDropHandler(FileSystemEventHandler):
    """Handle file system events for the drop folder."""
    
    def __init__(self, watcher: 'FileSystemWatcher'):
        self.watcher = watcher
        self.logger = watcher.logger
    
    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
        
        try:
            self.watcher.process_new_file(Path(event.src_path))
        except Exception as e:
            self.logger.error(f'Error processing file {event.src_path}: {e}')


class FileSystemWatcher(BaseWatcher):
    """
    Watcher that monitors a drop folder for new files.
    
    When a file is added to the drop folder, creates an action file
    in the Needs_Action folder for Claude Code to process.
    """
    
    def __init__(self, vault_path: str, drop_folder: Optional[str] = None, check_interval: int = 30):
        """
        Initialize the file system watcher.
        
        Args:
            vault_path: Path to the Obsidian vault
            drop_folder: Path to the drop folder (default: vault/Inbox)
            check_interval: Seconds between checks (default: 30)
        """
        super().__init__(vault_path, check_interval)
        
        # Setup drop folder - Using Inbox for live visibility
        if drop_folder:
            self.drop_folder = Path(drop_folder)
        else:
            self.drop_folder = self.vault_path / 'Inbox'
        
        self.drop_folder.mkdir(parents=True, exist_ok=True)
        
        # Track processed files by hash
        self.processed_files: Dict[str, str] = {}  # hash -> filename
        self._load_processed_files()
    
    def _load_processed_files(self):
        """Load list of already processed files from the vault."""
        # Scan existing action files to find already processed files
        for action_file in self.needs_action.glob('FILE_*.md'):
            content = action_file.read_text()
            if 'original_hash:' in content:
                for line in content.split('\n'):
                    if line.startswith('original_hash:'):
                        file_hash = line.split(':')[1].strip()
                        self.processed_files[file_hash] = action_file.name
                        break
        
        self.logger.info(f'Loaded {len(self.processed_files)} previously processed files')
    
    def _calculate_hash(self, filepath: Path) -> str:
        """Calculate SHA256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def check_for_updates(self) -> List[Path]:
        """
        Check drop folder for new files.
        
        Returns:
            List of new file paths to process
        """
        new_files = []
        
        if not self.drop_folder.exists():
            return new_files
        
        # Check all files in drop folder
        for filepath in self.drop_folder.iterdir():
            if filepath.is_file():
                file_hash = self._calculate_hash(filepath)
                
                # Skip if already processed
                if file_hash in self.processed_files:
                    self.logger.debug(f'File already processed: {filepath.name}')
                    continue
                
                new_files.append(filepath)
        
        return new_files
    
    def process_new_file(self, filepath: Path):
        """
        Process a newly detected file.
        
        Args:
            filepath: Path to the new file
        """
        self.create_action_file(filepath)
    
    def create_action_file(self, filepath: Path) -> Optional[Path]:
        """
        Create an action file for the dropped file.
        
        Args:
            filepath: Path to the dropped file
            
        Returns:
            Path to created action file
        """
        try:
            # Calculate file hash
            file_hash = self._calculate_hash(filepath)
            
            # Get file metadata
            stat = filepath.stat()
            file_size = stat.st_size
            created_time = datetime.fromtimestamp(stat.st_ctime).isoformat()
            modified_time = datetime.fromtimestamp(stat.st_mtime).isoformat()
            
            # Generate unique ID from first 8 chars of hash
            unique_id = file_hash[:8]
            
            # Create action file content
            content = self.create_yaml_frontmatter({
                'type': 'file_drop',
                'original_name': filepath.name,
                'original_hash': file_hash,
                'size_bytes': file_size,
                'created': created_time,
                'received': datetime.now().isoformat(),
                'status': 'pending',
                'priority': 'medium'
            })
            
            content += f'''## File Drop for Processing

**Original File:** `{filepath.name}`
**Size:** {self._format_size(file_size)}
**Received:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## File Content Preview

'''
            
            # Add file content preview if it's a text file
            if self._is_text_file(filepath):
                try:
                    preview = filepath.read_text()[:2000]  # First 2000 chars
                    content += f'''```
{preview}
```
'''
                except Exception as e:
                    content += f'*Could not preview file: {e}*\n'
            else:
                content += '*Binary file - cannot preview content*\n'
            
            content += f'''
---

## Suggested Actions

- [ ] Review file content
- [ ] Categorize file type
- [ ] Take appropriate action
- [ ] Move original file to appropriate location
- [ ] Mark as complete

---

## Processing Notes

*Add notes here during processing*

'''
            
            # Create action file
            filename = self.generate_filename('FILE', unique_id)
            action_filepath = self.needs_action / filename
            action_filepath.write_text(content)
            
            # Copy original file to vault for safekeeping
            files_folder = self.vault_path / 'Files'
            files_folder.mkdir(parents=True, exist_ok=True)
            dest_path = files_folder / f'{unique_id}_{filepath.name}'
            shutil.copy2(filepath, dest_path)
            
            # Mark as processed
            self.processed_files[file_hash] = filename
            self._save_processed_files()
            
            self.logger.info(f'Created action file for: {filepath.name}')
            
            return action_filepath
            
        except Exception as e:
            self.logger.error(f'Error creating action file for {filepath.name}: {e}')
            return None
    
    def _is_text_file(self, filepath: Path) -> bool:
        """Check if file is likely a text file."""
        text_extensions = {'.txt', '.md', '.py', '.js', '.json', '.yaml', '.yml', 
                          '.csv', '.xml', '.html', '.css', '.log', '.ini', '.cfg'}
        return filepath.suffix.lower() in text_extensions
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f'{size_bytes:.1f} {unit}'
            size_bytes /= 1024
        return f'{size_bytes:.1f} TB'
    
    def _save_processed_files(self):
        """Save list of processed files to disk."""
        cache_file = self.vault_path / '.processed_files.cache'
        with open(cache_file, 'w') as f:
            for file_hash, filename in self.processed_files.items():
                f.write(f'{file_hash}:{filename}\n')
    
    def run_with_observer(self):
        """
        Run the watcher using watchdog observer (real-time).
        This is more efficient than polling.
        """
        # Print welcome banner
        print('')
        print('╔═══════════════════════════════════════════════════════════╗')
        print('║                                                           ║')
        print('║   🥉 BRONZE TIER - PERSONAL AI EMPLOYEE                  ║')
        print('║                                                           ║')
        print('║   ✅ File System Watcher Started Successfully!           ║')
        print('║                                                           ║')
        print('╚═══════════════════════════════════════════════════════════╝')
        print('')
        
        self.logger.info(f'Starting {self.__class__.__name__} with real-time monitoring')
        self.logger.info(f'Inbox folder: {self.drop_folder}')
        
        event_handler = FileDropHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.drop_folder), recursive=False)
        observer.start()
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            observer.stop()
            self.logger.info(f'{self.__class__.__name__} stopped by user')
        observer.join()


def main():
    """Main entry point for the file system watcher."""
    if len(sys.argv) < 2:
        print('Usage: python filesystem_watcher.py <vault_path> [inbox_folder]')
        print('')
        print('Arguments:')
        print('  vault_path   Path to the Obsidian vault')
        print('  inbox_folder  Path to the inbox folder (optional, defaults to vault/Inbox)')
        print('')
        print('Example:')
        print('  python filesystem_watcher.py "C:/Users/pc/Desktop/AI_Employee_Vault"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    drop_folder = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Validate vault path
    if not Path(vault_path).exists():
        print(f'Error: Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    # Create and run watcher
    watcher = FileSystemWatcher(vault_path, drop_folder)
    
    # Use real-time observer for better performance
    watcher.run_with_observer()


if __name__ == '__main__':
    main()
