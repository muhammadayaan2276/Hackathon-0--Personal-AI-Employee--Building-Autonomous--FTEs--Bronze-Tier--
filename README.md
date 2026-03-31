# 🤖 Personal AI Employee - Bronze Tier

> **Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.**

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start File Watcher
```bash
python scripts\filesystem_watcher.py "C:\Users\pc\Desktop\desktop-tutorial\Hackathon-0--Personal-AI-Employee--Building-Autonomous--FTEs--Bronze-Tier--\AI_Employee_Vault"
```

### Step 2: Start Orchestrator (New Terminal)
```bash
python scripts\orchestrator.py "C:\Users\pc\Desktop\desktop-tutorial\Hackathon-0--Personal-AI-Employee--Building-Autonomous--FTEs--Bronze-Tier--\AI_Employee_Vault"
```

### Step 3: Drop Files & Process
- **Drop any file** → `AI_Employee_Vault/Inbox/`
- **Watcher** creates action file in `/Needs_Action`
- **Orchestrator** processes and updates `Dashboard.md`

---

## 📋 How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐     ┌──────────┐
│ Drop File   │ →   │ File Watcher │ →   │ Orchestrator    │ →   │ Dashboard│
│  /Inbox/    │     │  (Detects)   │     │  (Processes)    │     │  (Stats) │
└─────────────┘     └──────────────┘     └─────────────────┘     └──────────┘
```

**Flow:**
1. You drop a file in `/Inbox`
2. **Watcher** detects it → creates action file in `/Needs_Action`
3. **Orchestrator** reads action file → processes → moves to `/Done`
4. **Dashboard.md** auto-updates with stats every 30 seconds

---

## 📁 Vault Structure

```
AI_Employee_Vault/
├── Inbox/           # Drop files here
├── Needs_Action/    # Pending tasks (auto-created)
├── Done/            # Completed tasks
├── Files/           # Original files backup
├── Logs/            # System logs
├── Dashboard.md     # Real-time stats
├── Company_Handbook.md  # Rules
└── Business_Goals.md    # Objectives
```

---

## 🛠️ Commands Reference

| Task | Command |
|------|---------|
| **Start Watcher** | `python scripts\filesystem_watcher.py "path\to\vault"` |
| **Start Orchestrator** | `python scripts\orchestrator.py "path\to\vault"` |
| **Run Once (Test)** | `python scripts\orchestrator.py "path\to\vault" --run-once` |

---

## ✅ Test It

```bash
# 1. Start watcher (Terminal 1)
python scripts\filesystem_watcher.py "C:\Users\pc\Desktop\desktop-tutorial\Hackathon-0--Personal-AI-Employee--Building-Autonomous--FTEs--Bronze-Tier--\AI_Employee_Vault"

# 2. Start orchestrator (Terminal 2)
python scripts\orchestrator.py "C:\Users\pc\Desktop\desktop-tutorial\Hackathon-0--Personal-AI-Employee--Building-Autonomous--FTEs--Bronze-Tier--\AI_Employee_Vault"

# 3. Drop a test file in AI_Employee_Vault/Inbox/

# 4. Check AI_Employee_Vault/Needs_Action/ for action file
# 5. Open Dashboard.md to see updated stats
```

---

## 📊 Dashboard

Open `AI_Employee_Vault/Dashboard.md` in **Obsidian** for real-time view:
- Pending actions count
- Completed today/this week
- Inbox status
- Financial summary

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Watcher not detecting | Ensure file dropped in `/Inbox` |
| Orchestrator not running | Check logs in `/Logs/orchestrator_*.log` |
| Dashboard not updating | Run orchestrator with `--run-once` |

---

## 📚 Next Steps

1. **Customize** `Company_Handbook.md` with your rules
2. **Update** `Business_Goals.md` with objectives
3. **Test** with sample files
4. **Upgrade** to Silver Tier (Gmail/WhatsApp watchers)

---

*AI Employee v0.1 (Bronze Tier) | Last updated: 2026-03-31*
