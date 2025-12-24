#!/bin/bash

# migrate-to-agents.sh - Upgrade to Agent System v2.3
# Adds advanced agent capabilities to existing claude-code-toolkit projects

set -e  # Exit on error

echo "🤖 Migrating to Advanced Agent System v2.3"
echo ""

# Detect toolkit location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLKIT_DIR="${TOOLKIT_DIR:-$SCRIPT_DIR}"

echo "Toolkit location: $TOOLKIT_DIR"
echo "Current directory: $(pwd)"
echo ""

# 1. Backup current setup
echo "📦 Creating backup..."
if [ -d ".claude" ]; then
    cp -r .claude .claude.backup.$(date +%Y%m%d_%H%M%S)
    echo "✓ Backup created at .claude.backup.$(date +%Y%m%d_%H%M%S)"
else
    echo "⚠ No .claude directory found - creating from scratch"
    mkdir -p .claude
fi
echo ""

# 2. Create agent directories
echo "📁 Creating agent directory structure..."
mkdir -p .claude/agents
mkdir -p .claude/domains
echo "✓ Directories created"
echo ""

# 3. Copy agent registry and definitions from toolkit
echo "📋 Installing agent system..."
if [ -f "$TOOLKIT_DIR/agents/registry.json" ]; then
    cp "$TOOLKIT_DIR/agents/registry.json" .claude/agents/
    echo "✓ Agent registry installed"
else
    echo "✗ Error: Agent registry not found at $TOOLKIT_DIR/agents/registry.json"
    exit 1
fi

if [ -d "$TOOLKIT_DIR/agents/definitions" ]; then
    cp -r "$TOOLKIT_DIR/agents/definitions" .claude/agents/
    echo "✓ Agent definitions installed (3 agents)"
else
    echo "✗ Error: Agent definitions not found at $TOOLKIT_DIR/agents/definitions"
    exit 1
fi

if [ -f "$TOOLKIT_DIR/agents/chain-engine.md" ]; then
    cp "$TOOLKIT_DIR/agents/chain-engine.md" .claude/agents/
    echo "✓ Chain engine installed"
fi
echo ""

# 4. Detect domain and configure
echo "🔍 Detecting project domain..."
DOMAIN="general"

# Check for healthcare domain
if [ -f "docs/PRD_v1.md" ] && grep -qi "HIPAA\|healthcare\|PHI\|medical\|patient\|claim" docs/PRD_v1.md 2>/dev/null; then
    echo "Healthcare domain detected (found HIPAA/PHI references in PRD)"
    DOMAIN="healthcare"

    # Copy healthcare domain templates if they exist
    if [ -d "$TOOLKIT_DIR/domains/healthcare" ]; then
        mkdir -p .claude/domains/healthcare
        cp -r "$TOOLKIT_DIR/domains/healthcare/"* .claude/domains/healthcare/ 2>/dev/null || true
        echo "✓ Healthcare compliance templates installed"
    fi

# Check for revenue/finance domain
elif grep -rqi "revenue\|financial\|SOX\|accounting\|fiscal" docs/*.md 2>/dev/null; then
    echo "Revenue/Finance domain detected"
    DOMAIN="revenue"

    if [ -d "$TOOLKIT_DIR/domains/revenue" ]; then
        mkdir -p .claude/domains/revenue
        cp -r "$TOOLKIT_DIR/domains/revenue/"* .claude/domains/revenue/ 2>/dev/null || true
        echo "✓ Revenue compliance templates installed"
    fi
else
    echo "General development domain (no specific compliance requirements detected)"
    DOMAIN="general"
fi
echo ""

# 5. Create domain.json
echo "⚙️  Configuring domain: $DOMAIN"

if [ "$DOMAIN" = "healthcare" ]; then
    cat > .claude/domain.json <<'EOF'
{
  "domain": "healthcare",
  "compliance": ["HIPAA", "CMS"],
  "agents": {
    "enabled": ["healthcare-validator", "test-specialist", "code-reviewer"],
    "auto_trigger": {
      "healthcare-validator": ["prd-check", "build-prd", "verify"],
      "test-specialist": ["tdd", "verify"],
      "code-reviewer": ["review", "verify"]
    }
  },
  "phi_patterns": {
    "enabled": true,
    "custom_patterns": [
      {"name": "MRN", "regex": "\\bMRN[:=\\s]+[\\w-]+\\b"},
      {"name": "ClaimID", "regex": "\\b(CLM|claim)[-_][0-9A-Z]+\\b"}
    ]
  },
  "evidence_chain": {
    "required": true,
    "schema_file": ".claude/domains/healthcare/evidence-schema.json"
  }
}
EOF
elif [ "$DOMAIN" = "revenue" ]; then
    cat > .claude/domain.json <<'EOF'
{
  "domain": "revenue",
  "compliance": ["SOX", "GAAP"],
  "agents": {
    "enabled": ["test-specialist", "code-reviewer"],
    "auto_trigger": {
      "test-specialist": ["tdd", "verify"],
      "code-reviewer": ["review", "verify"]
    }
  },
  "financial_validation": {
    "enabled": true,
    "precision_required": "decimal",
    "audit_trail": "required"
  }
}
EOF
else
    cat > .claude/domain.json <<'EOF'
{
  "domain": "general",
  "agents": {
    "enabled": ["test-specialist", "code-reviewer"],
    "auto_trigger": {
      "test-specialist": ["tdd", "verify"],
      "code-reviewer": ["review", "verify"]
    }
  },
  "quality_gates": {
    "min_test_coverage": 80,
    "max_complexity": 10,
    "security_scan": "enabled"
  }
}
EOF
fi

echo "✓ Domain configuration created (.claude/domain.json)"
echo ""

# 6. Update CLAUDE.md to reference agents
echo "📝 Updating CLAUDE.md..."
if [ -f "CLAUDE.md" ]; then
    if ! grep -q "Agent System" CLAUDE.md; then
        echo "" >> CLAUDE.md
        echo "## Agent System: ENABLED" >> CLAUDE.md
        echo "" >> CLAUDE.md
        echo "**Domain**: $DOMAIN" >> CLAUDE.md
        echo "**Agents**: See [.claude/agents/registry.json](.claude/agents/registry.json)" >> CLAUDE.md
        echo "" >> CLAUDE.md
        echo "### Available Agents:" >> CLAUDE.md
        echo "- **test-specialist**: Test generation, coverage analysis, edge cases" >> CLAUDE.md
        echo "- **code-reviewer**: Security, quality, performance review" >> CLAUDE.md
        if [ "$DOMAIN" = "healthcare" ]; then
            echo "- **healthcare-validator**: HIPAA compliance, PHI detection, evidence chain" >> CLAUDE.md
        fi
        echo "" >> CLAUDE.md
        echo "### Agent Triggers:" >> CLAUDE.md
        echo "- \`/verify\`: Runs full agent chain (tests + quality + compliance)" >> CLAUDE.md
        echo "- \`/review\`: Runs code-reviewer agent" >> CLAUDE.md
        echo "- \`/tdd\`: Runs test-specialist agent" >> CLAUDE.md
        if [ "$DOMAIN" = "healthcare" ]; then
            echo "- \`/prd-check\`: Runs healthcare-validator (compliance check)" >> CLAUDE.md
        fi

        echo "✓ CLAUDE.md updated with agent information"
    else
        echo "ℹ CLAUDE.md already has agent system section"
    fi
else
    echo "⚠ CLAUDE.md not found - skipping update"
fi
echo ""

# 7. Summary
echo "========================================="
echo "✅ Migration complete!"
echo "========================================="
echo ""
echo "Domain: $DOMAIN"
echo "Agents installed:"
echo "  - test-specialist (general)"
echo "  - code-reviewer (general)"
if [ "$DOMAIN" = "healthcare" ]; then
    echo "  - healthcare-validator (healthcare)"
fi
echo ""
echo "Next steps:"
echo "1. Review .claude/domain.json to customize agent behavior"
echo "2. Run /verify to test the agent chain"
if [ "$DOMAIN" = "healthcare" ]; then
    echo "3. Run /prd-check to test healthcare compliance validation"
fi
echo ""
echo "Existing commands will continue to work unchanged."
echo "Agents will automatically enhance /verify, /review, and /tdd commands."
echo ""
echo "For more information, see:"
echo "  - .claude/agents/chain-engine.md (how agents work together)"
echo "  - .claude/agents/definitions/*.md (agent capabilities)"
echo "========================================="
