# Todo List

## Immediate
- [ ] Run ecosystem tests: `.\run-ecosystem-tests.ps1`
- [ ] Import Thunder Client collections into VS Code
  - Files in `test-collections/` folder
  - gocontrol-api.json, gpnet3-api.json, goconnect-api.json
- [ ] Sync toolkit to all projects: `.\copy-toolkit.ps1`
- [ ] Buy an AI computer
  - Research options for local LLM inference
  - Consider: Mac Studio M4, NVIDIA workstation, or cloud GPU

---

## Blocking (Before SMB customers)

### Complete GoMemory to 80%
**Priority: CRITICAL - Platform blocker**

Current state: 20% complete (scaffold only)

Why it matters:
- Without reliable memory, agents have no context
- They'll repeat questions, forget decisions, lose user trust
- The biggest gap in the platform

Requirements:
- Cross-session recall
- Multi-tenant isolation
- Keep read-only from GoAgent's perspective
- GoMemory suggests, GoAgent requests, GoControl authorizes

---

### Add audit persistence to GoControl
**Priority: CRITICAL - Compliance requirement**

Why it matters:
- Decisions happen in GoControl
- Actions happen in GoAgent
- Transcripts happen in GoConnect
- No single source of truth for "what happened and why"

Requirements:
- Immutable append-only log
- Every decision logged with timestamp, tenant, reason
- Cannot be tampered with
- Required for enterprise/compliance deals

---

### Document GoConnect vs GoMemory boundary
**Priority: HIGH - Architecture clarity**

The problem:
- GoConnect handles "transcripts"
- GoMemory handles "recall"
- These will merge accidentally unless explicitly separated

Decision needed:
- Who owns conversation state? Pick one.
- Where does "conversation history" live?
- Session state: GoConnect or GoMemory?

Action: Write a boundary document, enforce in code.

---

## Infrastructure

### Add tenant isolation layer
**Priority: HIGH - Required for multi-tenant SaaS**

Current state: Implied but not explicit

Requirements:
- Hard boundaries, not soft conventions
- Each tenant's data completely isolated
- Cannot accidentally cross tenant boundaries
- Required for SMB SaaS model

---

### Add distributed tracing across modules
**Priority: MEDIUM - Required for debugging**

Why it matters:
- 6 modules with no tracing = debug hell
- Incidents will take hours to diagnose
- Need to trace requests across GoAssist → GoAgent → GoControl → GoConnect

Tools: OpenTelemetry, Jaeger, or similar

---

## Products

### Build GoCRM (personal use)
**Type: Internal tool**

Purpose: Personal CRM for tracking contacts, deals, pipeline

Would integrate with:
- GoConnect for transport
- GoAgent for automation
- GoControl for permissions

---

### Build GoExpand product
Details: TBD - need user input on scope and purpose

---

## Decisions

### Decision: Deploy to Vercel vs Self-host
Details: TBD - need to evaluate Vercel deployment vs self-hosted infrastructure

---

## Prompts to Create

### Sales Tactics prompt
Details: TBD - need user input on specific use case

### GoControl prompt
Details: TBD - need user input on specific use case

### Segmentation prompt (reduce churn)
Details: TBD - need user input on specific use case

### Reduce Churn prompt
Details: TBD - need user input on specific use case

### Karpathy "Orchestrators" prompt
Details: Paste prompt from YouTube video about Karpathy and how we're becoming orchestrators (not coders)

---

## Key Architecture Risks (from ecosystem review)

1. **GoControl as Single Point of Failure** - Every action requires authorization. If slow/down, everything stops.
2. **Transport/Memory Boundary Collision** - GoConnect transcripts vs GoMemory recall will merge accidentally.
3. **Capability Inflation in GoAgent** - Easy to add tools, hard to remove. Each is attack surface.
4. **GoAssist Authority Creep** - User pressure will push toward direct execution.
5. **Audit Gap** - No single source of truth for what happened.

## Non-Negotiable Rules

- GoVertical is design-time ONLY - never runtime
- GoAssist can request, never execute
- GoControl is ultimate authority for all permissions
- GoMemory provides context, NOT authority
- GoConnect is transport only, not business logic
- GoAgent executes only within granted capabilities
- No module bypasses GoControl for tool access

---
Last updated: 2026-01-04
