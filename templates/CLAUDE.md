# Engineering Mode

## Context Management
Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off. Therefore, do not stop tasks early due to token budget concerns. Save progress to memory before context refresh. Be persistent and complete tasks fully.

## Verification Requirements
- NEVER mark a feature as complete without testing it end-to-end
- Run the actual test suite, don't just assume tests pass
- For web apps: use browser automation to test as a real user would
- For APIs: make actual requests, don't just read the code
- If you can't verify something works, say so explicitly

## Engineering Constraints
- Avoid over-engineering. Only make changes that are directly requested or clearly necessary
- Don't create extra files, unnecessary abstractions, or build in flexibility that wasn't requested
- Keep solutions minimal and focused on the actual requirements
- One feature at a time. Fix and verify before moving to the next

## Test/Build Commands
# Customize these for your project:
- Test: npm test
- Lint: npm run lint
- Build: npm run build
- Dev: npm run dev

## Git Workflow
- Commit after each feature passes verification
- Use conventional commits: feat/fix/docs/refactor
- Push after significant milestones

## Feature Tracking
- All features tracked in features.json with "passes": false by default
- Mark "passes": true only after verification
- Update claude-progress.txt after each session

## Autonomous Work Rules
- Work systematically through tasks without stopping for permission on routine operations
- Use subagents to verify details or investigate questions, especially early in tasks
- If blocked or uncertain, investigate first before asking for help
- Track progress in structured formats (JSON for test results, markdown for notes)

## Quality Standards
- Write tests alongside implementation, not as an afterthought
- Handle errors explicitly - don't let them fail silently
- Check edge cases before marking complete
- Review your own code for bugs and security issues before committing

## Communication
- Report what you actually did, not what you planned to do
- Be specific about what works and what doesn't
- If something isn't working, say so clearly rather than working around it
- Update claude-progress.txt after each completed task

## PRD Enforcement

**Product Requirements Document (PRD) Location:**
- Primary: /docs/PRD/[PROJECT]-PRD.md
- Fallback: /docs/REQUIREMENTS.md

**PRD-Aware Commands:**
- `/prd-check` - Verify alignment before work
- `/build-prd` - Build with PRD enforcement
- `/edit-prd` - Edit with PRD validation
- `/design-prd` - Design within PRD constraints

**Rules:**
1. NO code changes without PRD support
2. Quote PRD sections in commits for non-obvious decisions
3. If PRD is unclear, STOP and ask
4. Never invent requirements not in PRD

**Traceability:**
All features in features.json must reference PRD sections:
```json
{
  "id": "F001",
  "prd_section": "3.2.1",
  "prd_requirement": "Description from PRD"
}
```
