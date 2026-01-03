$projects = @('claude-code-toolkit', 'gpnet3', 'goassist3', 'govertical', 'goconnect', 'GoAgent', 'gomemory', 'gocontrol')
$totalAdded = 0

foreach ($proj in $projects) {
    $path = "C:\Dev\$proj"
    if (Test-Path "$path\.git") {
        Push-Location $path
        # Exclude test files
        $stats = git log --since='3 days ago' --numstat --format='' -- . ':!*test*' ':!*spec*' ':!*.test.*' ':!*__tests__*' 2>$null
        $added = 0
        foreach ($line in $stats) {
            if ($line -match '^(\d+)\s+\d+') {
                $added += [int]$matches[1]
            }
        }
        $color = if ($added -gt 0) { 'Green' } else { 'Gray' }
        Write-Host "$proj : $added lines" -ForegroundColor $color
        $totalAdded += $added
        Pop-Location
    }
}
Write-Host ''
Write-Host "TOTAL: $totalAdded lines added (last 3 days, excluding tests)" -ForegroundColor Cyan
