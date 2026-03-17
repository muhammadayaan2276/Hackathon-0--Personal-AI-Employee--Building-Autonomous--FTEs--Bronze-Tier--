# Personal AI Employee - Bronze Tier

> **Tagline:** *Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*

This is a **Bronze Tier** implementation of a Personal AI Employee - an autonomous AI agent that manages personal and business affairs 24/7 using **Claude Code** as the reasoning engine and **Obsidian** as the management dashboard.

## 🏆 Bronze Tier Deliverables

- [x] Obsidian vault with `Dashboard.md` and `Company_Handbook.md`
- [x] One working Watcher script (File System Watcher)
- [x] Claude Code integration for reading/writing to the vault
- [x] Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`
- [x] Orchestrator for processing pending items

## 📁 Project Structure

```
Hackathon-0--Personal-AI-Employee/
├── AI_Employee_Vault/          # Obsidian vault (your AI's memory)
│   ├── Inbox/                  # Raw incoming items
│   ├── Needs_Action/           # Items requiring processing
│   ├── Done/                   # Completed tasks
│   ├── Plans/                  # Generated plans
│   ├── Pending_Approval/       # Awaiting human approval
│   ├── Approved/               # Approved actions
│   ├── Rejected/               # Rejected actions
│   ├── Accounting/             # Financial records
│   ├── Briefings/              # CEO briefings
│   ├── Dashboard.md            # Real-time summary
│   ├── Company_Handbook.md     # Rules of engagement
│   └── Business_Goals.md       # Objectives and targets
├── scripts/
│   ├── base_watcher.py         # Base class for all watchers
│   ├── filesystem_watcher.py   # File system monitor (Bronze Tier)
│   └── orchestrator.py         # Main orchestration script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:

| Software | Version | Purpose |
|----------|---------|---------|
| [Python](https://www.python.org/downloads/) | 3.13+ | Watcher scripts |
| [Obsidian](https://obsidian.md/download) | v1.10.6+ | Knowledge base |
| [Claude Code](https://claude.com/product/claude-code) | Latest | AI reasoning engine |
| [Node.js](https://nodejs.org/) | v24+ | MCP servers (future tiers) |

### Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Open the vault in Obsidian:**
   - Launch Obsidian
   - Click "Open folder as vault"
   - Select the `AI_Employee_Vault` folder

4. **Verify Claude Code installation:**
   ```bash
   claude --version
   ```

### Running the System

#### 1. Start the File System Watcher

The File System Watcher monitors a drop folder for new files:

```bash
# Basic usage (uses vault/Drop_Folder as default)
python scripts/filesystem_watcher.py "C:\path\to\AI_Employee_Vault"

# With custom drop folder
python scripts/filesystem_watcher.py "C:\path\to\AI_Employee_Vault" "C:\path\to\Drop_Folder"
```

**How it works:**
- Drop any file into the `Drop_Folder` (or your custom folder)
- The watcher detects the new file
- An action file is created in `/Needs_Action`
- The original file is copied to `/Files` for safekeeping

#### 2. Start the Orchestrator

The Orchestrator processes items in `/Needs_Action`:

```bash
# Continuous monitoring (checks every 60 seconds)
python scripts/orchestrator.py "C:\path\to\AI_Employee_Vault"

# Single cycle (useful for testing)
python scripts/orchestrator.py "C:\path\to\AI_Employee_Vault" --run-once

# Custom check interval (30 seconds)
python scripts/orchestrator.py "C:\path\to\AI_Employee_Vault" 30
```

#### 3. Process with Claude Code

For Bronze Tier, manually trigger Claude Code to process pending items:

```bash
# Navigate to vault directory
cd AI_Employee_Vault

# Run Claude Code with instructions
claude "Check /Needs_Action folder and process any pending items according to Company_Handbook.md"
```

## 📖 Usage Guide

### How the File System Watcher Works

1. **Drop a file** into the `AI_Employee_Vault/Drop_Folder`
2. **Watcher detects** the new file within 30 seconds
3. **Action file created** in `/Needs_Action` with:
   - YAML frontmatter (type, priority, status)
   - File preview (if text file)
   - Suggested actions checklist
4. **Orchestrator logs** the new item
5. **Claude Code processes** the action file when triggered

### Example: Processing a Document

1. Drop `meeting_notes.txt` into `Drop_Folder`
2. Watcher creates `FILE_meeting_notes_TIMESTAMP.md` in `/Needs_Action`
3. Run orchestrator: `python scripts/orchestrator.py "path/to/vault" --run-once`
4. Open Obsidian and review the action file
5. Use Claude Code to summarize and categorize:
   ```
   claude "Read the meeting notes in /Needs_Action and create a summary in /Done"
   ```

### Human-in-the-Loop Pattern

For sensitive actions:

1. AI creates file in `/Pending_Approval/`
2. Human reviews and moves to `/Approved/` or `/Rejected/`
3. AI processes only approved items
4. All actions logged to `/Logs/`

## 🔧 Configuration

### Watcher Configuration

Edit `scripts/filesystem_watcher.py` to customize:

```python
# Check interval (default: 30 seconds for real-time)
check_interval = 30

# Drop folder location
self.drop_folder = self.vault_path / 'Drop_Folder'
```

### Orchestrator Configuration

Edit `scripts/orchestrator.py` to customize:

```python
# Check interval (default: 60 seconds)
check_interval = 60

# Log file location
self.logs = self.vault_path / 'Logs'
```

## 📊 Dashboard

The `Dashboard.md` provides real-time visibility:

| Section | Description |
|---------|-------------|
| **Quick Stats** | Pending, in-progress, completed counts |
| **Inbox Status** | File counts per folder |
| **Financial Summary** | Revenue and expenses (manual entry for Bronze) |
| **Active Projects** | Current project tracking |
| **Recent Activity** | Latest processed items |

## 🧪 Testing

### Test the File System Watcher

1. **Start the watcher:**
   ```bash
   python scripts/filesystem_watcher.py "path/to/AI_Employee_Vault"
   ```

2. **Drop a test file:**
   - Create a text file named `test.txt`
   - Put some content in it
   - Save to `AI_Employee_Vault/Drop_Folder`

3. **Verify action file created:**
   - Check `AI_Employee_Vault/Needs_Action/`
   - Should see `FILE_test_*.md`

4. **Run orchestrator:**
   ```bash
   python scripts/orchestrator.py "path/to/AI_Employee_Vault" --run-once
   ```

5. **Check logs:**
   - Open `AI_Employee_Vault/Logs/orchestrator_*.log`

### Test the Orchestrator

```bash
# Run single cycle with verbose output
python scripts/orchestrator.py "path/to/AI_Employee_Vault" --run-once

# Check dashboard was updated
# Open AI_Employee_Vault/Dashboard.md in Obsidian
```

## 📝 Sample Files

The vault includes sample action files for reference:

- `Needs_Action/FILE_example_document_SAMPLE.md` - Example file drop action
- `Needs_Action/INVOICE_REQUEST_sample.md` - Example invoice request

## 🔐 Security Notes

### For Bronze Tier

- ✅ All data stays local in your Obsidian vault
- ✅ No external API calls required
- ✅ File System Watcher uses only local file system
- ⚠️ Never drop files containing sensitive data into the drop folder
- ⚠️ Review all AI actions before executing in real scenarios

### Future Tiers (Silver/Gold)

When adding Gmail, WhatsApp, or banking integrations:

- Use environment variables for credentials
- Never store API keys in vault files
- Enable human-in-the-loop for sensitive actions
- Review audit logs regularly

## 🚧 Upgrading to Silver Tier

To extend beyond Bronze:

1. **Add Gmail Watcher** - Monitor inbox for important emails
2. **Add WhatsApp Watcher** - Use Playwright for WhatsApp Web monitoring
3. **Implement MCP Servers** - Enable external actions (send emails, make payments)
4. **Add Plan.md Generation** - Claude creates structured plans
5. **Implement Approval Workflow** - Full human-in-the-loop system

## 🐛 Troubleshooting

### Watcher not detecting files

- Ensure the drop folder path is correct
- Check watcher logs in `/Logs/watcher_*.log`
- Verify file permissions allow reading the drop folder
- Try restarting the watcher script

### Orchestrator not processing items

- Check orchestrator logs in `/Logs/orchestrator_*.log`
- Ensure vault path is correct
- Verify Python has write access to vault folders
- Run with `--run-once` to see error output

### Dashboard not updating

- Ensure `Dashboard.md` exists in vault root
- Check file permissions
- Run orchestrator manually to trigger update

## 📚 Additional Resources

- [Main Hackathon Document](./Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Company Handbook](./AI_Employee_Vault/Company_Handbook.md)
- [Business Goals](./AI_Employee_Vault/Business_Goals.md)
- [Claude Code Documentation](https://claude.com/product/claude-code)
- [Obsidian Help](https://help.obsidian.md/)

## 📈 Next Steps

1. **Customize** `Company_Handbook.md` with your rules
2. **Update** `Business_Goals.md` with your objectives
3. **Test** the File System Watcher with sample files
4. **Integrate** Claude Code for automated processing
5. **Consider** upgrading to Silver Tier with Gmail/WhatsApp watchers

## 🎯 Success Criteria (Bronze Tier)

- [x] Vault structure created
- [x] Dashboard.md operational
- [x] Company_Handbook.md defined
- [x] File System Watcher running
- [x] Orchestrator processing items
- [ ] Claude Code integration tested
- [ ] First real task processed end-to-end

---

*AI Employee v0.1 (Bronze Tier) - Built for Hackathon 0*

*Last updated: 2026-03-16*
