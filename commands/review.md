---
description: Code review current work and suggest improvements
---

<instructions>
Review the code changes since last commit (or specified files).
</instructions>

<agent_integration>
**If Advanced Agent System is installed** (check for `.claude/agents/registry.json`):

<trigger_agent>code-reviewer</trigger_agent>

<agent_workflow>
The **code-reviewer agent** provides expert-level code review focused on:
- **Security Analysis**: OWASP Top 10, injection attacks, auth vulnerabilities
- **Code Quality**: DRY, SOLID, design patterns, complexity analysis
- **Performance**: N+1 queries, algorithmic complexity, memory leaks
- **Maintainability**: Naming, documentation, modularity
</agent_workflow>

<fallback>
If agent system NOT installed, use basic review checklist below.
</fallback>
</agent_integration>

<review_checklist>
<category name="Correctness">
- [ ] Logic is correct
- [ ] Edge cases handled
- [ ] Error handling appropriate
- [ ] No obvious bugs
</category>

<category name="Security">
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevented
- [ ] Auth/authz correct
</category>

<category name="Quality">
- [ ] Code is readable
- [ ] Functions are focused (single responsibility)
- [ ] No unnecessary complexity
- [ ] Tests cover the changes
</category>

<category name="Performance">
- [ ] No obvious N+1 queries
- [ ] No blocking calls in async code
- [ ] Appropriate caching considered
</category>
</review_checklist>

<output_format>
```
Code Review: [files reviewed]
================================

✅ Good:
- [What's done well]

⚠️ Suggestions:
- [Improvements to consider]

❌ Issues (must fix):
- [Problems that need addressing]

Overall: [APPROVE / NEEDS CHANGES]
```
</output_format>

<arguments>$ARGUMENTS</arguments>
