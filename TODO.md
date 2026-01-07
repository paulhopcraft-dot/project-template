# Todo List

## 🔥 Active Work
- [ ] **Review workplace safety signal system - Convert GPNet → Full whistleblower system**
  - Analyze current GPNet capabilities
  - Design whistleblower-specific features (anonymous reporting, case tracking, etc.)
  - Plan implementation approach
  - Status: Not started

---

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

## Marketing & Discoverability

### SEO & LLM Discoverability Strategy
**Priority: HIGH - Required for product adoption**

Each product needs to be discoverable by:
- Traditional search (Google, Bing)
- LLM search (ChatGPT, Claude, Perplexity, SearchGPT)
- AI agents looking for tools/services

#### GoVertical (Directory Platform)
**Target:** "Local business directories", "niche directories", "vertical directories"

Strategy:
- [ ] Traditional SEO
  - Schema.org LocalBusiness markup for all listings
  - OpenGraph + Twitter Card meta tags
  - XML sitemap generation (auto-update)
  - robots.txt optimization
  - Semantic HTML5 structure
  - Fast Core Web Vitals scores

- [ ] LLM Optimization
  - Structured data in JSON-LD format
  - Clear product descriptions in natural language
  - FAQ sections (what, why, how)
  - Use cases and examples
  - API documentation in markdown
  - Pricing page with clear value props

- [ ] Content Strategy
  - Blog posts: "How to build a directory", "Vertical vs horizontal directories"
  - Case studies with measurable outcomes
  - Integration guides for popular tools
  - Community forum for discussions

- [ ] Technical Implementation
  - Server-side rendering (SSR) for all pages
  - Static site generation (SSG) for directory pages
  - Pre-rendered meta tags
  - Canonical URLs
  - Breadcrumb navigation

#### GPNet3 (API Management)
**Target:** "API management tools", "API versioning", "API governance"

Strategy:
- [ ] Developer-focused SEO
  - Code examples in multiple languages
  - Interactive API playground
  - Comprehensive API documentation
  - GitHub presence with examples
  - npm/pip package with good README

- [ ] LLM Discoverability
  - Clear feature comparison vs competitors
  - Use cases: "When to use GPNet3"
  - Integration guides: Express, FastAPI, etc.
  - Troubleshooting guides
  - Changelog in semantic versioning

- [ ] Community Building
  - Discord/Slack for developers
  - Stack Overflow monitoring
  - GitHub Discussions enabled
  - Tutorial videos on YouTube
  - Dev.to blog posts

#### GoConnect (Communication Hub)
**Target:** "Multi-channel messaging", "unified inbox", "customer communication platform"

Strategy:
- [ ] Product-led SEO
  - Integration directory (Slack, Discord, Email, SMS)
  - Comparison pages: "GoConnect vs Intercom"
  - Feature pages: "Unified Inbox", "Message Routing"
  - Industry-specific landing pages

- [ ] LLM Citations
  - Press releases on integration launches
  - Partner co-marketing content
  - Customer testimonials with metrics
  - Security & compliance documentation
  - GDPR/CCPA compliance pages

- [ ] Content Marketing
  - "State of Customer Communication" report
  - Best practices guides
  - Integration how-tos
  - ROI calculator

#### GoControl (Authorization Platform)
**Target:** "API authorization", "permission management", "multi-tenant auth"

Strategy:
- [ ] Security-focused SEO
  - Security documentation (OAuth2, JWT, etc.)
  - Compliance certifications (SOC2, ISO)
  - Audit log examples
  - Threat model documentation
  - Zero-trust architecture guides

- [ ] Developer Trust Building
  - Open-source components on GitHub
  - Security advisories page
  - Penetration test reports (summary)
  - Bug bounty program
  - Architecture diagrams

- [ ] Enterprise Content
  - White papers on authorization patterns
  - Case studies: enterprise customers
  - Comparison: "Build vs Buy"
  - ROI analysis for security teams

#### GoMemory (Memory Service)
**Target:** "AI agent memory", "context management", "conversation history"

Strategy:
- [ ] AI-first SEO
  - Integration guides for Claude, GPT, Gemini
  - Memory architecture documentation
  - RAG (Retrieval Augmented Generation) guides
  - Vector database comparisons
  - Embedding strategies

- [ ] Technical Depth
  - Research papers on memory systems
  - Benchmarks vs competitors
  - Open-source SDKs
  - Example applications
  - Architecture patterns

- [ ] Developer Experience
  - Quick start in 5 minutes
  - Playground with live demo
  - Code templates for common use cases
  - Troubleshooting decision tree

#### GoAgent (Execution Platform)
**Target:** "AI agent platform", "tool calling", "agent orchestration"

Strategy:
- [ ] AI Platform SEO
  - Tool library showcase
  - Agent examples and templates
  - Integration marketplace
  - Use case gallery
  - Performance benchmarks

- [ ] Developer Ecosystem
  - Public tool registry
  - Community-contributed tools
  - Agent templates repository
  - Tutorial series
  - Certification program

- [ ] Thought Leadership
  - Research blog on agent patterns
  - Conference talks
  - Open-source reference implementations
  - Podcast appearances

#### GoAssist (User Interface)
**Target:** "AI assistant", "conversational UI", "chat interface"

Strategy:
- [ ] User-focused SEO
  - Use case pages by industry
  - "How it works" explainer
  - Privacy & data handling
  - Customization showcase
  - Widget demos

- [ ] Product Marketing
  - Free tier for testing
  - Live demo on homepage
  - Customer success stories
  - Video testimonials
  - Feature comparison matrix

---

## Universal Tactics (All Products)

- [ ] **LLM Training Data Presence**
  - Ensure documentation is crawlable
  - Create Wikipedia page (if notable)
  - Get mentioned in authoritative sources
  - GitHub README files comprehensive
  - Stack Overflow answers referencing products

- [ ] **Structured Data**
  - Product schema.org markup
  - SoftwareApplication type
  - Review/rating markup
  - FAQ schema
  - BreadcrumbList schema

- [ ] **Social Proof**
  - Product Hunt launch
  - Y Combinator News posts
  - Reddit AMAs and discussions
  - LinkedIn articles
  - Twitter/X presence

- [ ] **AI Agent Accessibility**
  - Public APIs with OpenAPI specs
  - Clear pricing on main page
  - Getting started < 5 minutes
  - Free tier or trial available
  - Documentation as markdown (not PDFs)

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

### Build Papua New Guinea Compliance/Regulation System
**Type: Compliance tracking system**
**Source: Mentioned by Lisa**

Purpose: Compliance or regulation system for Papua New Guinea

Details: TBD - need to clarify with Lisa:
- What specific compliance/regulation area?
- Industry sector (mining, forestry, finance, etc.)?
- Regulatory body requirements?
- Tracking vs reporting vs enforcement?

Would potentially integrate with:
- GoControl for authorization/audit
- GoConnect for notifications
- GoAgent for automation

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
