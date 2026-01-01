# Launch All Projects - With Window Titles
# Opens 5 separate Windows Terminal windows with project names in title bar

$projects = @("gpnet3", "goassist3", "govertical", "goconnect", "GoAgent")

Write-Host "Launching Claude Code sessions..." -ForegroundColor Cyan

foreach ($proj in $projects) {
    $path = "C:\Dev\$proj"

    if (Test-Path $path) {
        Write-Host "  Starting $proj..." -ForegroundColor Green
        # --title sets the tab/window title to the project name
        Start-Process wt -ArgumentList "--title `"$proj`" -d `"$path`" cmd /k claude --continue"
        Start-Sleep -Milliseconds 800
    } else {
        Write-Host "  Skipping $proj - path not found" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "All sessions launched!" -ForegroundColor Cyan
Write-Host "Each window title shows the project name." -ForegroundColor Gray
