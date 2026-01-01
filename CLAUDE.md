# Engineering Mode

## Toolkit Version: v3.0 (Context-Optimized Mode)

**Status**: ACTIVE ✓

When v3.0 is active, use the template-based command generation system:
- Read `.claude/v3/context-strategy.json` at session start
- Use templates from `.claude/v3/templates/` instead of individual commands
- Apply meta-prompting with RAG for specialized command generation
- Cache generated commands in `.claude/v3/cache/` for session reuse

**Fallback**: If v3.0 files not found, use v2.4 commands from `.claude/commands/`

## Context Management
Your context window will be automatically compacted as it approaches its limit. Save progress to memory before context refresh. Be persistent and complete tasks fully.

**v3.0 Loading Strategy**:
- Always load: CLAUDE.md, domain.json, .claude/v3/context-strategy.json, progress summary
- Lazy load: Templates, agents, patterns (only when needed)
- Progressive: Build context through RAG retrieval, not upfront loading
- Budget: Max 1,500 tokens upfront (vs 23,400 in v2.4)

## Verification Requirements
- NEVER mark a feature complete without testing end-to-end
- Run the actual test suite, don't assume tests pass
- If you can't verify something works, say so explicitly

## Engineering Constraints
- Avoid over-engineering
- Don't create unnecessary abstractions
- Keep solutions minimal and focused
- One feature at a time

## Project Commands
- Test: echo 'Add your test command'
- Lint: echo 'Add your lint command'
- Build: echo 'Add your build command'
- Dev: echo 'Add your dev command'

## Git Workflow
- Commit after each feature passes verification
- Use conventional commits: feat/fix/docs/refactor
- Push after significant milestones

## Feature Tracking
- Track features in features.json with "passes": false by default
- Mark "passes": true only after verification
- Update claude-progress.txt after each session

## Semi-Autonomous Mode (Default)

Operate proactively. Assess → Decide → Execute (or Ask) → Evaluate.

### Project Context (ALWAYS SHOW)
**EVERY response** must start with the project context line:
```
[PROJECT: folder-name]
```
This ensures the user always knows which project they're working in.

### Task Header (REQUIRED)
At the start of EVERY new task, display the full header:
```
========================================
PROJECT: [project-folder-name]
TASK: [brief task description]
========================================
```

### Mandatory Toolkit Scan (REQUIRED)
Before ANY task that takes **more than 2 minutes**, display this scan:

```
TOOLKIT SCAN:
Commands: [list from .claude/commands/ or .claude/lite/]
Skills: [list from .claude/skills/]
Agents: Explore, Plan

SELECTED FOR THIS TASK:
- [command/skill 1] - [why]
- [command/skill 2] - [why]

PROCEED?
```

**Skip scan for quick tasks** (< 2 min): typo fixes, simple questions, one-line changes.

### Active Toolkit Usage (REQUIRED - BE PROACTIVE)
The toolkit must be **actively used**, not passively mentioned:

1. **SCAN** available commands and skills (shown in toolkit scan above)
2. **SELECT** the best tools for THIS specific task
3. **INVOKE** the selected tools - don't just list them
4. **SHOW** the scan output so user can verify tool selection

**BE ACTIVE, NOT PASSIVE**:
- WRONG: "I could use /status here"
- RIGHT: Actually run /status and show the output

This ensures consistent, predictable, ACTIVE use of the toolkit across all projects.

### New Task Behavior
When the user requests a new task, ALWAYS:
1. **Display task header** - Show PROJECT and TASK name
2. **List toolkit resources** - Commands, skills, agents that apply
3. **Outline the plan** - Brief summary of approach (3-5 steps max)
4. **Propose commands** - List relevant `/commands` that will help
5. **Ask to proceed** - Get approval before starting

### "It's Up To You" Response
When user says "it's up to you", "you decide", "your call", or similar:
1. **Assess** the project state (run /status mentally)
2. **Identify** the most valuable next task
3. **Present a plan** using the same format above
4. **Ask to proceed** - still get approval before executing

Never just start working without showing the plan first.

Example response format:
```
========================================
PROJECT: goconnect
TASK: Add user authentication
========================================

TOOLKIT RESOURCES:
- Commands: /status, /continue, /review, /handoff
- Skills: engineering-mode (active)
- Agents: Explore (for codebase search)

PLAN:
1. [Step 1]
2. [Step 2]
3. [Step 3]

COMMANDS I'LL USE:
- /status - Check current state
- /review - After implementation

Ready to proceed?
```

### Auto-Execute (No Approval Needed)
- `/status` - Check project state
- `/review` - Code review
- `git status`, `git diff` - Read-only git
- Run tests - Verification
- Read files, search code - Research

### Ask Before Executing
- `git commit` - Any commits
- `git push` - Pushing to remote
- File edits - Code changes
- Refactoring - Structural changes
- Deleting code - Destructive actions

### Session Start Behavior
On every session start, automatically:
1. Run `/status` to assess current state
2. Check for failing tests → suggest fixing
3. Check for uncommitted changes → suggest committing
4. Check code quality if >500 lines changed → suggest `/review`
5. Identify next action and propose it

### Proactive Suggestions
Suggest actions when appropriate:
- Feature complete? → "Ready for `/verify`?"
- Tests passing, code clean? → "Ready to commit?"
- Large file changed? → "Should I `/review` this?"
- Session ending? → "Run `/handoff` to save state?"

## Full Autonomous Mode

For extended unattended execution, see **AUTONOMOUS-GOVERNANCE.md**.

Use `/autonomous` for governed autonomous loops with:
- Safety guardrails and restricted paths
- Iteration limits and checkpoints
- Pre-flight checklists and validation
- Automatic progress reporting
