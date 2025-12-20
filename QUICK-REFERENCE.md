# Claude Code Quick Reference

## Commands

| Command | Purpose |
|---------|---------|
| `/project:init-project` | Initialize from spec.md |
| `/project:continue` | Work on next feature |
| `/project:status` | Show progress |
| `/project:verify` | Test all features |
| `/project:handoff` | Save state for next session |
| `/project:review` | Code review |
| `/project:branch` | Manage branches |
| `/project:add-feature` | Add to backlog |
| `/project:security-scan` | Security check |
| `/project:tdd` | Test-driven development |
| `/project:decide` | High-stakes decision analysis |
| `/project:constraints` | Define implementation boundaries |
| `/project:perspectives` | Multi-viewpoint analysis |

---

## Thinking Triggers

```
think < think hard < think harder < ultrathink
```

Use: "Think hard about the architecture before implementing"

---

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project rules (always read) |
| `DESIGN.md` | Architecture (from Browser Claude) |
| `features.json` | Feature tracking |
| `claude-progress.txt` | Session notes |

---

## Feature Tracking

```json
{
  "id": "F001",
  "passes": false,  // Red until verified
  "acceptance_criteria": [
    {"criterion": "...", "passes": false}
  ]
}
```

**Rule:** Never set `passes: true` without testing.

---

## Workflow

```
Browser Claude (Opus)              Claude Code (Sonnet)
─────────────────────              ──────────────────────
prompt-spec-ready.md          →   
Answer discovery questions        
Get: DESIGN.md, features.json     
                                  setup-wizard.sh
                                  /project:continue (repeat)
                                  /project:handoff (end session)
```

---

## Git Commits

Format: `type: description`

| Type | When |
|------|------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation |
| `refactor:` | Code cleanup |
| `test:` | Tests only |

---

## Interrupt

Press `Escape` to stop Claude and redirect.

---

## Start Claude Code

```bash
claude --dangerously-skip-permissions
```

---

## Verification Loop

```
Implement → Test → Verify E2E → Update features.json → Commit
```

Never skip verification.
