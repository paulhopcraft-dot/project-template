---
name: improve-prompt
description: Meta-prompt to automatically improve failing prompts based on examples
usage: /improve-prompt <command|agent> --failures=<path>
category: meta
version: 1.0.0
---

<command_role>
Use meta-prompting to analyze failures and generate improved versions of prompts, commands, or agents.
</command_role>

<inspiration>
## User Insight

> "You can actually go in take the existing prompt that you have and actually feed it more examples where maybe the prompt failed it didn't quite do what you wanted. And you can actually instead of you having to go and rewrite the prompt you just put it into the raw LLM and say help me make this prompt better and because it knows itself so well strangely."

**Key Insight**: LLMs understand their own reasoning better than we do - they can identify why a prompt failed and generate a better version automatically.
</inspiration>

<usage_examples>
## Examples

**Improve a failing agent**:
```bash
/improve-prompt code-reviewer --failures=.claude/failures.log
```

**Improve a command**:
```bash
/improve-prompt /build-prd --failures="Failed on multi-tenant feature, missed row-level security"
```

**Improve custom prompt**:
```bash
/improve-prompt --prompt="Review this code for bugs" --failures="Missed race condition in async code"
```

**Domain specialization**:
```bash
/improve-prompt code-reviewer --domain=healthcare --requirements="Must check for PHI exposure"
```
</usage_examples>

<workflow>
<step number="1">
**Load Original Prompt**

Identify what needs improvement:
- Agent definition (from `agents/definitions/*.md`)
- Command (from `commands/*.md`)
- Custom prompt (from user input)

Example:
```bash
Input: /improve-prompt code-reviewer

Loads: agents/definitions/code-reviewer.md
```
</step>

<step number="2">
**Collect Failure Examples**

Gather evidence of where prompt fails:

**From features.json**:
```bash
# Find features where passes=false and this agent was used
grep -A 10 '"passes": false' features.json

Example failure:
{
  "id": "F042",
  "name": "WebSocket reconnection",
  "passes": false,
  "notes": "Code reviewer missed lack of reconnection logic"
}
```

**From explicit failures parameter**:
```bash
--failures="
1. Input: Multi-tenant auth feature
   Expected: Check row-level security
   Actual: Only checked basic JWT auth

2. Input: Real-time WebSocket
   Expected: Verify reconnection logic
   Actual: Missed reconnection entirely
"
```

**From failure log**:
```bash
# If .claude/failures.log exists
tail -n 50 .claude/failures.log
```
</step>

<step number="3">
**Meta-Analysis Prompt**

Execute meta-prompt to analyze and improve:

```markdown
You are a prompt engineering expert specializing in improving prompts based on failure analysis.

## Original Prompt

{{original_prompt_content}}

## Failure Examples

{{failure_examples}}

## Your Task

1. **Identify Failure Patterns**
   - What types of issues does this prompt consistently miss?
   - Are there blind spots in the instructions?
   - Does it over-focus on certain areas and neglect others?

2. **Root Cause Analysis**
   - Why does the prompt fail on these specific cases?
   - What's ambiguous or missing in the instructions?
   - Are examples needed to clarify expectations?

3. **Generate Improved Version**
   - Fix identified issues
   - Add explicit instructions for missed cases
   - Include examples where helpful
   - Maintain what currently works well

4. **Explain Changes**
   - Document each modification
   - Explain why it addresses the failures
   - Provide before/after comparison

5. **Create Test Cases**
   - Suggest inputs that previously failed
   - Verify improved version handles them
   - Prevent regression on cases that worked

## Output Format

### Failure Pattern Analysis
[Patterns you identified]

### Root Causes
[Why prompt fails on these cases]

### Improved Prompt
```
[Complete improved version]
```

### Changes Made
1. **Change**: [What changed]
   **Rationale**: [Why this fixes failures]
   **Example**: [How it helps]

### Test Cases
1. **Input**: [Previously failed input]
   **Expected**: [What should happen]
   **Verification**: [How to test]

### A/B Comparison
| Aspect | Original | Improved | Benefit |
|--------|----------|----------|---------|
| ... | ... | ... | ... |
```
</step>

<step number="4">
**Review & Apply**

Present results to user:

```
## Meta-Prompt Analysis Complete

### Identified Issues
- Blind spot: Doesn't check for XYZ
- Over-emphasis on ABC
- Missing examples for edge cases

### Proposed Improvements
[Summary of changes]

### Improved Version Saved To
.claude/meta/improved/code-reviewer-v2.md

### Next Steps
1. Review improved version
2. Test on previous failures
3. If satisfied: mv .claude/meta/improved/code-reviewer-v2.md agents/definitions/code-reviewer.md
4. Or: /improve-prompt code-reviewer --iterate (refine further)
```
</step>

<step number="5">
**Optional: A/B Testing**

Compare original vs improved:

```bash
# Run both versions on same test cases
Test Case 1: Multi-tenant auth feature

Original version:
- Checked: JWT implementation ✓
- Missed: Row-level security ✗
- Score: 6/10

Improved version:
- Checked: JWT implementation ✓
- Checked: Row-level security ✓
- Checked: Tenant isolation ✓
- Score: 10/10

RECOMMENDATION: Use improved version (4-point improvement)
```
</step>
</workflow>

<real_world_example>
## Example: Improving code-reviewer Agent

**Scenario**: code-reviewer keeps missing prototype pollution vulnerabilities

**Step 1**: Load current agent
```
Read: agents/definitions/code-reviewer.md
Current focus: OWASP Top 10 (SQL injection, XSS, CSRF, etc.)
```

**Step 2**: Collect failures
```
Failures:
1. Feature F042: Object.assign merge utility
   - Missed: Prototype pollution via __proto__
   - Agent focused on SQL injection (not relevant here)

2. Feature F058: User preference merge
   - Missed: Prototype pollution in deep merge
   - Agent checked input validation but not merge safety

Pattern: Prototype pollution consistently missed
```

**Step 3**: Meta-prompt execution
```
Meta-analysis:
- Root cause: OWASP Top 10 mentioned but not exhaustive
- Prototype pollution IS in OWASP but not explicitly in prompt
- Agent has no examples of what prototype pollution looks like

Improvement:
Add to security checklist:
- [ ] No prototype pollution (check Object.assign, spread, deep merge)
  - Example: Reject __proto__, constructor, prototype keys
  - Use Object.create(null) for safe objects
  - Validate all object merge operations

Add to workflow step 1 (Security Scan):
"Check for prototype pollution in:
- Object.assign() without sanitization
- Spread operator on untrusted objects
- Deep merge functions
- Any code accepting {__proto__: ...} or {constructor: ...}

Example vulnerable code:
function merge(target, source) {
  return Object.assign(target, source) // ❌ Prototype pollution
}

Example safe code:
function merge(target, source) {
  const sanitized = sanitizeKeys(source) // ✓ Keys validated
  return Object.assign(target, sanitized)
}"
```

**Step 4**: Save improved version
```
Saved to: .claude/meta/improved/code-reviewer-v2.md

Changes:
+ Added prototype pollution to security checklist
+ Added examples of vulnerable vs safe code
+ Explicit instruction to check object merges

Test cases:
✓ Re-run on F042 → Now catches prototype pollution
✓ Re-run on F058 → Now catches deep merge issue
✓ Previous passing features still pass
```

**Step 5**: Promote to production
```bash
# After validation
mv .claude/meta/improved/code-reviewer-v2.md agents/definitions/code-reviewer.md

# Update version
# Log improvement in .claude/meta/improvements.log
```

**Result**: Agent now catches prototype pollution automatically!
</real_world_example>

<domain_specialization>
## Using Meta-Prompting for Domain Adaptation

**Use Case**: Adapt general agent for specific domain

**Command**:
```bash
/improve-prompt code-reviewer --domain=healthcare --requirements="PHI detection, HIPAA compliance"
```

**Meta-Prompt**:
```
Original: General code-reviewer agent

Domain Context:
- Healthcare industry
- HIPAA compliance required
- PHI must not leak
- Audit logging mandatory

Generate specialized version that:
1. Adds healthcare-specific security checks
2. Includes PHI exposure detection
3. Verifies HIPAA Security Rule compliance
4. Uses healthcare examples (MRN, diagnosis codes)

Output: code-reviewer-healthcare.md
```

**Result**: Automatic domain specialization without manual rewriting
</domain_specialization>

<continuous_improvement_loop>
## Automated Continuous Improvement

**Vision**: Toolkit learns from every failure automatically

**Configuration** (in `.claude/domain.json`):
```json
{
  "meta_improvement": {
    "enabled": true,
    "auto_improve": true,
    "triggers": {
      "failure_threshold": 5,
      "time_window_days": 7
    },
    "approval_required": true,
    "backup_originals": true
  }
}
```

**Automated Workflow**:
```
1. Every command/agent execution → Log result
2. If failure → Append to .claude/failures.log
3. Every 24 hours → Check failure counts
4. If threshold exceeded (5 failures in 7 days):
   a. Auto-trigger: /improve-prompt [failing-component]
   b. Generate improved version
   c. Save to .claude/meta/pending-improvements/
   d. Create notification for user review
5. User reviews and approves/rejects
6. If approved → Replace original, backup old version
7. Continue monitoring
```

**Benefits**:
- No manual prompt engineering needed
- Learns from production failures
- Continuous quality improvement
- Maintains version history
</continuous_improvement_loop>

<advanced_techniques>
## Advanced Meta-Prompting Techniques

### 1. Ensemble Improvement

Generate multiple improved versions, test all, select best:

```bash
/improve-prompt code-reviewer --ensemble=3

Generates:
- Version A: Conservative (minimal changes)
- Version B: Aggressive (major redesign)
- Version C: Hybrid (best of both)

Test all three → Select highest performer
```

---

### 2. Iterative Refinement

Chain multiple improvement rounds:

```bash
/improve-prompt code-reviewer --iterate=3

Round 1: Fix failure pattern A → Version 2
Round 2: Fix failure pattern B → Version 3
Round 3: Polish and optimize → Version 4 (final)
```

---

### 3. Failure-Pattern Learning

Detect common patterns across all failures:

```bash
/improve-prompt --analyze-patterns

Cross-agent analysis:
- code-reviewer misses: Prototype pollution (5x)
- test-specialist misses: Race conditions (7x)
- healthcare-validator misses: Indirect PHI (3x)

Meta-improvement:
1. Add prototype pollution to code-reviewer
2. Add concurrency checks to test-specialist
3. Add indirect PHI detection to healthcare-validator
```

---

### 4. Genetic Evolution

Evolve prompts like genetic algorithms:

```bash
/improve-prompt code-reviewer --evolve --generations=10

Generation 1: Base prompt, 60% success
  ↓ Mutate (5 variations)
Generation 2: Best variation, 72% success
  ↓ Mutate
Generation 3: Best variation, 81% success
  ↓ Mutate
...
Generation 10: Converged, 94% success

Final: Evolved prompt optimized for your specific use cases
```

</advanced_techniques>

<output_structure>
## Output Files

**Directory**: `.claude/meta/`

```
.claude/
  meta/
    failures.log                    # Auto-collected failures
    improvements.log                # History of improvements
    pending-improvements/           # Awaiting review
      code-reviewer-v2.md
      build-prd-v3.md
    improved/                       # Approved improvements
      code-reviewer-v2.md
      test-specialist-v2.md
    specialized/                    # Domain-specialized versions
      healthcare/
        code-reviewer-healthcare.md
      finance/
        code-reviewer-finance.md
    backups/                        # Original versions
      code-reviewer-v1.md
```

**Improvement Log Entry**:
```json
{
  "timestamp": "2025-12-25T20:00:00Z",
  "target": "agents/definitions/code-reviewer.md",
  "version": "v1 → v2",
  "trigger": "5 failures in 7 days (prototype pollution)",
  "changes": [
    "Added prototype pollution detection",
    "Added object merge validation",
    "Added examples of vulnerable code"
  ],
  "test_results": {
    "before": "60% on test suite",
    "after": "94% on test suite"
  },
  "status": "approved and deployed"
}
```
</output_structure>

<integration>
## Integration with Existing Toolkit

**Works with**:
- `/verify` - If verification fails, suggest `/improve-prompt verify`
- `/review` - If review misses issues, improve code-reviewer
- `/prd-check` - If compliance fails, improve domain validator
- `/build-prd` - If implementation fails, improve build chain
- RAG - Combine with context injection for better improvements
- Prompt Chaining - Improve individual chain steps

**Automatic Triggers** (optional):
```json
{
  "hooks": {
    "on_verify_fail": "/improve-prompt verify --auto",
    "on_review_miss": "/improve-prompt code-reviewer --auto",
    "on_test_fail": "/improve-prompt test-specialist --auto"
  }
}
```
</integration>

<notes>
- Meta-prompting leverages LLM self-knowledge
- LLMs can identify ambiguities in their own instructions
- Automated improvement reduces manual prompt engineering
- Especially powerful for domain adaptation (healthcare, finance, etc.)
- Can be fully automated or require human approval
- Maintains version history for rollback if needed
</notes>

<see_also>
- `/context-inject` - RAG pattern for context
- `agents/meta-prompting-engine.md` - Comprehensive guide
- `agents/prompt-chaining-engine.md` - Chain-based workflows
- Chain-of-Thought (CoT) - Reasoning within prompts
- Self-Consistency - Cross-validation of outputs
</see_also>
