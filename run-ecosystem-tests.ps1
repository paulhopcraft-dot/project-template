# Ecosystem Test Runner
# Runs all tests across all projects and generates a summary report

param(
    [switch]$Verbose,
    [switch]$StopOnFail,
    [string]$Project = "all"
)

$ErrorActionPreference = "Continue"

# Define all projects with their test commands
$projects = @(
    @{
        Name = "gocontrol"
        Path = "C:\Dev\gocontrol"
        Type = "python"
        TestCmd = "pytest -v"
        Priority = "HIGH"
    },
    @{
        Name = "gpnet3"
        Path = "C:\Dev\gpnet3"
        Type = "node"
        TestCmd = "npm run test"
        E2ECmd = "npm run test:e2e"
        Priority = "HIGH"
    },
    @{
        Name = "govertical"
        Path = "C:\Dev\govertical"
        Type = "node"
        TestCmd = "npm run test"
        Priority = "LOW"
    },
    @{
        Name = "goconnect"
        Path = "C:\Dev\goconnect"
        Type = "node"
        TestCmd = "npm run test"
        Priority = "MEDIUM"
    },
    @{
        Name = "GoAgent"
        Path = "C:\Dev\GoAgent"
        Type = "node"
        TestCmd = "npm run test"
        Priority = "MEDIUM"
    },
    @{
        Name = "gomemory"
        Path = "C:\Dev\gomemory"
        Type = "python"
        TestCmd = "pytest -v"
        Priority = "MEDIUM"
    },
    @{
        Name = "goassist3"
        Path = "C:\Dev\goassist3"
        Type = "node"
        TestCmd = "npm run test"
        Priority = "LOW"
    }
)

# Results storage
$results = @()
$startTime = Get-Date

Write-Host "`n" -NoNewline
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║               ECOSYSTEM TEST RUNNER                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Filter projects if specific one requested
if ($Project -ne "all") {
    $projects = $projects | Where-Object { $_.Name -eq $Project }
    if ($projects.Count -eq 0) {
        Write-Host "Project '$Project' not found!" -ForegroundColor Red
        exit 1
    }
}

# Run tests for each project
foreach ($proj in $projects) {
    $projectPath = $proj.Path
    $projectName = $proj.Name

    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    Write-Host "[$($proj.Priority)] $projectName" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

    if (-not (Test-Path $projectPath)) {
        Write-Host "  [WARN] Project path not found: $projectPath" -ForegroundColor Red
        $results += @{
            Project = $projectName
            Priority = $proj.Priority
            Status = "NOT_FOUND"
            Duration = 0
            Details = "Path not found"
        }
        continue
    }

    Push-Location $projectPath
    $testStart = Get-Date

    try {
        if ($proj.Type -eq "python") {
            # Python project - use pytest
            if (Test-Path "pyproject.toml") {
                Write-Host "  Running: pytest" -ForegroundColor Gray
                if ($Verbose) {
                    $output = & pytest -v 2>&1
                } else {
                    $output = & pytest 2>&1
                }
                $exitCode = $LASTEXITCODE
            } else {
                Write-Host "  [WARN] No pyproject.toml found" -ForegroundColor Yellow
                $exitCode = 1
                $output = "No configuration found"
            }
        }
        elseif ($proj.Type -eq "node") {
            # Node project - use npm test
            if (Test-Path "package.json") {
                Write-Host "  Running: npm test" -ForegroundColor Gray
                if ($Verbose) {
                    $output = & npm test 2>&1
                } else {
                    $output = & npm test 2>&1
                }
                $exitCode = $LASTEXITCODE
            } else {
                Write-Host "  [WARN] No package.json found" -ForegroundColor Yellow
                $exitCode = 1
                $output = "No configuration found"
            }
        }

        $testEnd = Get-Date
        $duration = ($testEnd - $testStart).TotalSeconds

        if ($exitCode -eq 0) {
            Write-Host "  [PASS] PASSED" -ForegroundColor Green
            Write-Host "  Duration: $([math]::Round($duration, 1))s" -ForegroundColor Gray
            $status = "PASSED"
        } else {
            Write-Host "  [FAIL] FAILED" -ForegroundColor Red
            Write-Host "  Duration: $([math]::Round($duration, 1))s" -ForegroundColor Gray
            $status = "FAILED"

            if ($Verbose) {
                Write-Host "`n  Output:" -ForegroundColor Gray
                $output | ForEach-Object { Write-Host "    $_" }
            }

            if ($StopOnFail) {
                Write-Host "`n  Stopping due to -StopOnFail" -ForegroundColor Red
                break
            }
        }

        $results += @{
            Project = $projectName
            Priority = $proj.Priority
            Status = $status
            Duration = [math]::Round($duration, 1)
            Details = if ($status -eq "FAILED") { ($output | Select-Object -Last 5) -join "`n" } else { "" }
        }

    } catch {
        Write-Host "  [ERR] ERROR: $_" -ForegroundColor Red
        $results += @{
            Project = $projectName
            Priority = $proj.Priority
            Status = "ERROR"
            Duration = 0
            Details = $_.Exception.Message
        }
    }

    Pop-Location
    Write-Host ""
}

# Summary
$endTime = Get-Date
$totalDuration = ($endTime - $startTime).TotalSeconds

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                       SUMMARY                                ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$passed = ($results | Where-Object { $_.Status -eq "PASSED" }).Count
$failed = ($results | Where-Object { $_.Status -eq "FAILED" }).Count
$errors = ($results | Where-Object { $_.Status -eq "ERROR" -or $_.Status -eq "NOT_FOUND" }).Count

foreach ($r in $results) {
    $icon = switch ($r.Status) {
        "PASSED" { "[PASS]" }
        "FAILED" { "[FAIL]" }
        "ERROR" { "[ERR ]" }
        "NOT_FOUND" { "[MISS]" }
        default { "[????]" }
    }
    $color = switch ($r.Status) {
        "PASSED" { "Green" }
        "FAILED" { "Red" }
        "ERROR" { "Yellow" }
        "NOT_FOUND" { "Gray" }
        default { "White" }
    }

    $line = "  $icon $($r.Project.PadRight(15)) [$($r.Priority.PadRight(6))] $($r.Status.PadRight(10)) $($r.Duration)s"
    Write-Host $line -ForegroundColor $color
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$totalColor = if ($failed -eq 0 -and $errors -eq 0) { "Green" } elseif ($failed -gt 0) { "Red" } else { "Yellow" }
Write-Host "  TOTAL: $passed passed, $failed failed, $errors errors" -ForegroundColor $totalColor
Write-Host "  TIME:  $([math]::Round($totalDuration, 1)) seconds" -ForegroundColor Gray
Write-Host ""

# Exit code based on results
if ($failed -gt 0 -or $errors -gt 0) {
    exit 1
} else {
    exit 0
}
