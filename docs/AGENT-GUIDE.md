# Agent System Guide

Complete guide to understanding and creating custom agents for the Claude Code Toolkit.

## Table of Contents

1. [Overview](#overview)
2. [How Agents Work](#how-agents-work)
3. [Built-In Agents](#built-in-agents)
4. [Creating Custom Agents](#creating-custom-agents)
5. [Agent Chaining](#agent-chaining)
6. [Domain Configuration](#domain-configuration)
7. [Best Practices](#best-practices)
8. [Examples](#examples)

---

## Overview

The Advanced Agent System allows you to create **specialist agents** that provide expert-level analysis in specific domains. Agents can work independently or be chained together for comprehensive validation.

### Why Use Agents?

- **Specialized Expertise**: Each agent is an expert in one area (security, testing, compliance)
- **Consistency**: Agents apply the same standards every time, no variance
- **Scalability**: Add new agents without modifying existing commands
- **Domain-Specific**: Automatically enable compliance agents for regulated industries
- **Composability**: Chain agents together for multi-faceted analysis

### Architecture

```
User runs /verify
    ↓
Command checks for .claude/agents/registry.json
    ↓
IF FOUND: Load "full-verification" chain
    ↓
Execute agents sequentially:
    1. test-specialist → Coverage report
    2. code-reviewer (receives coverage) → Quality report
    3. healthcare-validator (if healthcare domain) → Compliance report
    ↓
Merge all reports → Unified verification output
```

---

## How Agents Work

### Agent Lifecycle

1. **Registration**: Agent defined in `agents/definitions/my-agent.md`
2. **Registry Entry**: Added to `agents/registry.json` with triggers and capabilities
3. **Project Configuration**: Enabled in `.claude/domain.json`
4. **Triggering**: Command checks for agent and spawns it if conditions met
5. **Execution**: Agent runs its workflow, generates report
6. **Output**: Results merged and presented to user

### Agent Components

Every agent consists of:

**Agent Definition File** (`agents/definitions/agent-name.md`):
- XML-structured markdown describing the agent's role, capabilities, and workflow
- Specifies what the agent validates, checks, or generates
- Defines output format

**Registry Entry** (`agents/registry.json`):
```json
{
  "agent-name": {
    "file": "agent-name.md",
    "domain": "general|healthcare|security|etc",
    "triggers": ["verify", "review", "custom-command"],
    "capabilities": ["what-it-does"],
    "enabled_for": ["all"] or ["C:\\path\\to\\project"]
  }
}
```

**Domain Configuration** (`.claude/domain.json` in project):
```json
{
  "domain": "general",
  "agents": {
    "enabled": ["agent-name"],
    "auto_trigger": {
      "agent-name": ["verify", "review"]
    }
  }
}
```

---

## Built-In Agents

### 1. test-specialist

**Purpose**: Comprehensive testing expertise

**Capabilities**:
- Generate unit, integration, and E2E tests using AAA pattern
- Analyze test coverage (line, branch, function coverage)
- Discover edge cases (boundaries, null, empty, errors, async, concurrency)
- Review test quality (clarity, independence, brittleness)

**Triggers**: `/tdd`, `/verify`

**Output Example**:
```
## Test Specialist Report

### Coverage
- Line coverage: 85%
- Branch coverage: 78%
- Untested paths: [processPayment error handler, refundTransaction]

### Edge Cases Added
- Empty array handling
- Null input validation
- Concurrent modification protection

### Recommendations
1. Add tests for error recovery path (line 42)
2. Improve test names for clarity
3. Mock external API in integration tests
```

### 2. code-reviewer

**Purpose**: Senior engineer-level code review

**Capabilities**:
- **Security**: SQL injection, XSS, CSRF, auth vulnerabilities, OWASP Top 10
- **Quality**: DRY, SOLID, design patterns, cyclomatic complexity < 10
- **Performance**: N+1 queries, caching, algorithmic complexity
- **Maintainability**: Naming conventions, documentation, modularity

**Triggers**: `/review`, `/verify`

**Output Example**:
```
## Code Review Report

### Security Issues
🔴 HIGH: SQL injection in user search (line 42)
🟡 MEDIUM: Missing rate limiting on /api/export

### Quality Issues
🟡 MEDIUM: Function too complex (15 branches at line 78)
🟢 LOW: Inconsistent naming (camelCase vs snake_case)

### Performance Issues
🟡 MEDIUM: N+1 query in getOrders (line 124)

### Action Items
1. [CRITICAL] Fix SQL injection before merging
2. [REQUIRED] Add rate limiting
3. [RECOMMENDED] Refactor complex function
```

### 3. healthcare-validator

**Purpose**: HIPAA compliance and healthcare regulations

**Capabilities**:
- **PHI Detection**: Scans for 18 HIPAA PHI identifiers (SSN, MRN, DOB, etc.)
- **HIPAA Validation**: Security Rule (encryption, access controls, audit logging)
- **Evidence Chain**: Verifies immutable audit trail (who, what, when, why, where, how)
- **CMS Requirements**: Claims processing validation

**Triggers**: `/prd-check`, `/build-prd`, `/verify` (only in healthcare domain)

**Output Example**:
```
## Healthcare Compliance Validation

### PHI Exposure Risks
🔴 HIGH: SSN logged in error message (line 56)
🟡 MEDIUM: Patient name in URL parameter (api.js:89)

### HIPAA Compliance Status
✓ Encryption at rest: AES-256
✓ Encryption in transit: TLS 1.3
✗ Audit logging incomplete: Missing READ operations

### Evidence Chain Gaps
- Missing: Reason codes for batch updates
- Missing: Component identification in claims-service

### Recommendations
1. [CRITICAL] Remove PHI from logs
2. [REQUIRED] Complete audit logging
3. [REQUIRED] Add reason codes to evidence chain
```

---

## Creating Custom Agents

### Step 1: Define Your Agent

Create `agents/definitions/my-agent.md`:

```markdown
---
name: my-agent
domain: security
version: 1.0.0
---

<agent_role>
You are a security expert specializing in dependency vulnerability detection.
</agent_role>

<capabilities>
- **Dependency Scanning**: Identify known vulnerabilities in dependencies
- **License Compliance**: Check for incompatible licenses
- **Outdated Packages**: Flag packages with security updates available
- **Supply Chain**: Detect suspicious packages or maintainers
</capabilities>

<workflow>
<step number="1">
**Scan Dependencies**
- Run npm audit / pip-audit / cargo audit
- Check against CVE database
- Identify severity levels
</step>

<step number="2">
**License Review**
- Parse package licenses
- Flag GPL in commercial projects
- Warn about unknown licenses
</step>

<step number="3">
**Supply Chain Analysis**
- Check package age and maintainer reputation
- Flag packages with few downloads or new maintainers
- Detect typosquatting attempts
</step>

<step number="4">
**Report Findings**
```
## Dependency Security Report

### Vulnerabilities
🔴 CRITICAL: lodash 4.17.15 (CVE-2020-8203)
🟡 MEDIUM: axios 0.21.0 (CVE-2020-28168)

### License Issues
⚠️ GPL-3.0: package-foo (incompatible with commercial use)

### Supply Chain Risks
🟢 LOW: new-package (< 6 months old, few downloads)

### Action Items
1. [CRITICAL] Update lodash to 4.17.21
2. [REQUIRED] Replace or relicense package-foo
3. [OPTIONAL] Review new-package maintainer
```
</step>
</workflow>

<integration_points>
- Triggered by: `/security-scan`, `/verify`
- Works with: package.json, requirements.txt, Cargo.toml
- Outputs to: Security report
- Blocks commits if: Critical vulnerabilities found
</integration_points>
```

### Step 2: Register Your Agent

Add to `agents/registry.json`:

```json
{
  "agents": {
    "my-agent": {
      "file": "my-agent.md",
      "domain": "security",
      "triggers": ["security-scan", "verify"],
      "capabilities": ["dependency-scanning", "license-compliance"],
      "enabled_for": ["all"]
    },
    ...existing agents...
  }
}
```

### Step 3: Add to Chains (Optional)

Create or modify chain in `agents/registry.json`:

```json
{
  "chains": {
    "security-verification": {
      "description": "Complete security validation",
      "steps": [
        {"agent": "my-agent", "phase": "dependency-scan"},
        {"agent": "code-reviewer", "phase": "code-security"}
      ]
    }
  }
}
```

### Step 4: Enable in Projects

Add to `.claude/domain.json` in your project:

```json
{
  "domain": "general",
  "agents": {
    "enabled": ["my-agent", "test-specialist", "code-reviewer"],
    "auto_trigger": {
      "my-agent": ["security-scan", "verify"]
    }
  }
}
```

### Step 5: Create Trigger Command (Optional)

Create `.claude/commands/security-scan.md`:

```markdown
---
description: Run comprehensive security scan
---

<instructions>
Scan project for security vulnerabilities and compliance issues.
</instructions>

<agent_integration>
<trigger_agent>my-agent</trigger_agent>

<agent_workflow>
The **my-agent** will scan dependencies, licenses, and supply chain risks.
</agent_workflow>
</agent_integration>
```

---

## Agent Chaining

### Chain Types

**Sequential Chain**: Agents execute one after another
```
Agent A → Output → Agent B → Output → Agent C
```
Use when: Later agents need results from earlier agents

**Parallel Chain**: Agents execute simultaneously
```
Agent A ↘
Agent B → Merge → Final Output
Agent C ↗
```
Use when: Agents are independent and can run concurrently

**Conditional Chain**: Agents execute based on conditions
```
if (domain === 'healthcare') → HealthcareValidator
else if (domain === 'finance') → FinanceValidator
else → GeneralValidator
```
Use when: Domain-specific validation needed

### Defining Chains

In `agents/registry.json`:

```json
{
  "chains": {
    "full-security-audit": {
      "description": "Complete security validation",
      "mode": "sequential",
      "steps": [
        {
          "agent": "my-agent",
          "phase": "dependency-scan"
        },
        {
          "agent": "code-reviewer",
          "phase": "code-security",
          "context": "Focus on security issues from dependency scan"
        },
        {
          "agent": "penetration-tester",
          "phase": "exploit-testing",
          "if": "environment === 'staging'"
        }
      ]
    }
  }
}
```

### Context Passing

Agents in sequential chains can pass context:

```markdown
<!-- In code-reviewer.md -->
<context_handling>
If previous agent (test-specialist) identified untested functions,
focus code review on those functions as they pose higher risk.
</context_handling>
```

---

## Domain Configuration

### Domain Types

- **general**: Standard development (test-specialist, code-reviewer)
- **healthcare**: HIPAA compliance (+ healthcare-validator)
- **finance**: SOX, GAAP compliance (+ finance-validator)
- **security**: Security-focused (+ security-scanner, penetration-tester)

### Example Configurations

**Healthcare Project**:
```json
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
  "quality_gates": {
    "min_test_coverage": 90,
    "max_complexity": 8,
    "phi_scan": "required"
  }
}
```

**Security-Critical Project**:
```json
{
  "domain": "security",
  "agents": {
    "enabled": ["security-scanner", "code-reviewer", "test-specialist"],
    "auto_trigger": {
      "security-scanner": ["verify", "security-scan"],
      "code-reviewer": ["review", "verify"],
      "test-specialist": ["tdd"]
    }
  },
  "quality_gates": {
    "min_test_coverage": 95,
    "security_scan": "required",
    "penetration_test": "staging"
  }
}
```

---

## Best Practices

### Agent Design

1. **Single Responsibility**: Each agent should have one clear purpose
2. **Clear Output Format**: Use consistent report structure
3. **Actionable Findings**: Every issue should have clear remediation
4. **Severity Levels**: Use CRITICAL/HIGH/MEDIUM/LOW consistently
5. **Blocking vs Warning**: Define when agent should block vs warn

### Workflow Design

```markdown
<workflow>
<step number="1">
**Analyze** - Gather information
</step>

<step number="2">
**Validate** - Check against rules/standards
</step>

<step number="3">
**Report** - Generate findings with severity
</step>

<step number="4">
**Recommend** - Provide actionable fixes
</step>
</workflow>
```

### Output Format

```markdown
<step number="4">
**Report Findings**
```
## [Agent Name] Report

### [Category 1]
🔴 CRITICAL: [Issue] ([location])
🟡 MEDIUM: [Issue] ([location])

### [Category 2]
✓ [Good finding]
✗ [Issue to fix]

### Action Items
1. [CRITICAL] [Action required]
2. [REQUIRED] [Action needed]
3. [RECOMMENDED] [Suggestion]
```
</step>
```

### Testing Agents

Before deploying a custom agent:

1. **Manual Test**: Run agent on sample project
2. **Verify Output**: Check report format is clear
3. **Check False Positives**: Ensure rules aren't too strict
4. **Check False Negatives**: Ensure rules catch real issues
5. **Performance**: Agent should complete in < 60 seconds

---

## Examples

### Example 1: Performance Auditor Agent

```markdown
---
name: performance-auditor
domain: performance
version: 1.0.0
---

<agent_role>
You are a performance expert specializing in web application optimization.
</agent_role>

<capabilities>
- **Bundle Analysis**: Identify oversized bundles and imports
- **Database Queries**: Detect N+1 queries and missing indexes
- **Caching**: Find caching opportunities
- **Lazy Loading**: Suggest code splitting and lazy loading
</capabilities>

<workflow>
<step number="1">
**Bundle Analysis**
- Check bundle sizes (main bundle should be < 250KB)
- Identify large dependencies (moment.js, lodash)
- Flag unused imports
</step>

<step number="2">
**Database Performance**
- Scan for N+1 queries (getOrders().map(o => o.getItems()))
- Check for missing indexes on frequently queried fields
- Identify full table scans
</step>

<step number="3">
**Caching Opportunities**
- Flag repeated expensive operations
- Suggest Redis/Memcached for frequently accessed data
- Recommend CDN for static assets
</step>

<step number="4">
**Report Findings**
```
## Performance Audit Report

### Bundle Size
🔴 CRITICAL: Main bundle 450KB (target: 250KB)
  - moment.js: 67KB (use date-fns instead)
  - lodash: 72KB (import specific functions)

### Database Performance
🟡 MEDIUM: N+1 query in getOrders (line 89)
🟢 LOW: Missing index on users.email

### Caching
🟡 MEDIUM: User profile fetched on every request
  - Recommendation: Cache user profiles with 5-minute TTL

### Action Items
1. [CRITICAL] Replace moment.js with date-fns
2. [REQUIRED] Fix N+1 query with JOIN
3. [RECOMMENDED] Add Redis caching for user profiles
```
</step>
</workflow>
</capabilities>
```

### Example 2: Accessibility Auditor Agent

```markdown
---
name: a11y-auditor
domain: frontend
version: 1.0.0
---

<agent_role>
You are an accessibility expert ensuring WCAG 2.1 Level AA compliance.
</agent_role>

<capabilities>
- **Semantic HTML**: Verify proper use of ARIA labels and semantic tags
- **Keyboard Navigation**: Check tab order and focus management
- **Color Contrast**: Validate WCAG contrast ratios (4.5:1 normal, 3:1 large text)
- **Screen Reader**: Ensure screen reader compatibility
</capabilities>

<workflow>
<step number="1">
**Semantic HTML Review**
- Check for proper heading hierarchy (h1 → h2 → h3)
- Verify ARIA labels on interactive elements
- Ensure form inputs have associated labels
</step>

<step number="2">
**Keyboard Navigation**
- Verify tab order is logical
- Check for keyboard traps
- Ensure all interactive elements are keyboard accessible
</step>

<step number="3">
**Color Contrast**
- Calculate contrast ratios for text/background combinations
- Flag insufficient contrast (<4.5:1)
- Check focus indicators are visible
</step>

<step number="4">
**Report Findings**
```
## Accessibility Audit Report (WCAG 2.1 Level AA)

### Semantic HTML
🔴 CRITICAL: Missing h1 on homepage
🟡 MEDIUM: Button missing aria-label (LoginButton.tsx:42)

### Keyboard Navigation
✓ Tab order is logical
✗ Modal traps focus (Modal.tsx:67)

### Color Contrast
🔴 CRITICAL: Contrast ratio 2.8:1 (requires 4.5:1)
  - Primary button text on background

### Action Items
1. [CRITICAL] Add h1 to homepage
2. [CRITICAL] Fix button contrast ratio
3. [REQUIRED] Fix modal focus trap
4. [RECOMMENDED] Add aria-label to all buttons
```
</step>
</workflow>
```

---

## Migration & Deployment

### Adding Agents to Existing Projects

```bash
# Copy agent definitions from toolkit
cp -r /path/to/toolkit/agents .claude/

# Create domain.json
cat > .claude/domain.json <<EOF
{
  "domain": "general",
  "agents": {
    "enabled": ["test-specialist", "code-reviewer"],
    "auto_trigger": {
      "test-specialist": ["tdd", "verify"],
      "code-reviewer": ["review", "verify"]
    }
  }
}
EOF
```

Or use the migration script:

```bash
cd your-project
bash /path/to/toolkit/migrate-to-agents.sh
```

### Verifying Agent Installation

```bash
# Check agent registry exists
test -f .claude/agents/registry.json && echo "✓ Registry installed"

# Check domain config
test -f .claude/domain.json && echo "✓ Domain configured"

# List enabled agents
cat .claude/domain.json | grep -A 5 "enabled"
```

---

## Troubleshooting

### Agent Not Triggering

**Check**:
1. Does `.claude/agents/registry.json` exist?
2. Is agent listed in registry?
3. Is agent enabled in `.claude/domain.json`?
4. Does command include `<agent_integration>` block?
5. Are conditions met (e.g., domain === 'healthcare')?

### Agent Producing No Output

**Check**:
1. Is agent definition file in `agents/definitions/`?
2. Is workflow section properly structured with XML?
3. Are there syntax errors in agent definition?

### Chain Not Executing

**Check**:
1. Is chain defined in `agents/registry.json` under `chains`?
2. Are all agents in chain enabled in domain.json?
3. Is command triggering the chain (e.g., `/verify` → `full-verification`)?

---

## Further Reading

- [Chain Engine Documentation](../agents/chain-engine.md)
- [Agent Definitions](../agents/definitions/)
- [CHANGELOG.md](../CHANGELOG.md) - v2.3 release notes
- [Healthcare Compliance Checklist](../agents/domains/healthcare/compliance-checklist.md)

---

**Created**: 2025-12-25
**Version**: 2.3.0
**License**: MIT
