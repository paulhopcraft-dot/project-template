# Claude Code Toolkit - Comprehensive Cheat Sheet

*Last Updated: 2026-01-06 | Version: Session 7*

## 🚀 **Quick Start Commands**

| Situation | Command | What It Does |
|-----------|---------|--------------|
| Starting session | `/status` | Show project health, recent commits, next actions |
| What should I work on? | `/continue` | Resume where we left off, pick next task |
| Ending session | `/handoff` | Clean session end, save state for next time |
| Daily AI news | `/morning-brief` | Aggregate latest AI videos from 11 YouTube channels |
| View/edit settings | `/config` | Show or modify toolkit-config.yaml settings |

## 📋 **Task Management & Planning**

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/status` | Project health check | Start of every session, after completing tasks |
| `/continue` | Resume previous work | When you want Claude to pick next priority |
| `/autonomous` | Work independently | For 3+ similar tasks, batch work |
| `/anticipate` | Devil's advocate analysis | Before risky changes, complex decisions |
| `/think` | Thinking mode selector | Complex problems needing different approaches |
| `/decide` | High-stakes decisions | Choosing between libraries/frameworks/approaches |

## 🔨 **Development Commands**

### Core Development
| Command | Purpose | Best For |
|---------|---------|----------|
| `/tdd` | Test-driven development | New functions/classes, critical code |
| `/review` | Code review current work | Before commits, 100+ line changes |
| `/verify` | End-to-end testing | Feature completion, integration testing |
| `/build-prd` | Feature with PRD validation | Structured feature development |
| `/edit-prd` | Edit with PRD constraints | Modifying existing features |

### Advanced Development
| Command | Purpose | Use Cases |
|---------|---------|-----------|
| `/branch` | Feature branch management | Multi-file changes, new features |
| `/resolve` | AI-assisted merge conflicts | Git merge issues |
| `/constraints` | Define implementation constraints | Before complex features |
| `/validate` | Blind validation testing | Separate verifier runs tests |
| `/security-scan` | Security analysis | Auth code, .env files, sensitive changes |

## 🧠 **AI & Intelligence Commands**

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/think-parallel` | Decompose, Plan, Merge | Complex multi-part problems |
| `/perspectives` | Multiple viewpoint analysis | Important architectural decisions |
| `/expert` | Role-based constraint prompting | Need 10x more specific outputs |
| `/react` | Thought-Action-Observation cycles | Systematic problem solving |
| `/pal` | Program-Aided Language solving | Math/logic problems via executable code |

## 📊 **Project Management**

### Project Setup & Tracking
| Command | Purpose | Notes |
|---------|---------|-------|
| `/init-project` | Initialize new project | Creates features.json, tracking files |
| `/add-feature` | Add feature to features.json | Structured feature management |
| `/validate-features` | Check features.json schema | Ensure tracking file integrity |
| `/index` | Generate PROJECT_INDEX.json | Codebase mapping and documentation |

### Memory & Context
| Command | Purpose | Best For |
|---------|---------|----------|
| `/remember` | Store important context | Cross-session persistence |
| `/recall` | Retrieve stored memories | Finding previous decisions/context |
| `/context` | Check context window usage | Managing conversation length |
| `/fresh` | Context reset with state preservation | Clean slate while keeping progress |

## 🛠 **Specialized Tools**

### Document Generation
| Skill | Output Format | Use Cases |
|-------|---------------|-----------|
| `pdf` | PDF documents | Reports, documentation, presentations |
| `docx` | Word documents | Formal documents, proposals |
| `xlsx` | Excel spreadsheets | Data analysis, financial reports |
| `pptx` | PowerPoint presentations | Slide decks, presentations |

### Development Workflows
| Command | Purpose | Workflow Type |
|---------|---------|---------------|
| `/worktree` | Git worktree isolation | Safe feature development |
| `/delegate` | Spawn sub-agents | Isolated task management |
| `/launch` | Launch app in browser | Web application testing |
| `/frontend-design` | Production-grade UI design | Web components, pages, applications |

## 🔧 **Configuration & Settings**

### Core Configuration
```yaml
# toolkit-config.yaml structure
settings:
  default_model: "sonnet"          # sonnet | opus | haiku
  thinking_mode: "auto"           # auto | interleaved | none
  auto_commit: false              # Auto-commit completed features

projects:
  sync_enabled: true              # Sync skills to other projects
  sync_projects: [...]            # List of project paths

testing:
  run_before_commit: true         # Auto-run tests before commits
  parallel_execution: false      # Run tests in parallel
```

### Model Selection Rules
| Use Case | Model | Why |
|----------|-------|-----|
| Feature implementation | Sonnet | Fast, efficient for routine coding |
| Architecture decisions | Opus | Deep reasoning for complex choices |
| Quick tasks | Haiku | Speed and cost optimization |
| Library/framework choice | Opus | Requires careful evaluation |
| Complex debugging (>30min) | Opus | Deep analysis capabilities |

## 📈 **Workflow Patterns**

### Daily Development Workflow
1. **Start**: `/status` → See project state
2. **Work**: `/continue` → Pick up where left off
3. **Commit**: `/review` → Check before commit
4. **End**: `/handoff` → Clean session end

### Feature Development Workflow
1. **Plan**: `/anticipate` or `/think-parallel`
2. **Build**: `/tdd` or `/build-prd`
3. **Test**: `/verify`
4. **Review**: `/review`
5. **Track**: Update features.json

### Complex Problem Solving
1. **Analyze**: `/think` → Choose thinking mode
2. **Plan**: `/think-parallel` → Break down problem
3. **Decide**: `/decide` → Make key choices
4. **Execute**: `/autonomous` → Implement solution
5. **Validate**: `/validate` → Blind testing

## 🚨 **Emergency & Recovery**

| Problem | Command | What It Does |
|---------|---------|--------------|
| Tests failing | `/recover` | Diagnose and fix issues |
| Corrupted state | `/recover` | Restore from backup state |
| Merge conflicts | `/resolve` | AI-assisted resolution |
| Security concerns | `/security-scan` | Check for vulnerabilities |
| Lost context | `/reload` | Reload project context after /clear |

## 💡 **Pro Tips**

### Efficiency
- **Use `/status` after every task** - Shows progress and next actions
- **Chain commands** for related work: `/review` → `/verify` → commit
- **Use `/autonomous` for repetitive tasks** - Let Claude work independently
- **Model switching** - Use `/decide` to spawn Opus for architecture choices

### Best Practices
- **Always run tests before commits** - Use `/verify` or auto-testing
- **Document important decisions** - Use `/remember` for future reference
- **Use branches for risky changes** - `/branch` for isolation
- **Review before big commits** - Use `/review` for 100+ line changes

### Advanced Usage
- **Parallel work** - Use `/delegate` to spawn sub-agents
- **Complex analysis** - Use `/perspectives` for multi-angle views
- **Memory management** - Use `/context` to monitor conversation length

## 🗂 **File Structure**

```
claude-code-toolkit/
├── toolkit-config.yaml          # Main configuration
├── claude-progress.txt           # Session progress tracking
├── features.json                 # Feature tracking (if project uses)
├── TOOLKIT-CHEAT-SHEET.md       # This guide
├── .claude/
│   ├── skills/                   # All available skills
│   └── settings.local.json       # Local Claude settings
├── briefs/                       # Morning brief outputs
└── scripts/
    ├── morning-brief.ps1         # YouTube news aggregator
    ├── copy-toolkit.ps1          # Sync toolkit to projects
    └── run-tests-simple.ps1      # Test runner
```

## 🎯 **Quick Reference Card**

**Most Used Commands:**
- `/status` - Check project state
- `/continue` - Resume work
- `/review` - Code review
- `/verify` - Test everything
- `/handoff` - End session

**Emergency Commands:**
- `/recover` - Fix problems
- `/resolve` - Merge conflicts
- `/security-scan` - Security check

**Discovery Commands:**
- `/help` - Search available commands
- `/config` - View/edit settings
- `/recall` - Find previous context

---

## 🔄 **Ecosystem Integration**

The toolkit syncs to 7 ecosystem projects:
- **gpnet3** - Networking system
- **goconnect** - Connection management
- **govertical** - Vertical scaling
- **gocontrol** - Control systems
- **gomemory** - Memory management (80% complete)
- **GoAgent** - AI agent framework
- **goassist3** - Assistant system

Use `copy-toolkit.ps1` to sync skills across all projects.

---

*This cheat sheet covers 90% of daily toolkit usage. Run `/help` for complete command list.*