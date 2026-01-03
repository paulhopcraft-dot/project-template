$projects = @('gpnet3', 'goassist3', 'govertical', 'goconnect', 'GoAgent', 'gomemory', 'gocontrol')

foreach ($proj in $projects) {
    $path = "C:\Dev\$proj\.claude"
    if (Test-Path $path) {
        $cmds = (Get-ChildItem "$path\commands\*.md" -EA 0).Count
        $skills = (Get-ChildItem "$path\skills" -Directory -EA 0).Count
        $lite = (Get-ChildItem "$path\lite\*.md" -EA 0).Count
        Write-Host "$proj : $cmds commands, $skills skills, $lite lite"
    } else {
        Write-Host "$proj : .claude folder missing" -ForegroundColor Red
    }
}
