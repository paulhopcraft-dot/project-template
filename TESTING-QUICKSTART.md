# Testing Quick Start Guide

## Your Test Infrastructure

| Project | Framework | Command | Status |
|---------|-----------|---------|--------|
| gocontrol | pytest | `pytest -v` | 13+ tests ready |
| gpnet3 | Vitest + Playwright | `npm test` / `npm run test:e2e` | Configured |
| govertical | Vitest | `npm test` | Framework ready, no tests |
| goconnect | Jest | `npm test` | 15+ tests ready |
| GoAgent | Vitest | `npm test` | 1+ test ready |
| gomemory | pytest | `pytest -v` | 14 tests ready |

---

## Quick Commands

### Run All Tests (Ecosystem)
```powershell
.\run-ecosystem-tests.ps1
```

### Run Single Project
```powershell
.\run-ecosystem-tests.ps1 -Project gocontrol
```

### Verbose Output (Show Failures)
```powershell
.\run-ecosystem-tests.ps1 -Verbose
```

### Stop on First Failure
```powershell
.\run-ecosystem-tests.ps1 -StopOnFail
```

---

## VS Code Extension Usage

### Jest Extension (Node.js projects)
1. Open any `.test.ts` or `.spec.ts` file
2. Click the green play button next to test names
3. Or click the beaker icon in sidebar → Run All Tests

### Playwright Extension (E2E tests)
1. Click Playwright icon in sidebar (looks like a theater mask)
2. Select browser (Chromium/Firefox/WebKit)
3. Click "Run All Tests" or individual tests
4. Watch tests execute in browser window

### Thunder Client (API tests)
1. Click Thunder icon in sidebar (lightning bolt)
2. Import collection: `test-collections/gocontrol-api.json`
3. Select "Local" environment
4. Click "Run All" to execute all requests
5. Green = passed, Red = failed

### ErrorLens
- Errors appear inline in your code (red)
- Warnings appear inline (yellow)
- No action needed - just code!

---

## Import Thunder Client Collections

1. Open Thunder Client (sidebar)
2. Click "Collections" tab
3. Click "Import" button
4. Select files from `claude-code-toolkit/test-collections/`:
   - `gocontrol-api.json`
   - `gpnet3-api.json`
   - `goconnect-api.json`

---

## Project-Specific Testing

### gocontrol (Python)
```powershell
cd C:\Dev\gocontrol

# Run all tests
pytest -v

# Run specific category
pytest tests/integration/ -v

# Run with coverage
pytest --cov=src --cov-report=html
```

### gpnet3 (Node + Playwright)
```powershell
cd C:\Dev\gpnet3

# Unit tests
npm test

# E2E tests (headless)
npm run test:e2e

# E2E tests (see browser)
npm run test:e2e:headed
```

### goconnect (Node + Jest)
```powershell
cd C:\Dev\goconnect

# All tests
npm test

# With coverage
npm test -- --coverage
```

### gomemory (Python)
```powershell
cd C:\Dev\gomemory

# Run all tests
pytest -v

# Run specific test file
pytest tests/api/test_audio_upload.py -v
```

---

## Adding Tests to govertical

govertical has Vitest configured but no tests. To add tests:

1. Create test file:
```typescript
// tests/example.test.ts
import { describe, it, expect } from 'vitest'

describe('Example', () => {
  it('should work', () => {
    expect(1 + 1).toBe(2)
  })
})
```

2. Run tests:
```powershell
npm test
```

---

## Adding E2E Tests

Use the templates in `claude-code-toolkit/templates/`:

1. Copy `playwright.config.ts` to project root
2. Create `tests/e2e/` folder
3. Copy `example.e2e.spec.ts` and customize
4. Install Playwright:
```powershell
npm install -D @playwright/test
npx playwright install
```

---

## Test Priorities

| Priority | Projects | When to Test |
|----------|----------|--------------|
| **HIGH** | gocontrol, gpnet3 | Before every commit |
| **MEDIUM** | goconnect, GoAgent, gomemory | Weekly |
| **LOW** | govertical | After changes only |

---

## Troubleshooting

### "Tests not found"
- Check test file naming: `*.test.ts`, `*.spec.ts`, `test_*.py`
- Verify test directory matches config

### "Module not found"
```powershell
npm install  # or
pip install -e .
```

### "Database connection failed"
- Start required services (PostgreSQL, Redis)
- Check `.env` file exists with correct values

### "Port already in use"
```powershell
# Find what's using the port
netstat -ano | findstr :3000
# Kill the process
taskkill /PID <pid> /F
```

---

## Next Steps

1. Run `.\run-ecosystem-tests.ps1` to see current status
2. Import Thunder Client collections for API testing
3. Fix any failing tests before new development
4. Add tests before adding features (TDD)
