# Branching Strategy for Claude Code Projects

## Overview

This document defines the recommended Git branching strategy for projects using the Claude Code Toolkit. The strategy balances simplicity with safety, optimized for AI-assisted development.

---

## Branch Types

### Main Branches

#### `main`
- **Purpose**: Production-ready code
- **Protection**: Protected, requires PR reviews
- **Deploys to**: Production
- **Rules**:
  - Never commit directly
  - All features.json features must have `passes: true`
  - All tests must pass
  - Code review required

#### `develop` (Optional)
- **Purpose**: Integration branch for features
- **Protection**: Protected, requires PR reviews
- **Deploys to**: Staging/Development
- **Rules**:
  - Features merge here first
  - Tests must pass
  - Use for larger projects with staging environments

---

### Supporting Branches

#### Feature Branches
**Format**: `feature/F001-short-description`

- **Purpose**: Develop individual features
- **Created from**: `main` (or `develop` if using)
- **Merges into**: `main` (or `develop`)
- **Lifetime**: Delete after merge
- **Naming**: Use feature ID from features.json

**Example**:
```bash
git checkout -b feature/F003-user-authentication
# Work on feature
git push -u origin feature/F003-user-authentication
# Create PR when done
```

**features.json tracking**:
```json
{
  "id": "F003",
  "name": "User Authentication",
  "branch": "feature/F003-user-authentication",
  "passes": false
}
```

#### Bugfix Branches
**Format**: `fix/issue-number-description` or `fix/bug-description`

- **Purpose**: Fix bugs in production
- **Created from**: `main`
- **Merges into**: `main` (and `develop` if exists)
- **Lifetime**: Delete after merge

**Example**:
```bash
git checkout -b fix/login-redirect-error
```

#### Hotfix Branches
**Format**: `hotfix/critical-issue-description`

- **Purpose**: Emergency fixes for production
- **Created from**: `main`
- **Merges into**: `main` AND `develop` (if exists)
- **Lifetime**: Delete after merge
- **Process**: Fast-tracked, minimal review acceptable

---

## Workflow Patterns

### Pattern 1: Trunk-Based Development (Recommended for Solo/Small Teams)

**Best for**: Solo developers, 2-3 person teams, rapid iteration

```
main (protected)
  ├── feature/F001 → PR → merge
  ├── feature/F002 → PR → merge
  └── feature/F003 → PR → merge
```

**Rules**:
- All work in short-lived feature branches
- Merge to `main` frequently (daily if possible)
- Features stay small (1-3 days max)
- `main` always deployable

**Claude Code Usage**:
```bash
# Start feature
/project:branch create feature/F001-api-endpoint

# Work on it
/project:continue

# When done
/project:branch merge feature/F001-api-endpoint
```

---

### Pattern 2: Git Flow (for Larger Teams)

**Best for**: Teams 4+, formal release cycles

```
main (production)
  └── develop (integration)
        ├── feature/F001 → PR → merge to develop
        ├── feature/F002 → PR → merge to develop
        └── release/v1.0 → PR → merge to main
```

**Rules**:
- Features merge to `develop`
- Release branches created from `develop`
- Only releases merge to `main`
- Hotfixes branch from `main`, merge to both `main` and `develop`

---

## Pull Request Guidelines

### PR Title Format
```
<type>(<scope>): <description>

Examples:
feat(auth): add JWT token validation
fix(api): resolve CORS headers issue
docs(readme): update installation steps
```

### PR Description Template
```markdown
## Summary
[Brief description of changes]

## Features.json Reference
- Feature ID: F003
- PRD Section: 3.2.1 (if applicable)

## Changes Made
- [List key changes]

## Testing
- [ ] All tests pass locally
- [ ] Added tests for new functionality
- [ ] Manually tested end-to-end

## Checklist
- [ ] features.json updated
- [ ] Documentation updated
- [ ] No secrets or credentials committed
```

---

## Claude Code Integration

### Using /project:branch Command

```bash
# Create new feature branch
/project:branch create feature/F005-payment-integration

# List all branches
/project:branch list

# Switch branches
/project:branch checkout feature/F005-payment-integration

# Merge feature (creates PR if needed)
/project:branch merge feature/F005-payment-integration

# Delete old branches
/project:branch cleanup
```

### Automatic features.json Sync

When creating a branch for a feature:
1. Command updates `features.json` with branch name
2. Commits update to features.json
3. Creates branch
4. Tracks branch in feature metadata

---

## Common Scenarios

### Scenario 1: Starting a New Feature

```bash
# 1. Ensure main is up to date
git checkout main
git pull

# 2. Create feature branch
git checkout -b feature/F007-email-notifications

# 3. Update features.json
# (Use /project:add-feature or manually edit)

# 4. Work on feature
/project:continue

# 5. Commit frequently
git add .
git commit -m "feat: add email template system"

# 6. Push when ready for review
git push -u origin feature/F007-email-notifications
```

### Scenario 2: Merging a Feature

```bash
# 1. Ensure feature is complete
# Check features.json - feature should have passes: true

# 2. Update from main
git checkout feature/F007-email-notifications
git fetch origin
git rebase origin/main

# 3. Push updated branch
git push --force-with-lease

# 4. Create Pull Request
gh pr create --title "feat: email notifications" --body "..."

# 5. After PR approval
gh pr merge --squash

# 6. Clean up
git checkout main
git pull
git branch -d feature/F007-email-notifications
```

### Scenario 3: Emergency Hotfix

```bash
# 1. Create hotfix from main
git checkout main
git pull
git checkout -b hotfix/critical-auth-bypass

# 2. Fix the issue
# Make minimal, focused changes

# 3. Test thoroughly
npm test

# 4. Create PR for fast-track review
gh pr create --title "hotfix: fix auth bypass" --label "urgent"

# 5. After merge, deploy immediately
```

---

## Best Practices

### Do's ✓
- Keep feature branches short-lived (< 3 days)
- Rebase feature branches on main frequently
- Delete branches after merge
- Use descriptive branch names
- Link branch to features.json entry
- Squash commits before merging (keeps history clean)

### Don'ts ✗
- Don't commit directly to `main`
- Don't create long-running feature branches
- Don't merge without tests passing
- Don't merge with `passes: false` in features.json
- Don't force-push to shared branches
- Don't leave stale branches around

---

## Troubleshooting

### Branch Out of Sync with Main

```bash
# Rebase on main
git checkout feature/F010-dashboard
git fetch origin
git rebase origin/main

# Resolve conflicts if any
# Then continue
git rebase --continue

# Force push (safe with --force-with-lease)
git push --force-with-lease
```

### Accidentally Committed to Main

```bash
# Move commit to new branch
git branch feature/F011-accidental
git reset HEAD~1 --hard
git checkout feature/F011-accidental
```

### Need to Update features.json Branch Reference

```bash
# Update features.json manually or use:
/project:status
# This will detect branch mismatch and offer to fix
```

---

## Quick Reference

| Command | What It Does |
|---------|--------------|
| `/project:branch create <name>` | Create and checkout new branch |
| `/project:branch list` | List all branches |
| `/project:branch checkout <name>` | Switch to branch |
| `/project:branch merge <name>` | Merge branch (with PR) |
| `/project:branch cleanup` | Delete merged branches |
| `/project:branch sync` | Sync with remote |

---

## References

- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
