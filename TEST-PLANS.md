# Test Plans for Go Ecosystem

## Overview

| Project | Status | Priority | Test Focus |
|---------|--------|----------|------------|
| gocontrol | 80% | HIGH | Security, Auth, Kill Switch |
| gpnet3 | 60% | HIGH | PostgreSQL, API Endpoints |
| gomemory | 20% | MEDIUM | Core Functions, Storage |
| govertical | 100% | LOW | Regression Only |
| goconnect | 100% | LOW | Regression Only |
| GoAgent | 100% | LOW | Regression Only |
| goassist3 | 100% | LOW | Regression Only |

---

## Test Plan 1: gocontrol (Root of Trust)

### Critical Path Tests

```
SECURITY TESTS (Must Pass)
├── Authentication
│   ├── Valid token grants access
│   ├── Invalid token returns 401
│   ├── Expired token returns 401
│   └── Missing token returns 401
├── Authorization
│   ├── Admin can access all routes
│   ├── User blocked from admin routes
│   ├── Capability tokens enforced
│   └── Cross-project access denied
├── Kill Switch
│   ├── Kill switch stops target service
│   ├── Kill switch logs action
│   ├── Kill switch requires admin
│   └── Recovery after kill works
└── Audit Logging
    ├── All auth events logged
    ├── All admin actions logged
    └── Logs cannot be tampered
```

### API Endpoints (Thunder Client)

```json
// Collection: gocontrol-tests.json

// Test 1: Health Check
GET http://localhost:3000/health
Expected: 200 OK

// Test 2: Auth - Valid Login
POST http://localhost:3000/auth/login
Body: { "email": "admin@test.com", "password": "test123" }
Expected: 200, token returned

// Test 3: Auth - Invalid Login
POST http://localhost:3000/auth/login
Body: { "email": "wrong@test.com", "password": "wrong" }
Expected: 401 Unauthorized

// Test 4: Protected Route - No Token
GET http://localhost:3000/admin/dashboard
Expected: 401 Unauthorized

// Test 5: Protected Route - With Token
GET http://localhost:3000/admin/dashboard
Headers: Authorization: Bearer {{token}}
Expected: 200 OK

// Test 6: Kill Switch
POST http://localhost:3000/admin/kill
Body: { "service": "goassist3", "reason": "test" }
Expected: 200, service stopped
```

### Manual Verification Checklist

- [ ] Start gocontrol server
- [ ] Login as admin - verify token received
- [ ] Access protected route - verify works
- [ ] Logout - verify token invalidated
- [ ] Try accessing protected route - verify blocked
- [ ] Check audit log - verify all actions recorded
- [ ] Test kill switch on test service
- [ ] Verify kill switch logged

---

## Test Plan 2: gpnet3 (60% Complete)

### Database Tests (PostgreSQL)

```
DATABASE TESTS
├── Connection
│   ├── Connect to PostgreSQL
│   ├── Connection pooling works
│   └── Reconnect after failure
├── Migrations
│   ├── All migrations run successfully
│   ├── Rollback works
│   └── No duplicate migrations
├── CRUD Operations
│   ├── Create record succeeds
│   ├── Read record succeeds
│   ├── Update record succeeds
│   ├── Delete record succeeds
│   └── Transactions work correctly
└── Data Integrity
    ├── Foreign keys enforced
    ├── Unique constraints work
    └── Required fields validated
```

### API Endpoints (Thunder Client)

```json
// Collection: gpnet3-tests.json

// Test 1: Database Health
GET http://localhost:3001/health/db
Expected: 200, { "status": "connected" }

// Test 2: List Records
GET http://localhost:3001/api/records
Expected: 200, array of records

// Test 3: Create Record
POST http://localhost:3001/api/records
Body: { "name": "Test Record", "value": 123 }
Expected: 201 Created

// Test 4: Get Single Record
GET http://localhost:3001/api/records/1
Expected: 200, record object

// Test 5: Update Record
PUT http://localhost:3001/api/records/1
Body: { "name": "Updated Record" }
Expected: 200 OK

// Test 6: Delete Record
DELETE http://localhost:3001/api/records/1
Expected: 204 No Content

// Test 7: Invalid Request
POST http://localhost:3001/api/records
Body: { }
Expected: 400 Bad Request
```

### Manual Verification Checklist

- [ ] PostgreSQL container running
- [ ] Run migrations: `npm run db:migrate`
- [ ] Verify all tables created
- [ ] Test CRUD via API
- [ ] Check data in database directly
- [ ] Test error handling for invalid data

---

## Test Plan 3: gomemory (20% Complete - Scaffold)

### Core Function Tests

```
GOMEMORY TESTS
├── Storage
│   ├── Store memory entry
│   ├── Retrieve memory entry
│   ├── Update memory entry
│   ├── Delete memory entry
│   └── Search memories
├── Cross-Session
│   ├── Memory persists after restart
│   ├── Memory loads on startup
│   └── Memory not lost on crash
└── Integration
    ├── Claude can write memory
    ├── Claude can read memory
    └── Memory shared across projects
```

### Implementation Priority

Since gomemory is only 20% complete, focus on:

1. **Core Storage** - Basic save/load working
2. **Persistence** - Data survives restart
3. **API** - Simple endpoints for CRUD
4. **Integration** - Hook into other projects

---

## Test Plan 4: Regression Tests (100% Complete Projects)

### govertical (202 features)

Run weekly:
```bash
cd C:\Dev\govertical
npm test
# All 202 features should pass
```

### goconnect (99 features)

Run weekly:
```bash
cd C:\Dev\goconnect
npm test
# All 99 features should pass
```

### GoAgent (52 features)

Run weekly:
```bash
cd C:\Dev\GoAgent
npm test
# All 52 features should pass
```

### goassist3

Run weekly:
```bash
cd C:\Dev\goassist3
npm test
# All tests should pass
```

---

## VS Code Testing Workflow

### Jest (Unit Tests)

1. Open project in VS Code
2. Click Jest icon in sidebar
3. Click "Run All Tests"
4. View results in Test Explorer
5. Failed tests show inline in code

### Playwright (E2E Tests)

1. Open project in VS Code
2. Click Playwright icon in sidebar
3. Select browser (Chromium/Firefox/WebKit)
4. Click "Run Tests"
5. Watch test execution in browser
6. View report at `playwright-report/index.html`

### Thunder Client (API Tests)

1. Click Thunder icon in sidebar
2. Import collection (or create new)
3. Set environment variables
4. Click "Run All"
5. View pass/fail for each request
6. Export results as JSON

### ErrorLens (Inline Errors)

- Errors show directly on the line
- Warnings in yellow
- Info in blue
- No need to hover - visible immediately

---

## Automated Test Script

Save as `run-all-tests.ps1`:

```powershell
$projects = @(
    @{Name='gocontrol'; Path='C:\Dev\gocontrol'; Priority='HIGH'},
    @{Name='gpnet3'; Path='C:\Dev\gpnet3'; Priority='HIGH'},
    @{Name='gomemory'; Path='C:\Dev\gomemory'; Priority='MEDIUM'},
    @{Name='govertical'; Path='C:\Dev\govertical'; Priority='LOW'},
    @{Name='goconnect'; Path='C:\Dev\goconnect'; Priority='LOW'},
    @{Name='GoAgent'; Path='C:\Dev\GoAgent'; Priority='LOW'},
    @{Name='goassist3'; Path='C:\Dev\goassist3'; Priority='LOW'}
)

$results = @()

foreach ($proj in $projects) {
    if (Test-Path "$($proj.Path)\package.json") {
        Write-Host "`nTesting $($proj.Name) [$($proj.Priority)]..." -ForegroundColor Cyan
        Push-Location $proj.Path

        $output = npm test 2>&1
        $passed = $LASTEXITCODE -eq 0

        $results += @{
            Project = $proj.Name
            Priority = $proj.Priority
            Passed = $passed
        }

        if ($passed) {
            Write-Host "  PASSED" -ForegroundColor Green
        } else {
            Write-Host "  FAILED" -ForegroundColor Red
        }

        Pop-Location
    }
}

Write-Host "`n=== SUMMARY ===" -ForegroundColor Yellow
foreach ($r in $results) {
    $color = if ($r.Passed) { 'Green' } else { 'Red' }
    $status = if ($r.Passed) { 'PASS' } else { 'FAIL' }
    Write-Host "$($r.Project): $status" -ForegroundColor $color
}
```

---

## Quick Reference

| Task | Tool | Command |
|------|------|---------|
| Run unit tests | Jest | `npm test` |
| Run E2E tests | Playwright | `npx playwright test` |
| Test single API | Thunder Client | Click "Send" |
| Test all APIs | Thunder Client | "Run All" |
| View test coverage | Jest | `npm test -- --coverage` |
| Debug failing test | VS Code | Click "Debug" on test |

---

## Non-Technical User Guide

### How to Run Tests (Simple Steps)

1. **Open VS Code**
2. **Open Project** - File > Open Folder > select project
3. **Open Terminal** - View > Terminal
4. **Run Tests** - Type `npm test` and press Enter
5. **Read Results** - Green = passed, Red = failed

### What the Results Mean

- **All Passing**: Everything works correctly
- **Some Failing**: Those features are broken
- **All Failing**: Major issue (database down, config wrong)

### When to Test

- **Before committing**: Run `npm test`
- **After pulling changes**: Run `npm test`
- **Weekly**: Run all project tests
- **After deployments**: Run E2E tests

### If Tests Fail

1. Read the error message
2. Run `/status` in Claude Code
3. Ask Claude to fix it: "The tests are failing, can you fix them?"
