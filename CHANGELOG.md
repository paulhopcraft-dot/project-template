# Changelog

All notable changes to Claude Code Toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.3.0] - 2025-12-25

### Added - Advanced Agent System 🤖
- **Agent Registry**: Central registry system for custom agents with conditional triggering
- **Specialist Agents**: Three production-ready agents with expert capabilities:
  - `healthcare-validator`: HIPAA compliance, PHI detection, evidence chain validation
  - `test-specialist`: Test generation, coverage analysis, edge case discovery
  - `code-reviewer`: Security analysis (OWASP Top 10), code quality, performance review
- **Agent Chaining**: Sequential, parallel, and conditional agent execution via chain engine
- **Domain Detection**: Auto-detects healthcare, revenue, or general domains from project files
- **Migration Script**: `migrate-to-agents.sh` upgrades existing projects to agent system
- **Healthcare Domain Templates**: Evidence schema, compliance checklist, gpnet-healthcare skill
- **Domain Configuration**: `.claude/domain.json` for project-specific agent configuration

### Enhanced
- **Setup Wizard**: Added optional Advanced Agent System installation (Step 7.5)
- **Command Integration**: Four commands now trigger agents when available:
  - `/verify`: Runs full-verification chain (test-specialist → code-reviewer → domain agent)
  - `/review`: Uses code-reviewer agent for expert-level code review
  - `/tdd`: Uses test-specialist agent for comprehensive test guidance
  - `/prd-check`: Conditionally triggers healthcare-validator for compliance validation
- **All 32 Commands**: Converted to XML-enhanced format for better Claude parsing
- **CLAUDE.md**: Added Autonomous Mode documentation across all projects

### Agent Capabilities
- **Healthcare Validator**:
  - Scans for 18 HIPAA PHI identifiers (SSN, MRN, DOB, etc.)
  - Validates HIPAA Security Rule compliance (encryption, access controls, audit logging)
  - Verifies evidence chain completeness (who, what, when, why, where, how)
  - Checks CMS claims processing requirements
- **Test Specialist**:
  - Generates unit, integration, and E2E tests using AAA pattern
  - Identifies untested code paths and missing branch coverage
  - Discovers edge cases (boundaries, null, empty, errors, concurrency)
  - Reviews test quality (clarity, independence, brittleness)
- **Code Reviewer**:
  - Security: SQL injection, XSS, CSRF, auth vulnerabilities, secret detection
  - Quality: DRY, SOLID, complexity analysis (cyclomatic < 10), code smells
  - Performance: N+1 queries, caching opportunities, algorithmic complexity
  - Maintainability: Naming conventions, documentation, modularity

### Backwards Compatibility
- ✅ All existing commands work unchanged without agent system
- ✅ Agent system is optional (can be installed or skipped in setup wizard)
- ✅ Commands fall back to original behavior if agents not installed
- ✅ Zero breaking changes to existing workflows

### Domain Configurations
- **gpnet3**: Configured as healthcare domain with HIPAA compliance automation
- **goassist3**: Configured as general development domain with quality gates

### Documentation
- `agents/chain-engine.md`: Comprehensive agent chaining documentation
- `agents/definitions/*.md`: Three agent definition templates with XML structure
- `.claude/domains/healthcare/`: Evidence schema, compliance checklist templates

### Migration
Run `bash migrate-to-agents.sh` in existing projects to upgrade to agent system.

## [2.2.0] - 2025-12-24

### Added
- GitHub issue templates (bug report, feature request)
- Pull request template
- CONTRIBUTING.md with development guidelines
- Pre-commit hooks configuration
- VSCode workspace settings and recommended extensions
- Docker templates (Dockerfile, docker-compose.yml)
- Database migration templates (Alembic, Prisma, golang-migrate)

## [2.0.0] - 2025-12-23

### Added
- **JSON Schema Validation**: features.json now validates against schema automatically
- **Test Templates**: Ready-to-use test setups for Python (pytest), TypeScript/Node (Vitest/Jest), and Go
- **CI/CD Workflows**: GitHub Actions templates with security scanning for Python and Node.js
- **Recovery Commands**: `/recover` command to diagnose and fix broken states, corrupted files, git issues
- **Validation Command**: `/validate-features` with schema checking and auto-fix capabilities
- **Help System**: `/help` command with search functionality to find commands by keyword
- **Comprehensive .gitignore**: Multi-stack gitignore covering Python, Node, Go, Rust with security best practices
- **Environment Template**: .env.example with all common services (Supabase, AWS, OpenAI, Stripe, etc.)
- **Branching Strategy Guide**: Complete guide in docs/BRANCHING-STRATEGY.md covering trunk-based and git-flow
- **Frontend Design Skill**: Anthropic's official UI design skill for distinctive interfaces

### Changed
- **Setup Wizard**: Now automatically copies all 30+ commands and skills (previously only created 4 basic commands)
- **Setup Wizard**: Auto-detects toolkit location for reliable installation
- **Command Organization**: Removed .claude/commands duplication, commands/ is now single source of truth
- **LICENSE**: Updated with proper copyright holder
- **README.md**: Added v2.0 features section with comprehensive command listing
- **TOOLKIT-OVERVIEW.md**: Updated structure to reflect new templates and organization

### Fixed
- Setup wizard now correctly copies all commands and skills
- Command installation process is fully automated
- Features.json now includes schema reference for validation

### Enhanced
- pytest.ini with coverage, markers, logging, and best practices
- features.json template with schema reference and extended fields
- Documentation with production-ready examples
- Error messages and diagnostic output

## [1.0.0] - 2025-12-13

### Added
- Initial release of Claude Code Toolkit
- Core slash commands: continue, status, verify, handoff, review, branch, add-feature
- PRD enforcement commands: prd-check, build-prd, edit-prd, design-prd
- Decision-making commands: decide, constraints, perspectives
- Thinking commands: think, think-parallel, anticipate, reflect
- Context management commands: context, fresh, reload, last
- Delegation commands: delegate, expert, index
- features.json tracking system with red→green pattern
- CLAUDE.md template for project instructions
- claude-progress.txt for session continuity
- setup-wizard.sh for automated project setup
- engineering-mode skill with global code quality standards
- prompt-spec-ready.md for Browser Claude integration
- prompt-existing-project.md for retrofitting existing codebases
- prompt-harness.md for long-running agent patterns
- BEGINNERS-GUIDE.md for non-technical users
- QUICK-REFERENCE.md cheat sheet
- TOOLKIT-OVERVIEW.md comprehensive documentation

### Core Concepts
- Red → Green pattern (features start with passes: false)
- Session continuity through progress tracking
- Browser Claude (Opus) for planning, Claude Code (Sonnet) for building
- Verification-first approach (never mark complete without testing)
- JSON-based feature tracking over markdown

---

## Version History Summary

| Version | Date | Major Changes |
|---------|------|---------------|
| 2.0.0 | 2025-12-23 | Production-ready: schemas, tests, CI/CD, recovery tools |
| 1.0.0 | 2025-12-13 | Initial release with 30+ commands and core workflow |

---

## Migration Guides

### Migrating from 1.0 to 2.0

**Breaking Changes**: None - v2.0 is fully backward compatible

**New Features to Adopt**:
1. **Add schema to existing features.json**:
   ```json
   {
     "$schema": "./features.schema.json",
     ...
   }
   ```

2. **Copy new templates**:
   ```bash
   cp toolkit/templates/features.schema.json your-project/
   cp toolkit/templates/.gitignore your-project/
   cp toolkit/templates/.env.example your-project/
   ```

3. **Use new commands**:
   - `/validate-features` - Check your features.json
   - `/recover` - Fix issues when things break
   - `/help` - Find commands quickly

4. **Optional: Add CI/CD**:
   ```bash
   cp -r toolkit/templates/.github/ your-project/
   ```

5. **Optional: Add test templates**:
   ```bash
   cp -r toolkit/templates/tests/python/ your-project/tests/
   # or typescript, go depending on your stack
   ```

---

## Links

- [GitHub Repository](https://github.com/yourusername/claude-code-toolkit)
- [Issues](https://github.com/yourusername/claude-code-toolkit/issues)
- [Discussions](https://github.com/yourusername/claude-code-toolkit/discussions)
