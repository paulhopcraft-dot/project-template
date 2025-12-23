# Claude Code Best Practices Toolkit

**Complete package for autonomous Claude Code development**

---

## Workflow

```
Browser Claude (Opus)              Claude Code (Sonnet)
─────────────────────              ──────────────────────
1. Discovery questions        →   
2. Generate specs:                
   - DESIGN.md                    
   - REQUIREMENTS.md              
   - API.md, SCHEMA.md            
   - features.json                
                                  3. /project:continue
                                  4. Build features
                                  5. Verify & commit
```

---

## Toolkit Contents

```
claude-code-toolkit/
├── TOOLKIT-OVERVIEW.md          # This file
├── setup-wizard.sh              # Interactive setup (spec-ready or existing)
├── prompt-spec-ready.md         # Generate specs in Browser Claude
├── prompt-existing-project.md   # Retrofit existing codebase
├── prompt-harness.md            # Long-running agent harness (red→green)
│
├── templates/
│   ├── CLAUDE.md                # Project root instructions
│   ├── features.json            # Feature tracking with schema validation
│   ├── features.schema.json     # JSON schema for validation
│   ├── claude-progress.txt      # Session continuity log
│   ├── .gitignore               # Multi-stack gitignore
│   ├── .env.example             # Environment variables template
│   ├── tests/                   # Test templates (Python, TypeScript, Go)
│   └── .github/workflows/       # CI/CD templates
│
├── commands/                    # 30+ slash commands for .claude/commands/
│   ├── Core workflow (continue, status, verify, handoff, help)
│   ├── PRD enforcement (prd-check, build-prd, edit-prd, design-prd)
│   ├── Decision making (decide, constraints, perspectives)
│   ├── Recovery & validation (recover, validate-features)
│   └── ...and 20+ more commands
│
├── skills/                      # For /mnt/skills/user/
│   ├── engineering-mode/
│   │   └── SKILL.md             # Global engineering constraints
│   └── frontend-design/
│       └── SKILL.md             # Anthropic's UI design skill
│
└── agents/
    ├── initializer-agent.md     # First context window setup
    └── coding-agent.md          # Autonomous implementation
```

---

## Quick Start

### Spec-Ready Project (You have specs from Browser Claude)
```bash
mkdir my-project && cd my-project
# Copy your spec files here (DESIGN.md, features.json, etc.)
bash /path/to/claude-code-toolkit/setup-wizard.sh
claude --dangerously-skip-permissions
/project:continue
```

### Existing Project (Code exists, adding toolkit)
```bash
cd your-existing-project
bash /path/to/claude-code-toolkit/setup-wizard.sh
claude --dangerously-skip-permissions
/project:continue
```

### Generate Specs (In Browser Claude first)
Use `prompt-spec-ready.md` - paste into Browser Claude to generate all spec docs before moving to Claude Code.

---

## Core Patterns

### 1. Harness Pattern (Red → Green)
```json
{
  "id": "F001",
  "passes": false,  // Red until verified
  "acceptance_criteria": [
    {"criterion": "...", "passes": false}
  ]
}
```
Features stay `passes: false` until ALL criteria verified.

### 2. Initializer → Coding Agent Split
- **Initializer**: Reads spec, creates feature list, sets up structure
- **Coding Agent**: Picks next failing feature, implements, verifies

### 3. Context Management
```
Your context will auto-compact at limits.
Never stop early due to token budget.
Save progress before context refresh.
```

### 4. Verification Loop
```
Implement → Test → Verify end-to-end → Mark passing → Commit
```

---

## Thinking Triggers
```
think < think hard < think harder < ultrathink
```
Each level allocates more thinking budget.

---

## Key Files Explained

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project instructions, always read |
| `features.json` | Track features (JSON > markdown) |
| `claude-progress.txt` | Session handoff notes |
| `spec.md` | Requirements (human fills in) |

---

## Slash Commands

| Command | What it does |
|---------|--------------|
| `/project:init-project` | Initialize from spec.md |
| `/project:continue` | Pick next failing feature, implement |
| `/project:status` | Show progress, blockers |
| `/project:verify` | Test all "passing" features actually work |
| `/project:handoff` | Save state for next session |
| `/project:review` | Code review current work |
| `/project:decide` | High-stakes decision with confidence weighting |
| `/project:constraints` | Define implementation boundaries |
| `/project:perspectives` | Multi-viewpoint analysis |

### PRD-Aware Commands
| Command | Purpose |
|---------|---------|
| `/prd-check` | Verify PRD alignment before changes |
| `/build-prd` | Build with PRD enforcement |
| `/edit-prd` | Edit with PRD validation |
| `/design-prd` | Design within PRD constraints |

---

## Engineering Constraints (Always Active)

- Avoid over-engineering
- One feature at a time
- Commit after each verified feature
- Never mark complete without testing
- JSON tracking over markdown
- Conventional commits

---

## Integration with Skills System

For multi-project setups, add project-specific contracts:

```
/mnt/skills/user/
├── engineering-mode/     # Global (always loads)
├── gpnet-contract/       # Project-specific
├── echo25-contract/
└── ...
```

Global rules in `engineering-mode`, project overrides in contracts.
