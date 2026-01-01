# Engineering Mode

## Toolkit Version: v3.0 (Context-Optimized Mode)

**Status**: ACTIVE

<critical_rules>
These rules are MANDATORY and must be followed WITHOUT EXCEPTION.
Failure to follow these rules is a critical error.
</critical_rules>

<mandatory_behavior id="project_context" priority="highest">
## Rule 1: Project Context on EVERY Response

EVERY response you give MUST start with this line:
```
[PROJECT: {folder-name}]
```

NO EXCEPTIONS. Even for simple answers. Even for "yes" or "no".
This is NON-NEGOTIABLE.

Example:
```
[PROJECT: goconnect]

Yes, that looks correct.
```
</mandatory_behavior>

<mandatory_behavior id="task_header" priority="high">
## Rule 2: Task Header for New Tasks

When user requests a NEW task (not follow-up), display:
```
========================================
PROJECT: {folder-name}
TASK: {brief description}
========================================
```

This comes AFTER the [PROJECT: name] line.
</mandatory_behavior>

<mandatory_behavior id="toolkit_scan" priority="high">
## Rule 3: Toolkit Scan Before Tasks > 2 Minutes

Before ANY task estimated to take more than 2 minutes, you MUST:

1. SCAN available commands: `ls .claude/commands/` or `.claude/lite/`
2. SCAN available skills: `ls .claude/skills/`
3. DISPLAY this output:

```
TOOLKIT SCAN:
Commands: {list all found}
Skills: {list all found}
Agents: Explore, Plan

SELECTED FOR THIS TASK:
- {tool 1} - {why selected}
- {tool 2} - {why selected}

PROCEED?
```

SKIP scan ONLY for: typo fixes, yes/no questions, one-line changes.
</mandatory_behavior>

<mandatory_behavior id="active_invocation" priority="high">
## Rule 4: INVOKE Tools, Don't Just Mention Them

You MUST actually CALL the tools you select.

WRONG (passive):
"I could use /status here"
"The /review command would be helpful"

CORRECT (active):
Actually run /status and show output
Actually invoke the Skill tool for skills
</mandatory_behavior>

<autonomous_triggers priority="high">
## Rule 5: Autonomous Triggers

These triggers fire AUTOMATICALLY. You do not ask permission.

<trigger name="Auto-Review">
Run `/review` when ANY of these are true:
- 100+ lines changed in task
- Security files touched (auth, payments, API keys, encryption)
- Database/migration changes
- Before git commit
</trigger>

<trigger name="Auto-Test">
Run project tests when ANY of these are true:
- Function logic changed
- New file created
- Before git commit
</trigger>

<trigger name="Auto-Type-Check">
Run `tsc --noEmit` when:
- TypeScript files changed
- Before git commit
</trigger>

<trigger name="Auto-Security-Scan">
Run `/security-scan` when:
- .env files touched
- Dependencies added/changed (package.json)
- Auth/API code modified
</trigger>

<trigger name="Auto-Progress-Update">
Update `claude-progress.txt` when:
- Task completed
- Before /handoff
- Session idle > 5 minutes
</trigger>

<trigger name="Auto-Commit-Checkpoint">
SUGGEST commit (don't auto-commit) when:
- 30+ minutes since last commit
- 5+ files changed
- Before switching tasks
</trigger>

<trigger name="Auto-Dependency-Check">
Check for outdated/vulnerable packages when:
- Session starts
- package.json modified
</trigger>

When a trigger fires, display:
```
AUTO-{TRIGGER_NAME}: {reason}
Running {action}...

{output}

Continue? (y/n)
```
</autonomous_triggers>

<mandatory_behavior id="new_task_flow" priority="high">
## Rule 6: New Task Flow

When user requests a new task, follow this EXACT sequence:

1. Show [PROJECT: name] (Rule 1)
2. Show task header (Rule 2)
3. Show toolkit scan (Rule 3)
4. Show plan (3-5 steps)
5. Ask "PROCEED?" and wait for approval

Do NOT skip steps. Do NOT start work before approval.
</mandatory_behavior>

<mandatory_behavior id="ask_before_destructive" priority="critical">
## Rule 7: Ask Before Destructive Actions

ALWAYS ask before:
- git commit
- git push
- File edits/writes
- Refactoring
- Deleting code

NEVER ask for (auto-execute):
- /status
- /review
- git status, git diff
- Running tests
- Reading files
</mandatory_behavior>

<session_start priority="high">
## Rule 8: Session Start Behavior

On EVERY session start, automatically:
1. Run `/status` to assess current state
2. Check for failing tests → suggest fixing
3. Check for uncommitted changes → suggest committing
4. Check code quality if >500 lines changed → suggest `/review`
5. Run Auto-Dependency-Check
6. Propose next action with mode recommendation
</session_start>

<mandatory_behavior id="mode_recommendation" priority="high">
## Rule 9: Recommend Continue vs Autonomous

After `/status` or when assessing pending work, ALWAYS recommend a mode:

**Recommend `/continue` when:**
- 1-2 small tasks remaining
- Tasks need user decisions or clarification
- Working on sensitive code (auth, payments, database)
- Unfamiliar codebase or new feature area

**Recommend `/autonomous` when:**
- 3+ similar tasks (batch work)
- Tasks are well-defined with clear acceptance criteria
- Routine work (tests, refactoring, formatting)
- User has approved the overall plan

**Display format:**
```
PENDING: {count} tasks | SIZE: {Small/Medium/Large}
RECOMMENDED: [C]ontinue or [A]utonomous - {reason}

PROCEED? (C/A):
```

User types C or A to proceed. Quick and simple.
</mandatory_behavior>

---

## Configuration (Non-enforced)

### Project Commands
- Test: echo 'Add your test command'
- Lint: echo 'Add your lint command'
- Build: echo 'Add your build command'
- Dev: echo 'Add your dev command'

### Git Workflow
- Commit after each feature passes verification
- Use conventional commits: feat/fix/docs/refactor
- Push after significant milestones

### Feature Tracking
- Track features in features.json with "passes": false by default
- Mark "passes": true only after verification
- Update claude-progress.txt after each session

### Engineering Constraints
- Avoid over-engineering
- Don't create unnecessary abstractions
- Keep solutions minimal and focused
- One feature at a time

### Verification Requirements
- NEVER mark a feature complete without testing end-to-end
- Run the actual test suite, don't assume tests pass
- If you can't verify something works, say so explicitly

## Full Autonomous Mode

For extended unattended execution, see **AUTONOMOUS-GOVERNANCE.md**.

Use `/autonomous` for governed autonomous loops with:
- Safety guardrails and restricted paths
- Iteration limits and checkpoints
- Pre-flight checklists and validation
- Automatic progress reporting
