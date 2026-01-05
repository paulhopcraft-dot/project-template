<#
.SYNOPSIS
    Morning Brief - Fetch recent AI videos from configured YouTube channels

.DESCRIPTION
    Reads channels from toolkit-config.yaml and fetches recent videos using yt-dlp.
    Outputs a markdown file that Claude can read and summarize.

.EXAMPLE
    .\morning-brief.ps1
    .\morning-brief.ps1 -Hours 48
    .\morning-brief.ps1 -Channel "@ycombinator"

.NOTES
    Requires: yt-dlp (install via: winget install yt-dlp or pip install yt-dlp)
#>

param(
    [int]$Hours = 24,
    [string]$Channel = "",
    [switch]$Install
)

$ErrorActionPreference = "Stop"

# Check for yt-dlp
$ytdlp = Get-Command yt-dlp -ErrorAction SilentlyContinue
if (-not $ytdlp) {
    Write-Host ""
    Write-Host "yt-dlp is not installed." -ForegroundColor Red
    Write-Host ""
    Write-Host "Install options:" -ForegroundColor Yellow
    Write-Host "  winget install yt-dlp"
    Write-Host "  pip install yt-dlp"
    Write-Host "  choco install yt-dlp"
    Write-Host ""

    if ($Install) {
        Write-Host "Attempting to install via winget..." -ForegroundColor Cyan
        winget install yt-dlp
        exit 0
    }
    exit 1
}

# Read config
$configPath = Join-Path $PSScriptRoot "toolkit-config.yaml"
if (-not (Test-Path $configPath)) {
    Write-Host "Config not found: $configPath" -ForegroundColor Red
    exit 1
}

# Simple YAML parsing for channels (avoiding external dependencies)
$configContent = Get-Content $configPath -Raw
$channels = @()

# Extract channels from YAML
$inChannels = $false
foreach ($line in (Get-Content $configPath)) {
    if ($line -match '^\s*channels:') {
        $inChannels = $true
        continue
    }
    if ($inChannels) {
        if ($line -match '^\s*-\s*"?@?([^"]+)"?') {
            $ch = $Matches[1].Trim()
            if ($ch -notmatch '^(max_videos|lookback|summary)') {
                $channels += $ch
            }
        }
        if ($line -match '^\s*\w+:' -and $line -notmatch '^\s*-') {
            $inChannels = $false
        }
    }
}

# Filter to specific channel if requested
if ($Channel) {
    $Channel = $Channel -replace '^@', ''
    $channels = @($Channel)
}

if ($channels.Count -eq 0) {
    Write-Host "No channels found in config" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "MORNING BRIEF" -ForegroundColor Cyan
Write-Host "=============" -ForegroundColor Cyan
Write-Host "Channels: $($channels -join ', ')"
Write-Host "Lookback: $Hours hours"
Write-Host ""

# Create briefs directory
$briefsDir = Join-Path $PSScriptRoot "briefs"
if (-not (Test-Path $briefsDir)) {
    New-Item -ItemType Directory -Path $briefsDir | Out-Null
}

$date = Get-Date -Format "yyyy-MM-dd"
$outputFile = Join-Path $briefsDir "$date.md"
$cutoffDate = (Get-Date).AddHours(-$Hours)

# Start markdown output
$output = @()
$output += "# Morning AI Brief - $date"
$output += ""
$output += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
$output += "Lookback: $Hours hours"
$output += ""

$totalVideos = 0

foreach ($channel in $channels) {
    $channelName = $channel -replace '^@', ''
    Write-Host "Fetching: @$channelName..." -ForegroundColor Yellow

    $output += "## @$channelName"
    $output += ""

    try {
        # Get recent videos from channel
        $url = "https://www.youtube.com/@$channelName/videos"

        # yt-dlp to list videos (not download)
        $videos = yt-dlp --flat-playlist --print "%(upload_date)s|%(title)s|%(url)s" `
            --playlist-end 10 `
            --no-warnings `
            $url 2>$null

        if ($videos) {
            $videoCount = 0
            foreach ($video in $videos) {
                $parts = $video -split '\|', 3
                if ($parts.Count -ge 3) {
                    $uploadDate = $parts[0]
                    $title = $parts[1]
                    $videoUrl = $parts[2]

                    # Parse date (YYYYMMDD format)
                    if ($uploadDate -match '^\d{8}$') {
                        $videoDate = [DateTime]::ParseExact($uploadDate, "yyyyMMdd", $null)

                        if ($videoDate -ge $cutoffDate.Date) {
                            $output += "- **$title**"
                            $output += "  - Date: $($videoDate.ToString('yyyy-MM-dd'))"
                            $output += "  - URL: $videoUrl"
                            $output += ""
                            $videoCount++
                            $totalVideos++
                        }
                    }
                    elseif ($uploadDate -eq "NA") {
                        # Date not available - include video (can't filter by date)
                        $output += "- **$title**"
                        $output += "  - Date: Unknown (recent)"
                        $output += "  - URL: $videoUrl"
                        $output += ""
                        $videoCount++
                        $totalVideos++
                    }
                }
            }

            if ($videoCount -eq 0) {
                $output += "_No videos in the last $Hours hours_"
                $output += ""
            }

            Write-Host "  Found $videoCount recent videos" -ForegroundColor Green
        }
        else {
            $output += "_Could not fetch videos_"
            $output += ""
            Write-Host "  No videos found" -ForegroundColor Gray
        }
    }
    catch {
        $output += "_Error fetching: $($_.Exception.Message)_"
        $output += ""
        Write-Host "  Error: $_" -ForegroundColor Red
    }
}

# Summary section
$output += "---"
$output += ""
$output += "## Summary"
$output += ""
$output += "Total videos found: $totalVideos"
$output += ""
$output += "### For Claude"
$output += ""
$output += "Read this file and provide:"
$output += "1. Top 3 most relevant videos for an AI agent platform builder"
$output += "2. Key insights across all videos"
$output += "3. Any action items or things to watch later"
$output += ""

# Write output
$output | Out-File -FilePath $outputFile -Encoding UTF8

Write-Host ""
Write-Host "Brief saved to: $outputFile" -ForegroundColor Green
Write-Host ""
Write-Host "Next: Ask Claude to 'read briefs/$date.md and summarize'" -ForegroundColor Cyan
Write-Host ""
