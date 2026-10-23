param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("Start", "Stop")]
  [string]$Action
)

$ErrorActionPreference = "Stop"

function Invoke-Fly {
  param([string[]]$Arguments)

  & fly @Arguments
  if ($LASTEXITCODE -ne 0) {
    throw "fly $($Arguments -join ' ') failed with exit code $LASTEXITCODE"
  }
}

function Get-Machines {
  param([string]$App)

  $json = & fly machine list --app $App --json
  if ($LASTEXITCODE -ne 0) {
    throw "Unable to list machines for $App."
  }

  @($json | ConvertFrom-Json)
}

function Get-ProcessMachines {
  param([string]$App, [string]$Process)

  @(Get-Machines -App $App | Where-Object {
      $group = $_.config.metadata.fly_process_group
      if (-not $group) { $group = "app" }
      $group -eq $Process
    })
}

function Set-ProcessState {
  param([string]$App, [string]$Process, [string]$State)

  foreach ($machine in (Get-ProcessMachines -App $App -Process $Process)) {
    $publicApp = $App -in @("supportops-lab-p04", "supportops-lab-p05", "supportops-lab-mcp") -and $Process -eq "app"
    $autoStart = $null
    if ($publicApp -and @($machine.config.services).Count -gt 0) {
      $autoStart = [bool]$machine.config.services[0].autostart
    }

    if ($machine.state -eq $State) {
      if ($publicApp -and $null -ne $autoStart -and $autoStart -ne ($State -eq "started")) {
        $value = if ($State -eq "started") { "true" } else { "false" }
        Invoke-Fly -Arguments @("machine", "update", $machine.id, "--app", $App, "--autostart=$value", "--yes")
      }
      continue
    }

    if ($State -eq "started") {
      if ($publicApp -and $autoStart -eq $false) {
        Invoke-Fly -Arguments @("machine", "update", $machine.id, "--app", $App, "--autostart=true", "--yes")
      }
      Invoke-Fly -Arguments @("machine", "start", $machine.id, "--app", $App)
      Invoke-Fly -Arguments @("machine", "wait", $machine.id, "--app", $App, "--state", "started", "--wait-timeout", "5m")
    }
    else {
      if ($machine.state -ne "stopped") {
        Invoke-Fly -Arguments @("machine", "stop", $machine.id, "--app", $App, "--wait-timeout", "2m")
        Invoke-Fly -Arguments @("machine", "wait", $machine.id, "--app", $App, "--state", "stopped", "--wait-timeout", "2m")
      }
      if ($publicApp -and $autoStart -eq $true) {
        Invoke-Fly -Arguments @("machine", "update", $machine.id, "--app", $App, "--autostart=false", "--yes")
      }
    }
  }
}

function Wait-ForHealthyApp {
  param([string]$App, [int]$TimeoutSeconds = 300)

  $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
  do {
    $machines = @(Get-Machines -App $App | Where-Object state -eq "started")
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

$startOrder = @(
  @{ App = "supportops-lab-db"; Processes = @("app"); Check = $true },
  @{ App = "supportops-lab-redis"; Processes = @("app"); Check = $true },
  @{ App = "supportops-lab-idp"; Processes = @("app"); Check = $true },
  @{ App = "supportops-lab-sns"; Processes = @("app"); Check = $true },
  @{ App = "supportops-lab-jaeger"; Processes = @("app"); Check = $false },
  @{ App = "supportops-lab-p04"; Processes = @("worker"); Check = $false },
  @{ App = "supportops-lab-p05"; Processes = @("worker"); Check = $false },
  @{ App = "supportops-lab-p04"; Processes = @("app"); Check = $false },
  @{ App = "supportops-lab-p05"; Processes = @("app"); Check = $false },
  @{ App = "supportops-lab-mcp"; Processes = @("app"); Check = $false }
)

$stopOrder = @(
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

if ($Action -eq "Start") {
  foreach ($entry in $startOrder) {
    foreach ($process in $entry.Processes) {
      Write-Output "Starting $($entry.App)/$process"
      Set-ProcessState -App $entry.App -Process $process -State "started"
    }
    if ($entry.Check) { Wait-ForHealthyApp -App $entry.App }
  }
}
else {
  foreach ($entry in $stopOrder) {
    foreach ($process in $entry.Processes) {
      Write-Output "Stopping $($entry.App)/$process"
      Set-ProcessState -App $entry.App -Process $process -State "stopped"
    }
  }
}
