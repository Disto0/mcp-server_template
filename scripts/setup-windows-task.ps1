<#
.SYNOPSIS
    Registers a Windows Task Scheduler task that starts the MCP server
    (streamable-http transport) automatically at user logon.

.DESCRIPTION
    The task runs:  uv run mcp-server-template --transport streamable-http
    from the project root (the parent directory of this script), so it works
    no matter where the project folder is located.

    The task is created for the CURRENT user, at logon, and restarts
    automatically if the process exits unexpectedly (up to 3 times).

.PARAMETER TaskName
    Name of the scheduled task. Default: "MCP Server Template".

.PARAMETER Port
    Port for the HTTP transport. Default: 8000.

.PARAMETER Remove
    Remove the scheduled task instead of creating it.

.EXAMPLE
    # Create the task (default name/port):
    pwsh ./scripts/setup-windows-task.ps1

    # Custom port:
    pwsh ./scripts/setup-windows-task.ps1 -Port 9000

    # Remove the task:
    pwsh ./scripts/setup-windows-task.ps1 -Remove
#>
[CmdletBinding()]
param(
    [string]$TaskName = "MCP Server Template",
    [int]$Port = 8000,
    [switch]$Remove
)

$ErrorActionPreference = "Stop"

# Project root = parent of the scripts/ directory containing this file.
$ProjectRoot = Split-Path -Parent $PSScriptRoot

if (-not (Test-Path $ProjectRoot)) {
    throw "Project root not found: $ProjectRoot"
}

if ($Remove) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Scheduled task '$TaskName' removed." -ForegroundColor Green
    return
}

# Locate 'uv' so the task works even when the Task Scheduler environment
# has a different PATH than the interactive shell.
$Uv = Get-Command uv -ErrorAction Stop | Select-Object -ExpandProperty Source
if (-not $Uv) {
    throw "Could not find 'uv' on PATH. Install it first: https://docs.astral.sh/uv/"
}

$Action = New-ScheduledTaskAction `
    -Execute $Uv `
    -Argument "`"run`" mcp-server-template --transport streamable-http --host 127.0.0.1 --port $Port" `
    -WorkingDirectory $ProjectRoot

$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit (New-TimeSpan -Seconds 0)

# Create or update (idempotent).
$Existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($Existing) {
    Set-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings
    Write-Host "Scheduled task '$TaskName' updated." -ForegroundColor Green
} else {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -User $env:USERNAME `
        -Force | Out-Null
    Write-Host "Scheduled task '$TaskName' created." -ForegroundColor Green
}

Write-Host ""
Write-Host "The MCP server will start at logon on port $Port" -ForegroundColor Cyan
Write-Host "  Endpoint: http://127.0.0.1:$Port/mcp" -ForegroundColor Cyan
Write-Host ""
Write-Host "Manage it with:" -ForegroundColor Yellow
Write-Host "  Task Scheduler UI:  tasks.dml"
Write-Host "  Start now:          Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "  Remove:             pwsh $PSScriptRoot/setup-windows-task.ps1 -Remove"
