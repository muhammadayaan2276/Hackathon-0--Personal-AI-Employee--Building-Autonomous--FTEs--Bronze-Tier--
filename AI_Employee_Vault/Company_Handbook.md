---
version: 0.1-bronze
last_updated: 2026-03-17
---

# 📖 Company Handbook

## 🎯 Core Rules

### 1. File Processing
- All files from `/Inbox/` → `/Needs_Action/` (automatic)
- Process one by one
- Move to `/Done/` when complete

### 2. Priority Levels
| Priority | Response Time |
|----------|---------------|
| **High** | Within 1 hour |
| **Medium** | Within 24 hours |
| **Low** | Within 7 days |

### 3. Human-in-the-Loop
- ✅ AI: Automatic processing
- ✅ AI: File movement
- ✅ AI: Dashboard updates
- 👤 **HUMAN**: Approve/Reject decisions

---

## 📋 Workflow

```
Inbox → Needs_Action → Processing → Done
```

### Step-by-Step:

1. **USER** drops file in `/Inbox/`
2. **AI** detects (30 seconds)
3. **AI** creates action file in `/Needs_Action/`
4. **AI** processes content
5. **AI** moves to `/Done/`
6. **Dashboard** updates automatically

---

## ⚠️ Important

### Delete Files Properly:
```
To remove a task:
1. Delete from /Inbox/ (original file)
2. Delete from /Needs_Action/ (action file)
Both must be deleted!
```

### Don't:
- ❌ Don't edit action files manually
- ❌ Don't move files between folders manually
- ❌ Don't delete Dashboard.md

---

*Simple rules for Bronze Tier*
