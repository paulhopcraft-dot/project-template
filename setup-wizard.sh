#!/bin/bash
# Claude Code Setup Wizard - Interactive guided setup
# Just answer yes/no questions, everything happens automatically

set -e

# Get toolkit directory (where this script lives)
TOOLKIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔════════════════════════════════════════╗"
echo "║   Claude Code Setup Wizard             ║"
echo "║   Answer questions, I'll do the rest   ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "Toolkit location: $TOOLKIT_DIR"
echo ""

# Helper functions
ask_yes_no() {
    while true; do
        read -p "$1 (y/n): " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "Please answer y or n.";;
        esac
    done
}

# Detect stack
detect_stack() {
    if [ -f "package.json" ]; then
        if grep -q "typescript" package.json 2>/dev/null; then
            STACK="typescript"
            TEST_CMD="npm test"
            LINT_CMD="npm run lint"
            BUILD_CMD="npm run build"
            DEV_CMD="npm run dev"
        else
            STACK="javascript"
            TEST_CMD="npm test"
            LINT_CMD="npm run lint"
            BUILD_CMD="npm run build"
            DEV_CMD="npm run dev"
        fi
    elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
        STACK="python"
        TEST_CMD="pytest"
        LINT_CMD="ruff check ."
        BUILD_CMD="python -m build"
        DEV_CMD="python main.py"
    elif [ -f "Cargo.toml" ]; then
        STACK="rust"
        TEST_CMD="cargo test"
        LINT_CMD="cargo clippy"
        BUILD_CMD="cargo build --release"
        DEV_CMD="cargo run"
    elif [ -f "go.mod" ]; then
        STACK="go"
        TEST_CMD="go test ./..."
        LINT_CMD="golangci-lint run"
        BUILD_CMD="go build"
        DEV_CMD="go run ."
    else
        STACK="unknown"
        TEST_CMD="echo 'Add your test command'"
        LINT_CMD="echo 'Add your lint command'"
        BUILD_CMD="echo 'Add your build command'"
        DEV_CMD="echo 'Add your dev command'"
    fi
}

# Step 1: Check if existing project
echo "═══════════════════════════════════════"
echo "Step 1: Project Type"
echo "═══════════════════════════════════════"
echo ""

# Check for code files (not just spec docs)
CODE_EXISTS=$(find . -maxdepth 3 -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" -o -name "*.rs" 2>/dev/null | head -1)

if [ -n "$CODE_EXISTS" ]; then
    echo "📁 Found existing code files."
    MODE="existing"
    detect_stack
    echo "   Detected stack: $STACK"
elif [ "$(ls -A . 2>/dev/null)" ]; then
    echo "📋 Found files but no code - assuming spec-ready project."
    MODE="spec-ready"
else
    echo "📂 Empty folder - spec-ready project setup."
    MODE="spec-ready"
fi
echo ""

# Step 2: Create directory structure
echo "═══════════════════════════════════════"
echo "Step 2: Creating Structure"
echo "═══════════════════════════════════════"
echo ""

mkdir -p .claude/commands
echo "✓ Created .claude/commands/"

# Step 3: Create CLAUDE.md
echo "📝 Creating CLAUDE.md..."
cat > CLAUDE.md << CLAUDE_EOF
# Engineering Mode

## Context Management
Your context window will be automatically compacted as it approaches its limit. Save progress to memory before context refresh. Be persistent and complete tasks fully.

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
- Test: $TEST_CMD
- Lint: $LINT_CMD
- Build: $BUILD_CMD
- Dev: $DEV_CMD

## Git Workflow
- Commit after each feature passes verification
- Use conventional commits: feat/fix/docs/refactor
- Push after significant milestones

## Feature Tracking
- Track features in features.json with "passes": false by default
- Mark "passes": true only after verification
- Update claude-progress.txt after each session
CLAUDE_EOF
echo "✓ Created CLAUDE.md"

# Step 4: Create features.json
if [ ! -f "features.json" ]; then
    echo "📝 Creating features.json..."
    cat > features.json << 'FEATURES_EOF'
{
  "metadata": {
    "project_name": "",
    "created_at": "",
    "last_updated": "",
    "total_features": 0,
    "completed": 0
  },
  "features": [],
  "completed_features": []
}
FEATURES_EOF
    echo "✓ Created features.json"
fi

# Step 5: Create claude-progress.txt
if [ ! -f "claude-progress.txt" ]; then
    echo "📝 Creating claude-progress.txt..."
    cat > claude-progress.txt << PROGRESS_EOF
# Claude Progress Log

## Session 1 - $(date +%Y-%m-%d)
- Project setup with Claude Code toolkit
- Next: Run /project:init-project (new) or /project:continue (existing)
PROGRESS_EOF
    echo "✓ Created claude-progress.txt"
fi

# Step 6: Copy all slash commands from toolkit
echo "═══════════════════════════════════════"
echo "Step 6: Installing Slash Commands"
echo "═══════════════════════════════════════"
echo ""

if [ -d "$TOOLKIT_DIR/commands" ]; then
    echo "📝 Copying all 29 slash commands..."
    cp -r "$TOOLKIT_DIR/commands/"*.md .claude/commands/
    COMMAND_COUNT=$(ls -1 .claude/commands/*.md 2>/dev/null | wc -l)
    echo "✓ Installed $COMMAND_COUNT slash commands"
else
    echo "⚠️  Warning: Toolkit commands directory not found"
    echo "   Creating basic commands as fallback..."
    # Fallback to basic commands if toolkit not found
    cat > .claude/commands/continue.md << 'CMD_EOF'
---
description: Continue working on next feature
---

1. Read @features.json and @claude-progress.txt
2. Find next "passes": false feature
3. Implement with tests
4. Verify end-to-end
5. Update features.json ("passes": true)
6. Commit with conventional message
7. Update claude-progress.txt

$ARGUMENTS
CMD_EOF
    echo "✓ Created basic commands"
fi
echo ""

# Step 7: Copy skills from toolkit
echo "═══════════════════════════════════════"
echo "Step 7: Installing Skills"
echo "═══════════════════════════════════════"
echo ""

if [ -d "$TOOLKIT_DIR/skills" ]; then
    echo "📝 Installing Claude Code skills..."
    mkdir -p .claude/skills
    cp -r "$TOOLKIT_DIR/skills/"* .claude/skills/
    SKILL_COUNT=$(ls -1d .claude/skills/*/ 2>/dev/null | wc -l)
    echo "✓ Installed $SKILL_COUNT skills (engineering-mode, frontend-design)"
else
    echo "⚠️  Warning: Toolkit skills directory not found"
fi
echo ""

# Step 8: Create spec.md template (new projects only)
if [ "$MODE" = "new" ] && [ ! -f "spec.md" ]; then
    echo "📝 Creating spec.md template..."
    cat > spec.md << 'SPEC_EOF'
# Project Specification

## Overview
[What are you building? One paragraph description]

## Core Features
1. Feature 1
2. Feature 2
3. Feature 3

## Technical Requirements
- Language/Framework:
- Database:
- External APIs:
- Deployment target:

## Success Criteria
- What does "done" look like?
SPEC_EOF
    echo "✓ Created spec.md"
fi

# Step 9: Copy .gitignore if available
if [ ! -f ".gitignore" ] && [ -f "$TOOLKIT_DIR/templates/.gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cp "$TOOLKIT_DIR/templates/.gitignore" .gitignore
    echo "✓ Created .gitignore"
fi

# Step 10: Git init if needed
echo ""
if [ ! -d ".git" ]; then
    if ask_yes_no "Initialize git repository?"; then
        git init
        echo "✓ Initialized git"
    fi
fi

# Done
echo ""
echo "╔════════════════════════════════════════╗"
echo "║   ✅ Setup Complete!                   ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "Next steps:"
if [ "$MODE" = "spec-ready" ]; then
    echo "   1. Ensure your spec files are here (DESIGN.md, features.json, etc.)"
    echo "   2. claude --dangerously-skip-permissions"
    echo "   3. /project:continue"
else
    echo "   1. claude --dangerously-skip-permissions"
    echo "   2. /project:continue"
fi
echo ""
