# Simple Ecosystem Test Runner
param([string]$Project = "all")

$ErrorActionPreference = "Continue"

$projects = @(
    @{ Name = "gocontrol"; Path = "C:\Dev\gocontrol"; Type = "python"; Priority = "HIGH" },
    @{ Name = "gpnet3"; Path = "C:\Dev\gpnet3"; Type = "node"; Priority = "HIGH" },
    @{ Name = "govertical"; Path = "C:\Dev\govertical"; Type = "node"; Priority = "LOW" },
    @{ Name = "goconnect"; Path = "C:\Dev\goconnect"; Type = "node"; Priority = "MEDIUM" },
    @{ Name = "GoAgent"; Path = "C:\Dev\GoAgent"; Type = "node"; Priority = "MEDIUM" },
    @{ Name = "gomemory"; Path = "C:\Dev\gomemory"; Type = "python"; Priority = "MEDIUM" },
    @{ Name = "goassist3"; Path = "C:\Dev\goassist3"; Type = "node"; Priority = "LOW" }
)

$results = @()
$startTime = Get-Date

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ECOSYSTEM TEST RUNNER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($Project -ne "all") {
    $projects = $projects | Where-Object { $_.Name -eq $Project }
}

foreach ($proj in $projects) {
    Write-Host "----------------------------------------" -ForegroundColor Gray
    Write-Host "[$($proj.Priority)] $($proj.Name)" -ForegroundColor Yellow
    Write-Host "----------------------------------------" -ForegroundColor Gray

    if (-not (Test-Path $proj.Path)) {
        Write-Host "  MISSING: $($proj.Path)" -ForegroundColor Red
        $results += @{ Project = $proj.Name; Priority = $proj.Priority; Status = "MISSING"; Duration = 0 }
        continue
    }

    Push-Location $proj.Path
    $testStart = Get-Date

    try {
        if ($proj.Type -eq "python") {
            if (Test-Path "pyproject.toml") {
                Write-Host "  Running pytest..." -ForegroundColor Gray
                $output = & pytest -q 2>&1
                $exitCode = $LASTEXITCODE
            } else {
                Write-Host "  NO CONFIG" -ForegroundColor Yellow
                $exitCode = 1
            }
        }
        elseif ($proj.Type -eq "node") {
            if (Test-Path "package.json") {
                Write-Host "  Running npm test..." -ForegroundColor Gray
                $output = & npm test 2>&1
                $exitCode = $LASTEXITCODE
            } else {
                Write-Host "  NO CONFIG" -ForegroundColor Yellow
                $exitCode = 1
            }
        }

        $duration = ((Get-Date) - $testStart).TotalSeconds

        if ($exitCode -eq 0) {
            Write-Host "  PASSED ($([math]::Round($duration, 1))s)" -ForegroundColor Green
            $status = "PASSED"
        } else {
            Write-Host "  FAILED ($([math]::Round($duration, 1))s)" -ForegroundColor Red
            $status = "FAILED"
        }

        $results += @{
            Project = $proj.Name
            Priority = $proj.Priority
            Status = $status
            Duration = [math]::Round($duration, 1)
        }

    } catch {
        Write-Host "  ERROR: $_" -ForegroundColor Red
        $results += @{ Project = $proj.Name; Priority = $proj.Priority; Status = "ERROR"; Duration = 0 }
    }

    Pop-Location
    Write-Host ""
}

$totalDuration = ((Get-Date) - $startTime).TotalSeconds

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$passed = ($results | Where-Object { $_.Status -eq "PASSED" }).Count
$failed = ($results | Where-Object { $_.Status -eq "FAILED" }).Count
$errors = ($results | Where-Object { $_.Status -in @("ERROR", "MISSING") }).Count

foreach ($r in $results) {
    $color = switch ($r.Status) {
        "PASSED" { "Green" }
        "FAILED" { "Red" }
        default { "Yellow" }
    }
    $line = "  $($r.Project.PadRight(15)) [$($r.Priority.PadRight(6))] $($r.Status.PadRight(10)) $($r.Duration)s"
    Write-Host $line -ForegroundColor $color
}

Write-Host ""
Write-Host "TOTAL: $passed passed, $failed failed, $errors errors" -ForegroundColor $(if ($failed -eq 0 -and $errors -eq 0) { "Green" } else { "Red" })
Write-Host "TIME:  $([math]::Round($totalDuration, 1))s" -ForegroundColor Gray
Write-Host ""

if ($failed -gt 0 -or $errors -gt 0) { exit 1 } else { exit 0 }
