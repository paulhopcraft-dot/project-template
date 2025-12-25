---
name: context-inject
description: Use RAG pattern to inject domain context into current task
usage: /context-inject <task-description>
category: context
version: 1.0.0
---

<command_role>
Apply Retrieval Augmented Generation (RAG) to enhance task execution with project-specific knowledge.
</command_role>

<rag_pattern>
## Retrieval Augmented Generation

**Concept**: Before executing a task, retrieve and inject relevant context from:
1. Project documentation (PRD, SPEC, domain.json)
2. Features.json (completed features, patterns established)
3. Code patterns (existing implementations to follow)
4. Domain-specific rules (healthcare, revenue, etc.)

**Why RAG?**: Generic LLM knowledge + Project-specific context = Better, more consistent results
</rag_pattern>

<workflow>
<step number="1">
**Understand Task**
Parse user request to identify:
- Domain: Is this healthcare, revenue, general dev?
- Scope: Which features/modules are affected?
- Context needs: What knowledge would improve execution?

Example: "Add payment processing to checkout flow"
→ Domain: Revenue (likely needs SOX compliance)
→ Scope: Checkout module, payment integration
→ Context needed: Existing payment patterns, audit requirements
</step>

<step number="2">
**Retrieve Relevant Context (RAG)**

Read and extract relevant sections from:

**Domain Configuration**:
```bash
# Check domain-specific requirements
Read .claude/domain.json
→ Extract: Compliance requirements, quality gates, patterns

# Example for revenue domain:
"financial_validation": {
  "decimal_precision": "required",
  "audit_trail": "all mutations must log",
  "no_float_math": "use Decimal for currency"
}
```

**Feature History**:
```bash
# Find similar completed features
Read features.json
→ Filter: completed_features where domain matches
→ Extract: Patterns, acceptance criteria, notes

# Example:
Feature F007 (completed): "Payment Gateway Integration"
→ Pattern: Used Stripe SDK, stored audit logs in payments_log table
→ Lesson: Always validate webhook signatures
```

**Project Documentation**:
```bash
# Get domain requirements
Read docs/PRD*.md or docs/SPEC*.md
→ Search for: Related requirements, constraints
→ Extract: Must-follow rules

# Example from PRD:
Section 8.2: "All payment mutations require audit trail with user_id, timestamp, amount, reason"
```

**Code Patterns**:
```bash
# Find existing implementations to follow
Grep pattern="paymentService\." output_mode="files_with_matches"
→ Read: src/services/payment.ts
→ Extract: Error handling pattern, validation approach

# Example pattern found:
try {
  const result = await stripe.charge(...)
  await auditLog.record({ action: 'PAYMENT', ... })
} catch (error) {
  await auditLog.record({ action: 'PAYMENT_FAILED', ... })
  throw
}
```
</step>

<step number="3">
**Inject Context into Task Prompt**

Construct enhanced prompt with retrieved context:

```
Original task: "Add payment processing to checkout flow"

ENHANCED with RAG:

Task: Add payment processing to checkout flow

DOMAIN CONTEXT (from domain.json):
- This is a revenue domain project with SOX compliance
- All financial mutations require decimal precision (no floats)
- Audit trail is mandatory for all payment operations

SIMILAR COMPLETED WORK (from features.json):
- Feature F007 used Stripe SDK with webhook signature validation
- Pattern: Audit log before AND after mutation, including failures

PRD REQUIREMENTS (from docs/PRD_v1.md):
- Section 8.2: Audit trail must include user_id, timestamp, amount, reason
- Section 8.5: Payment failures must not leak sensitive card data in errors

CODE PATTERN TO FOLLOW (from src/services/payment.ts):
- Use try/catch with audit logging in both paths
- Validate input with Decimal type for amounts
- Return generic errors to client, detailed logs server-side

Now execute the task following these project-specific patterns.
```
</step>

<step number="4">
**Execute with Context**
- Implement feature using injected context
- Follow established patterns automatically
- Meet compliance requirements by default
- Maintain consistency with existing code
</step>

<step number="5">
**Verify Context Application**
Cross-check implementation against injected context:
- ✓ Used Decimal for currency (domain.json requirement)
- ✓ Added audit logs (PRD requirement)
- ✓ Followed error handling pattern (code pattern)
- ✓ Validated webhook signatures (lesson from F007)
</step>
</workflow>

<benefits>
## Why RAG Improves Toolkit

**Without RAG**:
- Claude uses generic knowledge → May miss project-specific patterns
- Inconsistent implementations across features
- Forgets compliance requirements unless reminded

**With RAG**:
- Automatic context injection → Follows project conventions
- Consistent code patterns → Reads existing code and replicates style
- Compliance by default → Domain rules applied automatically
- Knowledge reuse → Learns from completed features

**Example Impact**:
- **Before**: Dev adds payment, forgets audit logging, fails review
- **After**: RAG injects audit requirement from domain.json → implemented correctly first time
</benefits>

<usage_examples>
## Examples

**Example 1: Healthcare Domain**
```bash
/context-inject "Add prescription refill request feature"

→ RAG retrieves:
  - domain.json: HIPAA PHI protection rules
  - features.json: Previous feature used encryption for medical data
  - PRD: Section 5.2 requires provider verification
  - Code: Existing prescriptions.ts shows audit pattern

→ Implementation automatically includes:
  ✓ PHI encryption
  ✓ Provider auth check
  ✓ Audit logging
  ✓ Follows existing code style
```

**Example 2: Revenue Domain**
```bash
/context-inject "Generate quarterly revenue report"

→ RAG retrieves:
  - domain.json: SOX compliance, decimal precision required
  - features.json: Report F003 used Decimal.js for calculations
  - SPEC: Revenue recognition rules in section 4
  - Code: Existing reports use ReportBuilder class

→ Implementation automatically:
  ✓ Uses Decimal for all money math
  ✓ Follows revenue recognition rules
  ✓ Uses established ReportBuilder pattern
  ✓ Includes audit trail
```

**Example 3: General Development**
```bash
/context-inject "Add user profile editing"

→ RAG retrieves:
  - domain.json: Test coverage minimum 80%
  - features.json: Auth features used JWT middleware pattern
  - Code: Existing user.ts shows validation approach

→ Implementation automatically:
  ✓ Adds JWT middleware for auth
  ✓ Includes comprehensive tests (>80%)
  ✓ Follows validation pattern from user.ts
```
</usage_examples>

<integration>
## Auto-Trigger RAG

Configure commands to automatically use RAG:

**In .claude/domain.json**:
```json
{
  "rag": {
    "auto_inject": true,
    "sources": [
      "domain.json",
      "features.json",
      "docs/PRD*.md",
      "docs/SPEC*.md"
    ],
    "code_patterns": {
      "enabled": true,
      "max_examples": 2
    }
  }
}
```

**Commands that benefit from RAG**:
- `/build-prd` - Inject PRD requirements automatically
- `/edit-prd` - Follow existing code patterns
- `/add-feature` - Learn from completed features
- `/verify` - Check against domain requirements
</integration>

<output_format>
When RAG is used, show context sources:

```
## Context Injected (RAG)

📋 Domain: Revenue (SOX compliance)
📊 Pattern: 2 similar features analyzed
📄 Requirements: PRD v1.2 section 8, SPEC v1.1 section 4
💻 Code Style: Analyzed src/services/payment.ts, src/models/transaction.ts

Proceeding with implementation using project-specific context...
```
</output_format>

<notes>
- RAG prevents "generic Claude" responses by injecting project knowledge
- Reduces back-and-forth: "Did you check the PRD?" → Already checked via RAG
- Maintains consistency: New code follows existing patterns automatically
- Compliance by default: Domain rules applied without manual reminder
</notes>

<see_also>
- `/context` - Manual context management
- `/reload` - Refresh project context
- `/prd-check` - Verify alignment with PRD
</see_also>
