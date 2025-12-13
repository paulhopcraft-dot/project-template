# Claude Code Best Practices Toolkit - Spec-Ready Project Setup

**Use this prompt in Browser Claude (Opus) to generate specs, then take them to Claude Code (Sonnet) to build.**

Paste this into Browser Claude when you have a project idea:

---

I want to set up the Claude Code Best Practices Toolkit for a brand new project with comprehensive documentation that an engineer could build from without asking questions.

## Step 1: Create Directory Structure

Create:
- .claude/
- .claude/rules/
- .claude/commands/
- .claude/prompts/
- docs/
- tests/

## Step 2: Create Toolkit Files

1. **CLAUDE.md** (root) - with imports to .claude/CLAUDE.md and workspace management note: "When a task is substantial (>2hrs, >5 files, new endpoints, schema changes, high priority), create a branch and prompt user to open new Claude Code window"

2. **.claude/CLAUDE.md** - project instructions with:
   - Workspace management rules
   - Workflow (read code â†’ check domain memory â†’ pick feature â†’ implement â†’ verify â†’ update memory â†’ commit)
   - Verification loop (test, lint, check acceptance criteria)
   - Git discipline (conventional commits, never commit secrets)
   - Context management (/clear between tasks)

3. **.claude/domain_memory.json** - template with:
   - project: {name, description, created_at, last_updated}
   - constraints: {stack, integrations, security, compliance}
   - features: [] (with id, name, description, acceptance_criteria, dependencies, passes: false, priority, branch, blockers, notes, last_updated)
   - completed_features: []
   - active_branches: []
   - session_log: []
   - reviews: []

4. **.claude/rules/engineering.md** - code quality, security, testing, logging standards

5. **.claude/commands/** - create all these:
   - init.md, init-new.md, init-existing.md
   - continue.md (pick next feature, implement, update memory)
   - status.md (show progress, blockers, next up)
   - scan.md (scan repo, update memory)
   - review.md (code review, suggest improvements)
   - branch.md (manage feature branches)
   - add-feature.md (add feature to memory)

6. **.claude/prompts/** - create all these:
   - coding_agent.md (autonomous feature implementation with branch decision logic)
   - review_agent.md (automated feedback every 3 features, categorize: quick wins / medium / strategic)
   - branch_manager.md (create branches, prompt for new window, merge workflow)

## Step 3: Ask Discovery Questions

Ask me these ONE AT A TIME, wait for each answer:

1. **Problem & Users**: "What problem are you solving? Who are the users? What pain points does this address?"

2. **Domain**: "What domain is this? (healthcare, finance, operations, e-commerce, education, developer tools, other)"

3. **Project Type**: "What type of project? (API backend, full-stack web app, mobile app, CLI tool, data pipeline, library/SDK)"

4. **Stack**: "Do you have stack preferences or use defaults? I'll ask about each layer if you have preferences."
   - Frontend framework
   - Backend framework
   - Database
   - Auth solution
   - Hosting/deployment

5. **Integrations**: "What external services need to integrate? (payments, email, auth, storage, calendar, CRM, analytics, other)"

6. **Security & Compliance**: "Any security or compliance requirements? (multi-tenant, PII/PHI handling, HIPAA, SOC2, GDPR, audit logs, encryption at rest)"

7. **Non-Functional Requirements**: "Any performance, scale, or operational requirements? (real-time, offline support, expected users, uptime requirements)"

8. **Features**: "List the main features in priority order. I'll figure out dependencies and break them into trackable units."

## Step 4: Generate Complete Documentation

Based on my answers, create ALL of these documents:

### README.md
- Project name and one-line description
- Problem statement and target users
- Tech stack with versions
- Architecture overview (high-level diagram in mermaid)
- Getting started (prerequisites, installation, running locally)
- Project structure explanation
- Environment variables reference
- Available scripts/commands
- Contributing guidelines
- License

### docs/DESIGN.md
- Overview and goals
- Non-goals (what this project explicitly doesn't do)
- Architecture diagram (mermaid)
- Component breakdown with responsibilities
- Data flow description
- Key design decisions with rationale
- Trade-offs made and why
- Future considerations

### docs/REQUIREMENTS.md
- Business requirements (what the product must do)
- User stories for each feature
- Acceptance criteria for each story
- Out of scope items
- Assumptions
- Dependencies on external systems

### docs/API.md (if applicable)
- Base URL and versioning strategy
- Authentication method and flow
- Authorization model (roles, permissions)
- Common headers
- Error response format with codes
- Rate limiting
- Each endpoint grouped by resource:
  - Method, path, description
  - Request body schema
  - Response schema
  - Example request/response
  - Error cases

### docs/SCHEMA.md
- Entity relationship diagram (mermaid)
- Each entity with:
  - Fields, types, constraints
  - Relationships
  - Indexes
  - Validation rules
- Migration strategy
- Seed data requirements

### docs/DEPLOYMENT.md
- Environment types (local, staging, production)
- Infrastructure requirements
- Deployment process step-by-step
- Environment variables by environment
- Database setup and migrations
- CI/CD pipeline configuration
- Rollback procedures
- Health checks and monitoring
- Scaling considerations

### docs/TESTING.md
- Testing strategy (unit, integration, e2e)
- Test file organization
- How to run tests
- Coverage requirements
- Mocking strategy
- Test data management
- CI integration
- Performance testing approach (if applicable)

### docs/SECURITY.md (if PII/compliance involved)
- Data classification
- Encryption approach (at rest, in transit)
- Authentication flow details
- Authorization matrix
- Audit logging requirements
- Compliance checklist
- Incident response basics
- Security review checklist

### docs/RUNBOOK.md
- Common operations
- Troubleshooting guide
- Log locations and interpretation
- Monitoring dashboards
- Alert response procedures
- Backup and restore
- Emergency contacts/escalation

### .env.example
- Every required environment variable
- Grouped by service (app, database, auth, integrations)
- Comments explaining each variable
- Example values (non-sensitive)

### .gitignore
- Standard ignores for the stack
- Environment files
- IDE files
- Build outputs
- CLAUDE.local.md

### Stack-specific rules in .claude/rules/
- Create rules matching the chosen stack
- TypeScript rules if using TS
- Python rules if using Python
- React rules if using React
- API rules if building API
- Database rules for chosen DB

### domain_memory.json
- Populate project info from answers
- Add all constraints (stack, integrations, security, compliance)
- Add all features with:
  - Unique IDs (F001, F002, etc.)
  - Clear descriptions
  - Acceptance criteria (specific, testable)
  - Dependencies between features
  - Priority (high/medium/low)
  - All set to passes: false

## Step 5: Show Summary

After creating everything, show me:

```
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
âœ… PROJECT INITIALIZED
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

Created:
â”œâ”€â”€ README.md
â”œâ”€â”€ CLAUDE.md
â”œâ”€â”€ .env.example
â”œâ”€â”€ .gitignore
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ DESIGN.md
â”‚   â”œâ”€â”€ REQUIREMENTS.md
â”‚   â”œâ”€â”€ API.md
â”‚   â”œâ”€â”€ SCHEMA.md
â”‚   â”œâ”€â”€ DEPLOYMENT.md
â”‚   â”œâ”€â”€ TESTING.md
â”‚   â”œâ”€â”€ SECURITY.md (if applicable)
â”‚   â””â”€â”€ RUNBOOK.md
â”œâ”€â”€ tests/
â””â”€â”€ .claude/
    â”œâ”€â”€ CLAUDE.md
    â”œâ”€â”€ domain_memory.json ([X] features)
    â”œâ”€â”€ rules/
    â”œâ”€â”€ commands/
    â””â”€â”€ prompts/

FEATURES ([X] total):
1. F001: [name] - priority: high - [dependencies]
2. F002: [name] - priority: high - [dependencies]
...

RECOMMENDED BUILD ORDER:
1. F00X: [name] (no dependencies, foundation)
2. F00X: [name] (depends on F00X)
...

Ready to start? Use /project:continue
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
```

Now ask me the first question to get started.
