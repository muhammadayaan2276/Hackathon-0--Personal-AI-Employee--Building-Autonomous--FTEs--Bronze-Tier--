# Personal AI Employee Hackathon - Project Context

## Project Overview

This is a **Bronze Tier** hackathon project for building a **Personal AI Employee** - an autonomous AI agent that manages personal and business affairs 24/7. The project uses **Claude Code** as the reasoning engine and **Obsidian** (local Markdown) as the management dashboard.

**Tagline:** *Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*

### Core Architecture

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Brain** | Claude Code | Reasoning engine for decision-making |
| **Memory/GUI** | Obsidian Vault | Dashboard and long-term memory (Markdown files) |
| **Senses** | Python Watchers | Monitor Gmail, WhatsApp, filesystems to trigger AI |
| **Hands** | MCP Servers | Model Context Protocol for external actions |

### Key Concepts

- **Digital FTE (Full-Time Equivalent):** An AI agent priced and managed like a human employee
- **Watcher Pattern:** Lightweight Python scripts that monitor inputs and create `.md` files in `/Needs_Action`
- **Ralph Wiggum Loop:** A persistence pattern using Stop hooks to keep Claude working until tasks complete
- **Human-in-the-Loop:** Sensitive actions require approval via file movement (`/Pending_Approval` → `/Approved`)

## Directory Structure

```
Hackathon-0--Personal-AI-Employee/
├── .qwen/skills/
│   └── browsing-with-playwright/    # Playwright MCP skill for browser automation
│       ├── SKILL.md                 # Browser automation documentation
│       ├── references/
│       │   └── playwright-tools.md  # Complete MCP tool reference
│       └── scripts/
│           ├── mcp-client.py        # MCP client for Playwright calls
│           ├── start-server.sh      # Start Playwright MCP server
│           ├── stop-server.sh       # Stop Playwright MCP server
│           └── verify.py            # Server health check
├── skills-lock.json                 # Qwen skill registry
└── Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md  # Full hackathon guide
```

## Technologies & Dependencies

| Component | Technology | Purpose |
|-----------|------------|---------|
| **AI Engine** | Claude Code | Primary reasoning and task execution |
| **Dashboard** | Obsidian | Local Markdown knowledge base |
| **Browser Automation** | Playwright MCP | Web interaction (forms, navigation, screenshots) |
| **Scripting** | Python 3.13+ | Watcher scripts and orchestration |
| **Runtime** | Node.js v24+ | MCP servers |
| **Version Control** | Git / GitHub Desktop | Vault versioning |

## Building & Running

### Prerequisites Setup

```bash
# Verify Claude Code
claude --version

# Verify Python (3.13+)
python --version

# Verify Node.js (v24+)
node --version
```

### Playwright MCP Server (Browser Automation)

```bash
# Start the Playwright MCP server
bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh

# Verify server is running
python .qwen/skills/browsing-with-playwright/scripts/verify.py

# Stop the server
bash .qwen/skills/browsing-with-playwright/scripts/stop-server.sh
```

### Making MCP Calls

```bash
# Example: Navigate to a URL
python scripts/mcp-client.py call -u http://localhost:8808 -t browser_navigate \
  -p '{"url": "https://example.com"}'

# Example: Take a page snapshot
python scripts/mcp-client.py call -u http://localhost:8808 -t browser_snapshot -p '{}'
```

### Ralph Wiggum Loop (Autonomous Task Completion)

```bash
# Start a Ralph loop for multi-step tasks
/ralph-loop "Process all files in /Needs_Action, move to /Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

## Development Conventions

### Folder Structure (Obsidian Vault)

When creating the Obsidian vault, use this structure:

```
AI_Employee_Vault/
├── Inbox/                    # Raw incoming items
├── Needs_Action/             # Items requiring processing
├── In_Progress/<agent>/      # Claimed tasks (prevents double-work)
├── Pending_Approval/         # Awaiting human approval
├── Approved/                 # Approved actions ready for execution
├── Rejected/                 # Rejected actions
├── Done/                     # Completed tasks
├── Plans/                    # Generated plans with checkboxes
├── Briefings/                # CEO briefings and reports
├── Accounting/               # Bank transactions and financial data
└── Dashboard.md              # Real-time summary
```

### File Naming Conventions

- **Action Files:** `EMAIL_<id>.md`, `WHATSAPP_<id>.md`, `FILE_<name>.md`
- **Approval Requests:** `APPROVAL_<type>_<description>_<date>.md`
- **Plans:** `Plan_<task>_<date>.md`
- **Briefings:** `YYYY-MM-DD_Day_Briefing.md`

### Markdown Schema Standards

All action files should include YAML frontmatter:

```yaml
---
type: email
from: sender@example.com
subject: Subject Line
received: 2026-01-07T10:30:00Z
priority: high
status: pending
---
```

### Human-in-the-Loop Pattern

For sensitive actions (payments, sending emails), Claude writes an approval request:

```markdown
---
type: approval_request
action: payment
amount: 500.00
recipient: Client A
created: 2026-01-07T10:30:00Z
expires: 2026-01-08T10:30:00Z
status: pending
---

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder.
```

## Testing Practices

### Verification Steps

1. **Server Health:** Run `verify.py` before browser automation tasks
2. **File Operations:** Test file read/write in vault before automation
3. **Approval Workflow:** Manually test file movement pattern

### Debugging

```bash
# Check if Playwright MCP server is running
pgrep -f "@playwright/mcp"

# Restart server if needed
bash scripts/stop-server.sh && bash scripts/start-server.sh
```

## Hackathon Tiers

| Tier | Requirements | Estimated Time |
|------|-------------|----------------|
| **Bronze** | Obsidian dashboard, 1 watcher, Claude reading/writing vault | 8-12 hours |
| **Silver** | 2+ watchers, Plan.md generation, 1 MCP server, HITL workflow | 20-30 hours |
| **Gold** | Full integration, Odoo accounting, multiple MCPs, Ralph Wiggum loop | 40+ hours |
| **Platinum** | Cloud deployment, Cloud/Local split, A2A upgrade | 60+ hours |

## Key Resources

- **Main Documentation:** `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Browser Automation:** `.qwen/skills/browsing-with-playwright/SKILL.md`
- **MCP Tool Reference:** `.qwen/skills/browsing-with-playwright/references/playwright-tools.md`
- **Ralph Wiggum Pattern:** [GitHub Reference](https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum)

## Meeting Information

**Weekly Research & Showcase:** Wednesdays at 10:00 PM PKT on Zoom
- Meeting ID: 871 8870 7642
- Passcode: 744832
- YouTube: [Panaversity](https://www.youtube.com/@panaversity)
