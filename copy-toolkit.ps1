$projects = @('gpnet3', 'goassist3', 'govertical', 'goconnect', 'GoAgent')

foreach ($proj in $projects) {
    $dest = "C:\Dev\$proj"
    if (Test-Path $dest) {
        Write-Host "Copying to $proj..." -ForegroundColor Green

        # Copy CLAUDE.md
        Copy-Item 'C:\Dev\claude-code-toolkit\CLAUDE.md' "$dest\CLAUDE.md" -Force

        # Ensure .claude folder exists
        if (!(Test-Path "$dest\.claude")) {
            New-Item -ItemType Directory -Path "$dest\.claude" -Force | Out-Null
        }

        # Copy commands folder (remove old first)
        if (Test-Path "$dest\.claude\commands") {
            Remove-Item "$dest\.claude\commands" -Recurse -Force
        }
        Copy-Item 'C:\Dev\claude-code-toolkit\.claude\commands' "$dest\.claude\commands" -Recurse -Force

        Write-Host "  Done: CLAUDE.md + .claude/commands" -ForegroundColor Gray
    } else {
        Write-Host "Skipped $proj (not found)" -ForegroundColor Yellow
    }
}

Write-Host "`nAll projects updated!" -ForegroundColor Cyan
