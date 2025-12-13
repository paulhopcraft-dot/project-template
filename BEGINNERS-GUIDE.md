# Claude Code Beginner's Guide

No technical background needed. Just follow the steps.

---

## What is This?

Claude Code is an AI coding assistant that runs in your terminal. This toolkit gives it best practices so it builds things properly.

**Your Workflow:**
1. **Browser Claude (Opus)** → Discovery, create specs
2. **Claude Code (Sonnet)** → Build from those specs

---

## First Time Setup (One Time Only)

### Step 1: Install Claude Code

```bash
# Mac/Linux
curl -fsSL https://claude.ai/install | sh

# Windows
# Download from claude.ai/download
```

### Step 2: Get the Toolkit

Download and unzip `claude-code-toolkit.zip` somewhere you'll remember.

---

## Starting a Spec-Ready Project

### Step 1: Create Specs in Browser Claude

Use `prompt-spec-ready.md` - paste it into Browser Claude and answer the discovery questions. You'll get:
- DESIGN.md
- REQUIREMENTS.md
- API.md
- SCHEMA.md
- features.json

### Step 2: Create Project Folder

```bash
mkdir my-project
cd my-project
```

### Step 3: Copy Your Specs

Move all the spec files Browser Claude created into this folder.

### Step 4: Run Setup

```bash
bash /path/to/claude-code-toolkit/setup-wizard.sh
```

### Step 5: Start Claude Code

```bash
claude --dangerously-skip-permissions
```

### Step 6: Build It

Type:
```
/project:continue
```

Claude picks up features from your specs and builds them. Keep saying `/project:continue` until done.

---

## Daily Workflow

1. Open terminal in your project folder
2. Run `claude --dangerously-skip-permissions`
3. Type `/project:continue`
4. When done for the day: `/project:handoff`

---

## Useful Commands

| Command | What it does |
|---------|--------------|
| `/project:continue` | Work on next feature |
| `/project:status` | See progress |
| `/project:handoff` | Save state for next time |
| `/project:verify` | Check everything works |
| `/project:review` | Get code review |

---

## If Something Goes Wrong

### Claude Stops Mid-Task
Just say "continue" or run `/project:continue`

### Claude Goes Off Track
Press `Escape` to interrupt, then redirect

### Tests Failing
Ask: "Why are the tests failing? Fix them."

### Stuck for >10 Minutes
Ask: "I'm stuck on X. What are my options?"

---

## Tips

1. **Be specific** - "Add a login button that sends email/password to /api/login" beats "add login"

2. **One thing at a time** - Don't ask for 5 features at once

3. **Check the work** - Run `/project:verify` periodically

4. **Save progress** - Run `/project:handoff` before closing

---

## Glossary

| Term | Meaning |
|------|---------|
| Terminal | The text-based interface (Command Prompt, Terminal app) |
| Repository | Your project folder with git tracking |
| Commit | Saving a checkpoint of your code |
| Feature | One piece of functionality |
| Test | Code that checks if other code works |

---

That's it. Start building!
