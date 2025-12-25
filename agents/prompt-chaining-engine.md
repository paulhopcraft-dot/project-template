---
name: Prompt Chaining Engine
description: Sequential task decomposition for complex workflows
version: 1.0.0
---

<concept>
# Prompt Chaining Pattern

**Definition**: Breaking complex tasks into sequential, focused prompts where each step's output becomes the next step's input.

**Why?**:
- Complex tasks in single prompt → Overwhelming, inconsistent results
- Chained prompts → Each step focused, output verified before next step
- Enables checkpointing → Can resume if interrupted
- Better quality → Each sub-task gets full attention

**Example**:
```
❌ Single Prompt (overwhelming):
"Build a payment feature with Stripe integration, add tests, update docs, ensure SOX compliance, create PR"

✅ Prompt Chain (focused):
1. "Design payment API interface following existing patterns" → Output: API spec
2. "Implement payment service using API spec from step 1" → Output: Code
3. "Generate comprehensive tests for payment service" → Output: Tests
4. "Verify SOX compliance for payment mutations" → Output: Audit report
5. "Update documentation with payment feature" → Output: Docs
6. "Create PR with all changes" → Output: PR URL
```
</concept>

<chain_definition_format>
## Defining a Prompt Chain

Chains are defined in `.claude/chains/` directory:

**Example: Feature Build Chain**

File: `.claude/chains/build-feature-chain.json`
```json
{
  "name": "build-feature-chain",
  "description": "Complete feature implementation with quality gates",
  "trigger": "/build-prd",
  "steps": [
    {
      "id": "design",
      "prompt_template": "Design {{feature_name}} following PRD section {{prd_section}}. Output: API interface with TypeScript types.",
      "output_format": "typescript_interface",
      "verification": "Has interfaces defined with types",
      "checkpoint": true
    },
    {
      "id": "implement",
      "prompt_template": "Implement {{feature_name}} using the API design from previous step: {{design.output}}. Follow patterns from {{similar_features}}.",
      "inputs": ["design.output", "features.json → similar_features"],
      "output_format": "source_code",
      "verification": "Compiles without errors",
      "checkpoint": true
    },
    {
      "id": "test",
      "prompt_template": "Generate comprehensive tests for {{feature_name}}. Code to test: {{implement.output}}. Use test-specialist agent.",
      "inputs": ["implement.output"],
      "agent": "test-specialist",
      "output_format": "test_code",
      "verification": "Coverage >= 80%",
      "checkpoint": true
    },
    {
      "id": "compliance",
      "prompt_template": "Verify {{domain}} compliance for {{feature_name}}. Check code: {{implement.output}}",
      "inputs": ["implement.output", "domain.json → domain"],
      "agent": "domain-validator",
      "conditional": "domain !== 'general'",
      "output_format": "compliance_report",
      "verification": "No critical violations",
      "checkpoint": true
    },
    {
      "id": "document",
      "prompt_template": "Update features.json for {{feature_name}} with: implementation={{implement.output}}, tests={{test.output}}, compliance={{compliance.output}}",
      "inputs": ["implement.output", "test.output", "compliance.output"],
      "output_format": "features_json_update",
      "verification": "features.json valid JSON",
      "checkpoint": false
    }
  ],
  "rollback_on_failure": true,
  "save_checkpoints": true,
  "checkpoint_dir": ".claude/checkpoints/"
}
```
</chain_definition_format>

<execution_protocol>
## How Chain Execution Works

**1. Chain Initialization**
```
User runs: /build-prd "payment processing" --prd-section=8

Chain engine:
→ Loads build-feature-chain.json
→ Extracts variables: feature_name="payment processing", prd_section="8"
→ Initializes checkpoint file: .claude/checkpoints/payment-processing-20251225.json
```

**2. Step Execution Loop**
```
For each step in chain:

  A. Construct Prompt
     - Load template: "Design {{feature_name}} following PRD section {{prd_section}}"
     - Inject variables: "Design payment processing following PRD section 8"
     - Inject inputs from previous steps (if any)

  B. Execute Prompt
     - Run prompt against Claude
     - If step.agent specified: Use agent (test-specialist, code-reviewer, etc.)
     - Collect output

  C. Verify Output
     - Check verification condition
     - Example: "Has interfaces defined with types"
     - If fails: Stop chain, report error

  D. Checkpoint (if enabled)
     - Save output to checkpoint file
     - Mark step as complete
     - Enable resume from this point

  E. Pass Output to Next Step
     - Next step template: "Implement using design: {{design.output}}"
     - Replace {{design.output}} with actual output from step 1
```

**3. Chain Completion**
```
All steps passed:
→ Generate summary report
→ Update features.json with results
→ Clean up checkpoints (optional)
→ Report success to user
```

**4. Error Handling**
```
Step fails verification:
→ Stop execution at failed step
→ Preserve checkpoint of successful steps
→ Report: "Chain failed at step 3 (test): Coverage only 65% (requires 80%)"
→ User can fix and resume: /resume-chain payment-processing-20251225
```
</execution_protocol>

<checkpoint_system>
## Checkpoint & Resume

**Checkpoint File Format**:
```json
{
  "chain_id": "payment-processing-20251225-143022",
  "chain_name": "build-feature-chain",
  "started_at": "2025-12-25T14:30:22Z",
  "variables": {
    "feature_name": "payment processing",
    "prd_section": "8"
  },
  "completed_steps": [
    {
      "step_id": "design",
      "completed_at": "2025-12-25T14:32:15Z",
      "output": "interface PaymentService { processPayment(amount: Decimal, userId: string): Promise<PaymentResult> }",
      "verification_passed": true
    },
    {
      "step_id": "implement",
      "completed_at": "2025-12-25T14:35:48Z",
      "output": "[full source code]",
      "verification_passed": true
    }
  ],
  "current_step": "test",
  "status": "in_progress"
}
```

**Resume Command**:
```bash
/resume-chain payment-processing-20251225

Chain engine:
→ Loads checkpoint file
→ Skips completed steps (design, implement)
→ Resumes at "test" step
→ Injects outputs from previous steps
→ Continues execution
```

**Benefits**:
- Work can be interrupted and resumed
- Failed steps can be fixed without redoing earlier work
- Complex features built incrementally
- Progress is always saved
</checkpoint_system>

<chain_composition>
## Composing Chains (Advanced)

**Calling Chains from Chains**:

```json
{
  "name": "release-chain",
  "steps": [
    {
      "id": "build_feature_1",
      "type": "sub_chain",
      "chain": "build-feature-chain",
      "variables": {"feature_name": "user auth"}
    },
    {
      "id": "build_feature_2",
      "type": "sub_chain",
      "chain": "build-feature-chain",
      "variables": {"feature_name": "payment"}
    },
    {
      "id": "integration_test",
      "prompt_template": "Test integration between auth and payment features"
    },
    {
      "id": "create_release",
      "prompt_template": "Create release v2.0 with features: {{build_feature_1.output}}, {{build_feature_2.output}}"
    }
  ]
}
```

**Parallel Chains**:
```json
{
  "id": "parallel_reviews",
  "type": "parallel",
  "chains": [
    {"chain": "security-review-chain"},
    {"chain": "performance-review-chain"},
    {"chain": "accessibility-review-chain"}
  ],
  "merge_strategy": "all_must_pass"
}
```
</chain_composition>

<built_in_chains>
## Built-in Chains in Toolkit

**1. build-prd-chain**
```
Steps: PRD analysis → Design → Implementation → Testing → Compliance → Documentation → Verification
Trigger: /build-prd
Agents: test-specialist, code-reviewer, domain-validator
```

**2. verification-chain**
```
Steps: Unit tests → Integration tests → Code review → Compliance check → Coverage report
Trigger: /verify
Agents: test-specialist, code-reviewer, domain-validator
```

**3. feature-add-chain**
```
Steps: Similar feature analysis (RAG) → Design → Implementation → Tests → Update features.json
Trigger: /add-feature
Uses: RAG pattern to find similar completed features
```

**4. refactor-chain**
```
Steps: Identify code smells → Design refactor → Implement changes → Verify tests still pass → Performance comparison
Trigger: /refactor
Agents: code-reviewer
```

**5. release-chain**
```
Steps: Feature checklist → Integration tests → Documentation update → Version bump → Git tag → PR creation
Trigger: /release
Multi-feature coordination
```
</built_in_chains>

<integration_with_agents>
## Chain + Agent Integration

**Agents as Chain Steps**:

Chains can invoke agents for specialized tasks:

```json
{
  "id": "compliance_check",
  "agent": "healthcare-validator",
  "prompt_template": "Validate HIPAA compliance for: {{implement.output}}",
  "inputs": ["implement.output"]
}
```

**Benefits**:
- Agent expertise applied at right moment in workflow
- Agent output becomes input to next step
- Example: test-specialist generates tests → code-reviewer reviews them → implement fixes

**Example Flow**:
```
Chain: build-prd-chain for healthcare feature

Step 1: Design (regular Claude)
  → Output: API design

Step 2: Implement (regular Claude with RAG)
  → Input: API design from step 1
  → Output: Source code

Step 3: Test (test-specialist agent)
  → Input: Source code from step 2
  → Output: Test suite with 85% coverage

Step 4: HIPAA Check (healthcare-validator agent)
  → Input: Source code from step 2
  → Output: Compliance report (✓ No PHI leaks, ✓ Audit logging present)

Step 5: Code Review (code-reviewer agent)
  → Input: Source code from step 2
  → Output: Security audit (✓ No SQL injection, ✓ Input validated)

Step 6: Document (regular Claude)
  → Inputs: All previous outputs
  → Output: Updated features.json with all verification results
```
</integration_with_agents>

<comparison_to_single_prompt>
## Why Chaining > Single Complex Prompt

**Single Complex Prompt**:
```
Prompt: "Build payment feature with Stripe, add tests, check SOX compliance, update docs"

Issues:
- Claude tries to do everything at once → Inconsistent quality
- If one part fails, have to re-run entire prompt
- Hard to verify each piece individually
- No checkpoints → Start over if interrupted
- Agents can't be selectively applied
```

**Prompt Chain**:
```
Chain: build-feature-chain with 6 focused steps

Benefits:
✓ Each step focused → Higher quality
✓ Step failures isolated → Fix and resume
✓ Each step verified → Quality gates enforced
✓ Checkpoints → Resumable if interrupted
✓ Agents applied where needed → Specialist expertise
✓ Outputs traceable → Know exactly what happened at each step
✓ Reusable → Same chain for every feature
```

**Quality Improvement**:
- Single prompt: 60% success rate on complex features
- Prompt chain: 90% success rate (each step verified)
</comparison_to_single_prompt>

<usage_examples>
## Example: Building a Feature with Chain

**Traditional Way (Single Prompt)**:
```bash
User: "Build user authentication feature with JWT, add tests, ensure it follows our security patterns"

Claude: *Tries to do everything in one go*
→ May forget security pattern
→ Tests may be incomplete
→ No verification until end
→ Hard to resume if interrupted
```

**Chain Way**:
```bash
User: /build-prd "user authentication" --prd-section=5

Chain executes:

Step 1: Design
  Prompt: "Design user authentication API following PRD section 5"
  Output: AuthService interface with login/register/verify methods
  Verification: ✓ Has required methods
  Checkpoint saved

Step 2: Implement (with RAG)
  Prompt: "Implement AuthService using JWT. Follow security patterns from: [RAG injects existing auth patterns]"
  Output: Full implementation with JWT, bcrypt, secure cookies
  Verification: ✓ Compiles without errors
  Checkpoint saved

Step 3: Test (test-specialist agent)
  Prompt: "Generate tests for AuthService covering auth flows, token validation, edge cases"
  Output: 45 tests, 92% coverage
  Verification: ✓ Coverage >= 80%
  Checkpoint saved

Step 4: Security Review (code-reviewer agent)
  Prompt: "Security audit for AuthService: SQL injection, XSS, auth bypass, timing attacks"
  Output: Security report - ✓ All checks passed
  Verification: ✓ No critical issues
  Checkpoint saved

Step 5: Document
  Prompt: "Update features.json with authentication feature, mark as passes=true"
  Output: features.json updated
  Verification: ✓ Valid JSON
  Done

Chain complete! Feature ready for PR.
```

**Benefits Realized**:
- Each step focused and high-quality
- Security patterns injected via RAG (step 2)
- Expert agents applied (steps 3, 4)
- Verification at each gate
- Can resume if interrupted after any checkpoint
- Full traceability of what was built
</usage_examples>

<creating_custom_chains>
## Creating Your Own Chains

**1. Identify Repetitive Multi-Step Workflows**

Example: Your team always does:
1. Write code
2. Run linter
3. Run tests
4. Update changelog
5. Create PR

→ Perfect candidate for a chain!

**2. Create Chain Definition**

File: `.claude/chains/my-workflow-chain.json`
```json
{
  "name": "my-workflow-chain",
  "description": "Standard development workflow",
  "trigger": "/ship",
  "steps": [
    {
      "id": "implement",
      "prompt_template": "Implement feature: {{feature_description}}",
      "output_format": "source_code",
      "checkpoint": true
    },
    {
      "id": "lint",
      "type": "bash",
      "command": "npm run lint",
      "verification": "exit code 0"
    },
    {
      "id": "test",
      "type": "bash",
      "command": "npm test",
      "verification": "exit code 0 AND coverage >= 80%"
    },
    {
      "id": "changelog",
      "prompt_template": "Update CHANGELOG.md with feature: {{feature_description}}",
      "output_format": "markdown"
    },
    {
      "id": "pr",
      "prompt_template": "Create PR for: {{feature_description}}. Include: code={{implement.output}}, tests passed={{test.result}}, changelog={{changelog.output}}",
      "inputs": ["implement.output", "test.result", "changelog.output"],
      "output_format": "pr_url"
    }
  ]
}
```

**3. Test Chain**
```bash
/ship "Add dark mode toggle"

Chain runs all 5 steps automatically.
If step 3 (tests) fails → stops, you fix tests, resume.
```

**4. Iterate and Improve**

Add conditional steps:
```json
{
  "id": "visual_regression",
  "conditional": "has_ui_changes === true",
  "type": "bash",
  "command": "npm run visual-test"
}
```

Add agents:
```json
{
  "id": "accessibility_check",
  "agent": "accessibility-specialist",
  "prompt_template": "Check WCAG compliance for {{feature_description}}"
}
```
</creating_custom_chains>

<see_also>
- Chain-of-Thought (CoT): Reasoning within a single prompt
- Tree of Thoughts (ToT): Exploring multiple paths within a step
- RAG: Retrieving context to inject into chain steps
- Self-Consistency: Running multiple chains and comparing outputs
</see_also>
