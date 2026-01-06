$projects = @('gpnet3', 'goassist3', 'govertical', 'goconnect', 'GoAgent', 'gomemory', 'gocontrol')

foreach ($proj in $projects) {
    $dest = "C:\Dev\$proj"
    if (Test-Path $dest) {
        Write-Host "Copying to $proj..." -ForegroundColor Green

        # Copy CLAUDE.md
        Copy-Item 'C:\Dev\claude-code-toolkit\CLAUDE.md' "$dest\CLAUDE.md" -Force

        # Copy toolkit-config.yaml
        Copy-Item 'C:\Dev\claude-code-toolkit\toolkit-config.yaml' "$dest\toolkit-config.yaml" -Force

        # Copy GUIDED-WORKFLOW.md
        Copy-Item 'C:\Dev\claude-code-toolkit\GUIDED-WORKFLOW.md' "$dest\GUIDED-WORKFLOW.md" -Force

        # Copy transcribe-video.ps1
        Copy-Item 'C:\Dev\claude-code-toolkit\transcribe-video.ps1' "$dest\transcribe-video.ps1" -Force

        # Ensure .claude folder exists
        if (!(Test-Path "$dest\.claude")) {
            New-Item -ItemType Directory -Path "$dest\.claude" -Force | Out-Null
        }

        # Copy commands folder (remove old first)
        if (Test-Path "$dest\.claude\commands") {
            Remove-Item "$dest\.claude\commands" -Recurse -Force
        }
        Copy-Item 'C:\Dev\claude-code-toolkit\.claude\commands' "$dest\.claude\commands" -Recurse -Force

        # Copy skills folder (remove old first)
        if (Test-Path "$dest\.claude\skills") {
            Remove-Item "$dest\.claude\skills" -Recurse -Force
        }
        Copy-Item 'C:\Dev\claude-code-toolkit\.claude\skills' "$dest\.claude\skills" -Recurse -Force

        # Copy lite folder (remove old first)
        if (Test-Path "$dest\.claude\lite") {
            Remove-Item "$dest\.claude\lite" -Recurse -Force
        }
        Copy-Item 'C:\Dev\claude-code-toolkit\.claude\lite' "$dest\.claude\lite" -Recurse -Force

        Write-Host "  Done: CLAUDE.md, toolkit-config.yaml, GUIDED-WORKFLOW.md, transcribe-video.ps1 + .claude/{commands,skills,lite}" -ForegroundColor Gray
    } else {
        Write-Host "Skipped $proj (not found)" -ForegroundColor Yellow
    }
}

Write-Host "`nAll projects updated!" -ForegroundColor Cyan
