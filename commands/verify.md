---
description: Verify all passing features actually work
---

<instructions>
Use subagents to thoroughly verify all features marked "passes": true in @features.json.
</instructions>

<agent_integration>
**If Advanced Agent System is installed** (check for `.claude/agents/registry.json`):

<trigger_chain>full-verification</trigger_chain>

<chain_execution>
1. **test-specialist agent**: Validates test coverage and quality
   - Checks all tests are passing
   - Identifies untested code paths
   - Suggests missing edge case tests
   - Reviews test quality (AAA pattern, independence, clarity)

2. **code-reviewer agent**: Reviews code quality and security
   - Security scan (OWASP Top 10, injection attacks)
   - Code quality (complexity, DRY, SOLID)
   - Performance review (N+1 queries, caching)
   - Maintainability assessment

3. **domain agent** (conditional based on `.claude/domain.json`):
   - healthcare-validator (if domain === "healthcare"): HIPAA, PHI, evidence chain
   - finance-validator (if domain === "finance"): SOX, audit trails
   - (Skip if domain === "general")

4. **Merge Results**: Combine all agent reports into unified verification
</chain_execution>

<fallback>
If agent system NOT installed, use basic subagent verification (current behavior).
</fallback>
</agent_integration>

<verification_steps>
For each feature:
1. Run related tests
2. Test end-to-end as a user would
3. Check edge cases
4. Verify acceptance_criteria are actually met
</verification_steps>

<failure_handling>
If anything is broken:
- Set "passes": false in features.json
- Note what's wrong in the feature's "notes" field
- Block feature completion until fixed
</failure_handling>

<output_format>
**With Agent System**:
```
## Verification Report

### Test Coverage (test-specialist)
✓ Line coverage: 87%
✗ Missing tests for error recovery (line 42)
⚠ Edge case: null input not tested

### Code Quality (code-reviewer)
✓ No security vulnerabilities
✗ Function complexity too high (line 78: 12 branches)
⚠ N+1 query detected (getOrders)

### Healthcare Compliance (healthcare-validator) [if applicable]
✓ No PHI in logs
✓ Encryption configured correctly
✗ Evidence chain missing reason codes

### Summary
- CRITICAL: 1 (evidence chain)
- HIGH: 2 (complexity, N+1 query)
- MEDIUM: 2 (edge cases, coverage gaps)
- BLOCKING: YES (cannot mark complete until critical fixed)
```

**Without Agent System**:
```
Feature Verification Report
===========================

Verified: X features
Actually Working: Y
Found Broken: Z

Broken Features:
- F00X: [name] - [what's wrong]
- F00X: [name] - [what's wrong]

Remaining Unverified: A
```
</output_format>
