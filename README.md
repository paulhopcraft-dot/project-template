# Claude Code Best Practices Toolkit

A complete workflow system for building apps with Claude. Uses Browser Claude (Opus) for planning, Claude Code (Sonnet) for building.

## Quick Start

```bash
# Clone this repo
git clone https://github.com/yourusername/claude-code-toolkit.git

# Starting a new project? Open Browser Claude and paste prompt-spec-ready.md
# Then download the generated specs to your project folder

# Run setup
cd your-project
bash /path/to/claude-code-toolkit/setup-wizard.sh

# Start building
claude --dangerously-skip-permissions
/project:continue
```

## Workflow

```
Browser Claude (Opus)              Claude Code (Sonnet)
─────────────────────              ──────────────────────
1. Paste prompt-spec-ready.md →   
2. Answer discovery questions     
3. Download generated specs       
                                  4. bash setup-wizard.sh
                                  5. /project:continue (repeat)
                                  6. /project:handoff (end session)
```

## What's Included

| File | What it does |
|------|--------------|
| `prompt-spec-ready.md` | Paste into Browser Claude to generate specs |
| `prompt-existing-project.md` | Add toolkit to existing codebase |
| `prompt-harness.md` | Long-running agent pattern (advanced) |
| `setup-wizard.sh` | Sets up project with toolkit files |

### Templates (created by setup-wizard.sh)

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project rules Claude Code always reads |
| `features.json` | Track features (red until verified) |
| `claude-progress.txt` | Session handoff notes |

### Slash Commands (created in .claude/commands/)

| Command | What it does |
|---------|--------------|
| `/project:continue` | Work on next feature |
| `/project:status` | Show progress |
| `/project:verify` | Test all features |
| `/project:handoff` | Save state for next session |
| `/project:review` | Code review |
| `/project:branch` | Manage branches |
| `/project:add-feature` | Add to backlog |
| `/project:security-scan` | Security check |
| `/project:tdd` | Test-driven development |

## Core Concepts

### Red → Green Pattern

All features start `"passes": false` (red). Only flip to `true` after:
- Tests written and passing
- Verified end-to-end
- Acceptance criteria met

```json
{
  "id": "F001",
  "passes": false,
  "acceptance_criteria": [
    {"criterion": "User can log in", "passes": false}
  ]
}
```

### Session Continuity

`claude-progress.txt` maintains context between sessions:
- What was completed
- What's in progress
- What to do next
- Any blockers

### Verification Loop

```
Implement → Test → Verify E2E → Update features.json → Commit
```

Never skip verification. Never mark complete without testing.

## Two Scenarios

### Spec-Ready Project
You have specs from Browser Claude, no code yet.

```bash
mkdir my-project && cd my-project
# Copy spec files here
bash /path/to/setup-wizard.sh
claude --dangerously-skip-permissions
/project:continue
```

### Existing Project
Code already exists, adding toolkit.

```bash
cd existing-project
bash /path/to/setup-wizard.sh
claude --dangerously-skip-permissions
/project:continue
```

## Tips

### Thinking Triggers
```
think < think hard < think harder < ultrathink
```
Use: "Think hard about the architecture before implementing"

### Interrupt
Press `Escape` to stop Claude and redirect.

### Daily Workflow
1. `claude --dangerously-skip-permissions`
2. `/project:status`
3. `/project:continue` (repeat)
4. `/project:handoff` (end of day)

## Documentation

- [BEGINNERS-GUIDE.md](BEGINNERS-GUIDE.md) - Step-by-step for non-technical users
- [QUICK-REFERENCE.md](QUICK-REFERENCE.md) - Cheat sheet
- [TOOLKIT-OVERVIEW.md](TOOLKIT-OVERVIEW.md) - Full documentation

## Why This Works

| Problem | Solution |
|---------|----------|
| Claude says "done" but it's broken | `passes: false` until verified |
| Lost context between sessions | `claude-progress.txt` handoff |
| No idea what's left | `features.json` tracking |
| Inconsistent quality | Engineering mode constraints |
| Planning vs building needs different skills | Opus plans, Sonnet builds |

## License

MIT - Use however you want.
