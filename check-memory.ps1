$os = Get-CimInstance Win32_OperatingSystem
$usedGB = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory)/1MB, 1)
$totalGB = [math]::Round($os.TotalVisibleMemorySize/1MB, 1)
$pct = [math]::Round($usedGB/$totalGB*100, 0)

Write-Host "RAM: $usedGB GB / $totalGB GB ($pct% used)" -ForegroundColor Cyan

Write-Host "`nTop processes:" -ForegroundColor Yellow
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 Name, @{N='MB';E={[math]::Round($_.WorkingSet64/1MB,0)}} | Format-Table -AutoSize
