---
name: Meta-Prompting Engine
description: Self-improving prompts that generate better versions of themselves
version: 1.0.0
---

<concept>
# Meta-Prompting: Prompts that Improve Prompts

**Definition**: Using an LLM to analyze and improve prompts based on failure examples

**Key Insight**: LLMs understand themselves better than we do - they can identify why a prompt failed and generate a better version

**The Loop**:
```
1. Prompt fails or underperforms
2. Feed to meta-prompt: "Here's the prompt + examples where it failed"
3. LLM analyzes failure patterns
4. LLM generates improved prompt
5. Test new prompt
6. Repeat if needed
```
</concept>

<user_example>
## Real-World Example from User

**Scenario**: Classifier prompt that adapts based on query

**Traditional Approach**:
```
You have a general classifier prompt.
When it fails on edge cases, you manually rewrite it.
Trial and error until it works.
```

**Meta-Prompting Approach**:
```
You have a general classifier prompt.
When it fails, you feed: prompt + failure examples to raw LLM.
LLM generates specialized version for that query type.
Automatically improves itself.
```

**Why This Works**:
> "Because it knows itself so well strangely"
- LLMs have introspection into their own reasoning
- They understand what prompt structures work better
- They can identify ambiguity in instructions
- They can specialize prompts for specific domains
</user_example>

<pattern_types>
## Types of Meta-Prompting

### 1. Failure-Driven Improvement

**When**: Prompt works 80% of the time, fails on edge cases

**Meta-Prompt Template**:
```
I have this prompt that's failing on certain inputs:

CURRENT PROMPT:
"""
[Your prompt here]
"""

FAILURE EXAMPLES:
1. Input: [failed input 1]
   Expected: [what should happen]
   Actual: [what happened]

2. Input: [failed input 2]
   Expected: [what should happen]
   Actual: [what happened]

Analyze why the prompt fails on these cases and generate an improved version that handles these edge cases while maintaining performance on normal cases.
```

**LLM Response**:
```
Analysis:
- Failure pattern: Prompt assumes X, but edge cases violate X
- Root cause: Ambiguous instruction about Y
- Missing: Explicit handling of Z case

IMPROVED PROMPT:
"""
[Enhanced version with fixes]
"""

Changes made:
1. Added explicit instruction for Z case
2. Clarified Y with examples
3. Added constraint to prevent X assumption
```

---

### 2. Domain Specialization

**When**: General prompt needs to adapt for specific domain

**Meta-Prompt Template**:
```
I have this general-purpose prompt:

GENERAL PROMPT:
"""
[Your generic prompt]
"""

DOMAIN CONTEXT:
- Domain: Healthcare / Finance / Legal / etc.
- Specific requirements: [HIPAA, SOX, compliance needs]
- Domain terminology: [key terms]

Generate a specialized version of this prompt optimized for this domain. Include domain-specific examples, terminology, and constraints.
```

**Example for Toolkit**:
```
GENERAL PROMPT (code-reviewer):
"Review this code for security issues"

DOMAIN: Healthcare

META-PROMPT generates:
"Review this code for security issues, specifically:
- PHI exposure in logs, errors, or responses
- HIPAA Security Rule violations (encryption, access control)
- BAA requirements for third-party services
- Audit logging completeness
Use healthcare examples: MRN leakage, diagnosis code exposure, etc."
```

---

### 3. Dynamic Classifier (User's Example)

**When**: Different query types need different prompt strategies

**Meta-Prompt Template**:
```
I have a classifier that processes various types of queries.

QUERY: [User's actual query]

QUERY TYPE: [Detected type: technical, creative, analytical, etc.]

GENERAL CLASSIFIER PROMPT:
"""
[Your current classifier prompt]
"""

Generate a specialized version of this prompt optimized specifically for [QUERY TYPE] queries. The specialized prompt should handle the nuances of this query type better than the general version.
```

**Example**:
```
QUERY: "Debug this SQL injection vulnerability"
TYPE: Technical security issue

Meta-prompt generates specialized version:
- Adds security-specific context
- Includes OWASP references
- Provides SQL injection examples
- Tailors output format for security reports
```

---

### 4. Performance Optimization

**When**: Prompt works but is inefficient or verbose

**Meta-Prompt Template**:
```
This prompt works but has performance issues:

CURRENT PROMPT:
"""
[Your working but slow prompt]
"""

PERFORMANCE ISSUES:
- Takes too many tokens
- Requires multiple rounds
- Produces verbose output
- Misses obvious shortcuts

Generate a more efficient version that produces the same quality output with fewer tokens and faster execution.
```

---

### 5. Iterative Refinement Loop

**When**: Continuous improvement based on production failures

**Automation**:
```
LOOP:
  1. Collect failures from production usage
  2. Every N failures, trigger meta-prompt
  3. Generate improved version
  4. A/B test: 90% old version, 10% new version
  5. If new version performs better, promote to 100%
  6. Continue collecting failures
```

</pattern_types>

<toolkit_integration>
## Applying Meta-Prompting to claude-code-toolkit

### Use Case 1: Agent Self-Improvement

**Scenario**: code-reviewer agent misses certain security issues

**Implementation**:

File: `.claude/agents/meta/improve-agent.md`
```markdown
---
trigger: When agent_failure_count > threshold
---

AGENT BEING IMPROVED: code-reviewer

FAILURE LOG:
[Automatically collected from features.json where passes=false]

Example failures:
1. Missed: ReDoS vulnerability in regex validation
   File: src/validators/email.ts
   Why missed: Agent didn't check regex complexity

2. Missed: Prototype pollution in object merge
   File: src/utils/merge.ts
   Why missed: Agent focused on SQL injection, missed prototype pollution

META-ANALYSIS:
Current agent prompt emphasizes OWASP Top 10 but doesn't explicitly mention:
- ReDoS (Regular Expression Denial of Service)
- Prototype pollution
- These are in OWASP but not prominently featured

IMPROVED AGENT PROMPT:
[Generate enhanced version with explicit ReDoS and prototype pollution checks]

TESTING:
- Re-run agent on previous failures
- Verify: New version catches missed issues
- If successful: Update agents/definitions/code-reviewer.md
```

---

### Use Case 2: Command Adaptation

**Scenario**: `/build-prd` command works for simple features, fails on complex ones

**Meta-Prompt**:
```
COMMAND: /build-prd

FAILURES:
1. Feature: "Multi-tenant authorization with row-level security"
   Issue: Generated basic auth, missed row-level security

2. Feature: "Real-time WebSocket with reconnection logic"
   Issue: Implemented WebSocket but no reconnection

3. Feature: "Payment processing with idempotency"
   Issue: Basic Stripe integration, no idempotency keys

PATTERN: Command misses advanced requirements when feature description uses shorthand

META-IMPROVEMENT:
Add clarification step to /build-prd chain:

NEW STEP 0 (before design):
  Prompt: "Analyze feature description: '{{feature}}'.

  List implicit requirements based on keywords:
  - 'multi-tenant' → row-level security, tenant isolation
  - 'real-time' → reconnection, heartbeat, offline handling
  - 'payment' → idempotency, webhook verification, refunds

  Expand feature description with explicit requirements before proceeding."

Result: Command now catches implicit requirements automatically
```

---

### Use Case 3: Domain-Specific Specialization

**Scenario**: Healthcare projects need different prompts than finance projects

**Current State**:
```
Generic prompt: "Add user authentication"
→ Generates: Basic JWT auth

Healthcare version should generate:
✓ MFA required (HIPAA)
✓ Session timeout (15 min)
✓ Audit logging of auth events
✓ No PHI in JWT claims

Finance version should generate:
✓ IP whitelisting option
✓ SOX-compliant audit trail
✓ PCI DSS session requirements
```

**Meta-Prompt Implementation**:

File: `.claude/meta/domain-specializer.md`
```markdown
INPUT:
- Generic command prompt
- Domain: healthcare|finance|general
- domain.json configuration

PROCESS:
1. Load domain.json requirements
2. Analyze generic prompt
3. Inject domain-specific constraints
4. Generate specialized version

OUTPUT:
Domain-specialized prompt with compliance built-in

CACHE:
Store specialized prompts in .claude/meta/specialized/
Reuse for similar commands
```

---

### Use Case 4: RAG + Meta-Prompting Combination

**Power Combo**: RAG retrieves context, Meta-Prompting adapts prompt

**Example**:
```
User: /add-feature "notification system"

STEP 1 (RAG): Retrieve similar features
→ Found: Feature F007 (email notifications)
→ Pattern: Used SendGrid, queued with Bull

STEP 2 (Meta-Prompting): Adapt generic feature prompt
→ Input: Generic "add feature" prompt
→ Context: SendGrid + Bull patterns from RAG
→ Output: Specialized prompt that uses established patterns

STEP 3 (Execute): Run specialized prompt
→ Implementation automatically uses SendGrid + Bull
→ Consistent with existing codebase
→ No manual prompt engineering needed
```

</toolkit_integration>

<implementation_new_command>
## New Command: /improve-prompt

**Purpose**: Meta-prompt any failing command or agent

**Usage**:
```bash
# Improve a command that failed
/improve-prompt command=/build-prd failures=features.json

# Improve an agent
/improve-prompt agent=code-reviewer failures=.claude/agent-failures.log

# Improve custom prompt
/improve-prompt prompt="[your prompt]" failures="[failure examples]"
```

**Implementation**:

File: `commands/improve-prompt.md`
```markdown
---
name: improve-prompt
description: Meta-prompt to generate improved version based on failures
category: meta
---

<workflow>
STEP 1: Collect Context
- Load original prompt
- Load failure examples
- Identify failure patterns

STEP 2: Meta-Analysis
Prompt to Claude:
"""
You are a prompt engineering expert. Analyze this prompt and its failures:

ORIGINAL PROMPT:
{{original_prompt}}

FAILURES:
{{failure_examples}}

Your task:
1. Identify why the prompt fails on these cases
2. Detect patterns in the failures
3. Find ambiguities or missing instructions
4. Generate an improved version

Provide:
- Root cause analysis
- Pattern identification
- Improved prompt
- Explanation of changes
- Test cases to verify improvement
"""

STEP 3: Generate Improved Version
- Output new prompt
- Document changes
- Suggest test cases

STEP 4: Optional A/B Test
- Run both versions on same inputs
- Compare results
- Recommend which to use
</workflow>

<output_format>
## Meta-Prompt Analysis

### Failure Patterns Detected
[List of patterns]

### Root Causes
[Analysis]

### Improved Prompt
```
[New version]
```

### Changes Made
1. [Change 1 with rationale]
2. [Change 2 with rationale]

### Test Cases
[Suggested tests to verify improvement]
</output_format>
```

</implementation_new_command>

<automatic_improvement_loop>
## Automatic Continuous Improvement

**Vision**: Toolkit learns from every failure and improves itself

**Architecture**:

```
.claude/
  meta/
    failures.log              # Auto-collected failures
    improvements.log          # Improvement history
    specialized/              # Generated specialized prompts
      healthcare/
        code-reviewer-v2.md   # Improved version
        build-prd-v3.md
      finance/
        code-reviewer-v2.md

  agents/
    definitions/
      code-reviewer.md        # Original (v1)
      code-reviewer-meta.md   # Meta-improvement instructions
```

**Trigger Conditions**:
```json
{
  "meta_improvement": {
    "enabled": true,
    "triggers": {
      "failure_threshold": 5,
      "time_window": "7 days",
      "confidence_required": 0.8
    },
    "auto_promote": false
  }
}
```

**Workflow**:
```
1. Agent/Command executes → If fails, log to failures.log
2. When failure_count >= 5 in 7 days → Trigger meta-improvement
3. Meta-prompt analyzes failures → Generates improved version
4. Save to .claude/meta/specialized/
5. Human review (if auto_promote=false)
6. If approved → Replace original
7. Continue monitoring
```

</automatic_improvement_loop>

<advanced_patterns>
## Advanced Meta-Prompting Patterns

### 1. Ensemble Meta-Prompting

**Concept**: Generate multiple improved versions, ensemble them

```
Input: Failing prompt + examples

Meta-Prompt 1 (Conservative): "Fix minimal issues, preserve structure"
→ Output: Version A

Meta-Prompt 2 (Aggressive): "Completely redesign for these failures"
→ Output: Version B

Meta-Prompt 3 (Hybrid): "Combine best of both approaches"
→ Input: Version A + Version B
→ Output: Version C (ensemble)

Test all three, select best performer
```

---

### 2. Genetic Prompt Evolution

**Concept**: Evolve prompts like genetic algorithms

```
GENERATION 1:
- Prompt V1 (original)
- Fitness: 60% success rate

MUTATION:
- Meta-prompt generates 5 variations
- Variation 1: Add examples
- Variation 2: Simplify language
- Variation 3: Add constraints
- Variation 4: Change structure
- Variation 5: Domain-specialize

SELECTION:
- Test all 5 variations
- Variation 3 has 75% success rate → Winner

GENERATION 2:
- Use Variation 3 as base
- Generate 5 new mutations
- Repeat...

CONVERGENCE:
- Stop when success rate plateau
- Final prompt is "evolved" for your use case
```

---

### 3. Self-Reflective Prompts

**Concept**: Prompt includes self-analysis

```
You are a code reviewer.

[Review instructions...]

AFTER COMPLETING REVIEW:
Self-reflect:
1. Did I miss any obvious issues by focusing too deeply on one area?
2. Are my severity levels consistent?
3. Did I follow my own guidelines?

If self-reflection reveals issues, re-review with corrections.

Report both: initial findings + self-corrections
```

**Why This Works**:
- LLM reviews its own output
- Catches inconsistencies
- Self-corrects before final output
- Similar to Self-Consistency but integrated into single prompt

</advanced_patterns>

<success_metrics>
## Measuring Meta-Prompt Effectiveness

**Before Meta-Prompting**:
- Prompt improvement: Manual, time-consuming
- Adaptation to failures: Requires developer intervention
- Domain specialization: Create separate prompts manually
- Learning curve: No learning from failures

**After Meta-Prompting**:
- Prompt improvement: Automated with /improve-prompt
- Adaptation: Self-improving based on failure patterns
- Domain specialization: Auto-generated on demand
- Learning curve: Continuous improvement from production use

**Expected Impact**:
- Prompt quality improvement: +20-30% per iteration
- Time to fix failing prompts: 15 min → 2 min
- Domain adaptation: Manual (hours) → Automatic (minutes)
- Failure recurrence: High → Low (learns from mistakes)

</success_metrics>

<see_also>
- Chain-of-Thought: Reasoning within prompts
- RAG: Context injection before prompts
- Prompt Chaining: Sequential prompts
- Active-Prompt: Dynamic prompt selection
- Automatic Prompt Engineer (APE): Research paper on automated prompt generation
</see_also>

<references>
## Research & Inspiration

- **Automatic Prompt Engineer (APE)**: Zhou et al., 2022
  - Automated instruction generation and selection

- **Large Language Models Are Human-Level Prompt Engineers**: 2022
  - LLMs can generate better prompts than humans

- **Active-Prompt**: Diao et al., 2023
  - Task-specific example selection for prompts

- **User's Insight**: "Because it knows itself so well strangely"
  - LLMs have introspection into their own reasoning
  - Can identify and fix prompt ambiguities
  - Self-understanding enables self-improvement
</references>
