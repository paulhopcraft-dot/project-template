# Claude Code Best Practices Toolkit - Existing Project Setup Prompt

Paste this into Claude Code after running `claude` in your existing project folder:

---

I want to set up the Claude Code Best Practices Toolkit for this existing project. Scan the codebase thoroughly and create comprehensive documentation.

## Step 1: Create Directory Structure

Create (if not exists):
- .claude/
- .claude/rules/
- .claude/commands/
- .claude/prompts/
- docs/ (if not exists)

## Step 2: Create Toolkit Files

1. **CLAUDE.md** (root) - with imports to .claude/CLAUDE.md and workspace management note: "When a task is substantial (>2hrs, >5 files, new endpoints, schema changes, high priority), create a branch and prompt user to open new Claude Code window"

2. **.claude/CLAUDE.md** - project instructions with:
   - Workspace management rules
   - Workflow (read code â†’ check domain memory â†’ pick feature â†’ implement â†’ verify â†’ update memory â†’ commit)
   - Verification loop (test, lint, check acceptance criteria)
   - Git discipline (conventional commits, never commit secrets)
   - Context management (/clear between tasks)

3. **.claude/domain_memory.json** - template structure (will populate after scan)

4. **.claude/rules/engineering.md** - code quality, security, testing, logging standards

5. **.claude/commands/** - create all: init.md, continue.md, status.md, scan.md, review.md, branch.md, add-feature.md

6. **.claude/prompts/** - create: coding_agent.md, review_agent.md, branch_manager.md

## Step 3: Deep Repository Scan

Scan everything systematically:

### 3.1 Structure Analysis
```bash
find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.tsx" -o -name "*.jsx" -o -name "*.go" -o -name "*.rs" \) | grep -v node_modules | grep -v __pycache__ | head -100
```

### 3.2 Stack Detection
Read and analyze:
- package.json (dependencies, scripts)
- requirements.txt / pyproject.toml / Pipfile
- Cargo.toml / go.mod
- docker-compose.yml / Dockerfile
- tsconfig.json / eslint config / prettier config

### 3.3 Documentation Inventory
```bash
find . -name "*.md" -not -path "./node_modules/*" | head -30
```
Read all existing .md files completely.

### 3.4 Code Analysis
- Entry points (main.*, index.*, app.*)
- Route definitions (find all endpoints)
- Models/schemas (database entities)
- Services/controllers (business logic)
- Middleware/hooks
- Utils/helpers
- Config files

### 3.5 Test Analysis
- Test file locations
- Test frameworks used
- Coverage configuration
- Which features have tests

### 3.6 Git Analysis
```bash
git log --oneline -30
git branch -a
git remote -v
```

### 3.7 TODO/FIXME Extraction
```bash
grep -rn "TODO\|FIXME\|HACK\|XXX\|BUG" --include="*.py" --include="*.ts" --include="*.js" --include="*.tsx" | head -50
```

### 3.8 Environment Analysis
- .env.example / .env.sample
- Config files
- Required external services

## Step 4: Present Scan Results

Show me:

```
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
ðŸ“Š REPOSITORY SCAN COMPLETE
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

PROJECT: [name]
DESCRIPTION: [inferred from README or code]

STACK:
â”œâ”€â”€ Language: [detected]
â”œâ”€â”€ Frontend: [detected or N/A]
â”œâ”€â”€ Backend: [detected or N/A]
â”œâ”€â”€ Database: [detected or N/A]
â”œâ”€â”€ ORM: [detected or N/A]
â”œâ”€â”€ Auth: [detected or N/A]
â”œâ”€â”€ Testing: [frameworks detected]
â””â”€â”€ CI/CD: [detected or N/A]

STRUCTURE:
â”œâ”€â”€ Source files: [count]
â”œâ”€â”€ Test files: [count]
â”œâ”€â”€ API routes/endpoints: [count]
â”œâ”€â”€ Models/entities: [count]
â”œâ”€â”€ Services: [count]
â””â”€â”€ Documentation files: [count]

EXISTING DOCUMENTATION:
â”œâ”€â”€ README.md: [exists/missing] - [brief assessment]
â”œâ”€â”€ API docs: [exists/missing]
â”œâ”€â”€ Schema docs: [exists/missing]
â”œâ”€â”€ Deployment docs: [exists/missing]
â””â”€â”€ Other: [list any other docs]

INTEGRATIONS DETECTED:
- [list external services found in config/code]

TODOs/FIXMEs FOUND: [count]

Is this accurate? Anything to add or correct?
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
```

Wait for my confirmation before proceeding.

## Step 5: Feature Extraction

Extract features from the codebase:

### Working Features (passes: true)
- Each major route group = feature
- Each core model with CRUD = feature
- Each integration that's wired up = feature
- Features with passing tests = working

### Incomplete Features (passes: false)
- TODOs/FIXMEs = incomplete features
- Partial implementations
- Referenced but not built
- Failing/skipped tests

### Present Features

```
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
ðŸ“‹ FEATURES EXTRACTED
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

WORKING (passes: true):
âœ“ F001: [name] - [evidence: routes, tests, etc.]
âœ“ F002: [name] - [evidence]
...

INCOMPLETE (passes: false):
â—‹ F00X: [name] - [evidence: TODO, partial code, etc.]
â—‹ F00X: [name] - [evidence]
...

NEEDS VERIFICATION:
? F00X: [name] - [unclear status, needs manual check]
...

Should I add these to domain memory?
Any features to add, remove, or rename?
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
```

Wait for my confirmation.

## Step 6: Gap Analysis & Documentation Generation

Identify what documentation is missing and offer to create it:

```
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
ðŸ“ DOCUMENTATION GAP ANALYSIS
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

WILL CREATE (missing):
[ ] docs/DESIGN.md - Architecture documentation
[ ] docs/API.md - API reference
[ ] docs/SCHEMA.md - Data models
[ ] docs/DEPLOYMENT.md - Deployment guide
[ ] docs/TESTING.md - Testing strategy
[ ] docs/RUNBOOK.md - Operations guide

WILL UPDATE (exists but incomplete):
[ ] README.md - [what's missing]

OPTIONAL:
[ ] docs/SECURITY.md - Security documentation
[ ] docs/REQUIREMENTS.md - Business requirements

Which should I create? (all / list numbers / skip)
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
```

For each document I create, I'll base it on what I found in the code:
- DESIGN.md â†’ architecture from actual code structure
- API.md â†’ endpoints from actual routes
- SCHEMA.md â†’ entities from actual models
- DEPLOYMENT.md â†’ from Dockerfile, docker-compose, CI configs
- TESTING.md â†’ from test files and config

## Step 7: Create Stack-Specific Rules

Based on detected stack, create appropriate .claude/rules/:
- typescript.md (if TS detected)
- python.md (if Python detected)
- react.md (if React detected)
- api.md (if API backend)
- database.md (for detected DB)

Rules should match the patterns already in the codebase.

## Step 8: Finalize Domain Memory

Populate .claude/domain_memory.json with:
- Project info from scan
- Detected constraints (stack, integrations)
- All extracted features with correct passes status
- Dependencies between features
- Priorities based on current state

## Step 9: Show Completion Summary

```
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
âœ… RETROFIT COMPLETE
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

TOOLKIT FILES CREATED:
â”œâ”€â”€ CLAUDE.md (root)
â””â”€â”€ .claude/
    â”œâ”€â”€ CLAUDE.md
    â”œâ”€â”€ domain_memory.json
    â”œâ”€â”€ rules/
    â”‚   â”œâ”€â”€ engineering.md
    â”‚   â””â”€â”€ [stack-specific].md
    â”œâ”€â”€ commands/
    â””â”€â”€ prompts/

DOCUMENTATION CREATED:
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ [list created docs]
â”‚   â””â”€â”€ ...

DOMAIN MEMORY:
â”œâ”€â”€ Working features: [X]
â”œâ”€â”€ Incomplete features: [Y]
â””â”€â”€ Total tracked: [X+Y]

NEXT STEPS:
1. Review docs/ for accuracy
2. Check domain_memory.json for any missing features
3. Run /project:continue to start on: F00X [name]

COMMANDS AVAILABLE:
- /project:status - See progress
- /project:continue - Work on next feature
- /project:review - Get improvement suggestions
- /project:branch - Manage branches

Ready to continue development!
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
```
