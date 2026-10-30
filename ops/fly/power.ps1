<#
.SYNOPSIS
Start, stop or inspect the machines of the SupportOps Fly stack.

.DESCRIPTION
Start and Stop act only on apps in ops/fly/stack-apps.ps1, in dependency order.
Volumes are never touched here. Use deploy.ps1 -Action Up/Down for the
one-command lifecycle; this script is the resume/suspend half of it.

.PARAMETER Action
Start, Stop or Status.

.PARAMETER DryRun
Print the mutating Fly commands instead of running them.

.PARAMETER Only
Restrict the action to these stack apps.

.PARAMETER ExistingOnly
Skip apps that do not exist yet and do not wait for health.
#>
param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("Start", "Stop", "Status")]
  [string]$Action,
  [switch]$DryRun,
  [string[]]$Only = @(),
  [switch]$ExistingOnly
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "stack-apps.ps1")

function Get-Machines {
  param([string]$App, [switch]$AllowMissing)

  $machines = Read-FlyJson -Arguments @("machine", "list", "--app", $App, "--json") -AllowMissing:$AllowMissing
  if ($null -eq $machines) { return $null }
  , @($machines)
}

function Get-ProcessMachines {
  param([string]$App, [string]$Process, [switch]$AllowMissing)

  $machines = Get-Machines -App $App -AllowMissing:$AllowMissing
  if ($null -eq $machines) { return @() }
  @($machines | Where-Object {
      $group = $_.config.metadata.fly_process_group
      if (-not $group) { $group = "app" }
      $group -eq $Process
    })
}

function Set-ProcessState {
  param([string]$App, [string]$Process, [string]$State)

  $allowMissing = $DryRun -or $ExistingOnly
  foreach ($machine in (Get-ProcessMachines -App $App -Process $Process -AllowMissing:$allowMissing)) {
    $publicApp = $App -in @("supportops-lab-p04", "supportops-lab-p05", "supportops-lab-mcp", "supportops-lab-web") -and $Process -eq "app"
    $autoStart = $null
    if ($publicApp -and @($machine.config.services).Count -gt 0) {
      $autoStart = [bool]$machine.config.services[0].autostart
    }

    if ($machine.state -eq $State) {
      if ($publicApp -and $null -ne $autoStart -and $autoStart -ne ($State -eq "started")) {
        $value = if ($State -eq "started") { "true" } else { "false" }
        Invoke-Fly -DryRun:$DryRun -Arguments @("machine", "update", $machine.id, "--app", $App, "--autostart=$value", "--yes")
      }
      continue
    }

    if ($State -eq "started") {
      if ($publicApp -and $autoStart -eq $false) {
        Invoke-Fly -DryRun:$DryRun -Arguments @("machine", "update", $machine.id, "--app", $App, "--autostart=true", "--yes")
      }
      Invoke-Fly -DryRun:$DryRun -Arguments @("machine", "start", $machine.id, "--app", $App)
      Invoke-Fly -DryRun:$DryRun -Arguments @("machine", "wait", $machine.id, "--app", $App, "--state", "started", "--wait-timeout", "5m")
    }
    else {
      if ($machine.state -ne "stopped") {
        Invoke-Fly -DryRun:$DryRun -Arguments @("machine", "stop", $machine.id, "--app", $App, "--wait-timeout", "2m")
        Invoke-Fly -DryRun:$DryRun -Arguments @("machine", "wait", $machine.id, "--app", $App, "--state", "stopped", "--wait-timeout", "2m")
      }
      if ($publicApp -and $autoStart -eq $true) {
        Invoke-Fly -DryRun:$DryRun -Arguments @("machine", "update", $machine.id, "--app", $App, "--autostart=false", "--yes")
      }
    }
  }
}

function Wait-ForHealthyApp {
  param([string]$App, [int]$TimeoutSeconds = 300)

  $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
  do {
    $machines = Get-Machines -App $App
    $machines = @($machines | Where-Object state -eq "started")
    if ($machines.Count -gt 0) {
      $checked = @($machines | Where-Object { @($_.checks).Count -gt 0 })
      if ($checked.Count -eq 0 -or @($checked | Where-Object {
            @($_.checks | Where-Object status -ne "passing").Count -gt 0
          }).Count -eq 0) {
        return
      }
    }

    Start-Sleep -Seconds 5
  } while ([DateTime]::UtcNow -lt $deadline)

  throw "$App did not become healthy within $TimeoutSeconds seconds."
}

function Write-StackStatus {
  param([object[]]$Apps)

  foreach ($app in $Apps) {
    $machines = Get-Machines -App $app.Name -AllowMissing
    if ($null -eq $machines) {
      Write-Output "$($app.Name): not deployed or unreachable"
      continue
    }
    foreach ($machine in $machines) {
      $group = $machine.config.metadata.fly_process_group
      if (-not $group) { $group = "app" }
      Write-Output "$($app.Name)/$group`: machine $($machine.id) is $($machine.state)"
    }
    if (@($machines).Count -eq 0) { Write-Output "$($app.Name): no machines" }
    $volumes = Read-FlyJson -Arguments @("volumes", "list", "--app", $app.Name, "--json") -AllowMissing
    foreach ($volume in @($volumes)) {
      if ($volume) { Write-Output "$($app.Name): volume $($volume.name) $($volume.size_gb)GB ($($volume.state))" }
    }
  }
}

$startOrder = @(
  @{ App = "supportops-lab-db"; Processes = @("app"); Check = $true },
  @{ App = "supportops-lab-redis"; Processes = @("app"); Check = $true },
  @{ App = "supportops-lab-idp"; Processes = @("app"); Check = $true },
  @{ App = "supportops-lab-sns"; Processes = @("app"); Check = $true },
  @{ App = "supportops-lab-jaeger"; Processes = @("app"); Check = $false },
  @{ App = "supportops-lab-p04"; Processes = @("worker"); Check = $false },
  @{ App = "supportops-lab-p05"; Processes = @("worker"); Check = $false },
  @{ App = "supportops-lab-p04"; Processes = @("app"); Check = $true },
  @{ App = "supportops-lab-p05"; Processes = @("app"); Check = $true },
  @{ App = "supportops-lab-mcp"; Processes = @("app"); Check = $true },
  @{ App = "supportops-lab-web"; Processes = @("app"); Check = $true }
)

$stopOrder = @(
  @{ App = "supportops-lab-web"; Processes = @("app") },
  @{ App = "supportops-lab-p04"; Processes = @("app") },
  @{ App = "supportops-lab-p05"; Processes = @("app") },
  @{ App = "supportops-lab-mcp"; Processes = @("app") },
  @{ App = "supportops-lab-p04"; Processes = @("worker") },
  @{ App = "supportops-lab-p05"; Processes = @("worker") },
  @{ App = "supportops-lab-idp"; Processes = @("app") },
  @{ App = "supportops-lab-sns"; Processes = @("app") },
  @{ App = "supportops-lab-jaeger"; Processes = @("app") },
  @{ App = "supportops-lab-redis"; Processes = @("app") },
  @{ App = "supportops-lab-db"; Processes = @("app") }
)

$selected = @(Get-StackApps -Only $Only | ForEach-Object { $_.Name })

if ($Action -eq "Status") {
  Write-StackStatus -Apps (Get-StackApps -Only $Only)
}
elseif ($Action -eq "Start") {
  foreach ($entry in ($startOrder | Where-Object { $selected -contains $_.App })) {
    foreach ($process in $entry.Processes) {
      Write-Output "Starting $($entry.App)/$process"
      Set-ProcessState -App $entry.App -Process $process -State "started"
    }
    if ($entry.Check -and -not $DryRun -and -not $ExistingOnly) { Wait-ForHealthyApp -App $entry.App }
  }
}
else {
  foreach ($entry in ($stopOrder | Where-Object { $selected -contains $_.App })) {
    foreach ($process in $entry.Processes) {
      Write-Output "Stopping $($entry.App)/$process"
      Set-ProcessState -App $entry.App -Process $process -State "stopped"
    }
  }
}
