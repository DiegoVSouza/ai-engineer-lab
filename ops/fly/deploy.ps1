<#
.SYNOPSIS
One-command lifecycle of the SupportOps Fly stack.

.DESCRIPTION
Up     Prepare secrets once, create missing stack apps and volumes, wake existing
       machines, deploy every app in dependency order, start everything and wait
       for health. Safe to repeat.
Down   Stop every machine and disable public autostart. Volumes survive and are
       listed. Nothing is deleted unless -DestroyData is confirmed.
Status Report machines and volumes per app without changing anything.
Stage, Build and Deploy remain available as the individual steps of Up.

Only apps in ops/fly/stack-apps.ps1 can be touched. Up and Down spend real money
and change a public deployment; preview them with -DryRun.

.PARAMETER Action
Up, Down, Status, Stage, Build or Deploy.

.PARAMETER Only
Restrict the action to these stack apps.

.PARAMETER DryRun
Print the mutating Fly commands instead of running them.

.PARAMETER SkipSecrets
Skip secret preparation and import during Up or Stage.

.PARAMETER DestroyData
With Down, delete the stack apps and their volumes. Irreversible; requires
-ConfirmDestroy supportops-lab.

.PARAMETER ConfirmDestroy
Must equal supportops-lab for -DestroyData to run.

.EXAMPLE
pwsh -File ops/fly/deploy.ps1 -Action Up -DryRun

.EXAMPLE
pwsh -File ops/fly/deploy.ps1 -Action Down
#>
param(
  [ValidateSet("Up", "Down", "Status", "Stage", "Build", "Deploy")]
  [string]$Action = "Build",
  [string[]]$Only = @(),
  [switch]$DryRun,
  [switch]$SkipSecrets,
  [switch]$DestroyData,
  [string]$ConfirmDestroy = ""
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "stack-apps.ps1")
$root = (Resolve-Path (Join-Path $PSScriptRoot "../.." )).Path
$power = Join-Path $PSScriptRoot "power.ps1"
$apps = @(Get-StackApps -Only $Only)

if ($DestroyData) {
  if ($Action -ne "Down") { throw "-DestroyData is only valid with -Action Down." }
  if ($ConfirmDestroy -cne $script:ConfirmToken) {
    throw "-DestroyData deletes apps and volumes; pass -ConfirmDestroy $($script:ConfirmToken) to proceed."
  }
}

function Invoke-Stage {
  $existing = Read-FlyJson -Arguments @("apps", "list", "--json") -AllowMissing:$DryRun
  foreach ($app in $apps) {
    if (-not ($existing | Where-Object Name -eq $app.Name)) {
      Invoke-Fly -DryRun:$DryRun -Arguments @("apps", "create", $app.Name, "--org", "personal", "--yes")
    }
  }
  foreach ($app in $apps) {
    if ($app.Volume) {
      $volumes = Read-FlyJson -Arguments @("volumes", "list", "--app", $app.Name, "--json") -AllowMissing
      if (-not ($volumes | Where-Object Name -eq $app.Volume.Name)) {
        Invoke-Fly -DryRun:$DryRun -Arguments @("volumes", "create", $app.Volume.Name, "--app", $app.Name, "--region", "iad", "--size", "$($app.Volume.Size)", "--snapshot-retention", "14", "--yes")
      }
    }
  }
  if ($SkipSecrets) { return }
  if ($DryRun) {
    Write-Output "DRY-RUN prepare-secrets.ps1 -Action Prepare, then -Action Import"
    return
  }
  & (Join-Path $PSScriptRoot "prepare-secrets.ps1") -Action Prepare
  & (Join-Path $PSScriptRoot "prepare-secrets.ps1") -Action Import
}

function Invoke-Build {
  foreach ($app in $apps) {
    $config = Join-Path $root $app.Config
    $context = Join-Path $root $app.Context
    Invoke-Fly -DryRun:$DryRun -Arguments @("deploy", $context, "--config", $config, "--app", $app.Name, "--remote-only", "--build-only", "--yes")
  }
}

function Invoke-Deploy {
  foreach ($app in $apps) {
    $config = Join-Path $root $app.Config
    $context = Join-Path $root $app.Context
    Invoke-Fly -DryRun:$DryRun -Arguments @("deploy", $context, "--config", $config, "--app", $app.Name, "--remote-only", "--yes", "--ha=false")
    foreach ($group in $app.Processes) {
      Invoke-Fly -DryRun:$DryRun -Arguments @("scale", "count", "1", "--process-group", $group, "--app", $app.Name, "--yes")
    }
  }
}

function Invoke-ClientSync {
  if ($DryRun) {
    Write-Output "DRY-RUN python ops/stack/idp_clients.py (WEB_ORIGIN https://supportops-lab-web.fly.dev)"
    return
  }
  if ($SkipSecrets) { return }
  $secretPath = Join-Path $root "artifacts/checkpoints/pre-fly-final-20261023/fly-secrets.json"
  if ($env:FLY_SECRETS_DIR) { $secretPath = Join-Path $env:FLY_SECRETS_DIR "fly-secrets.json" }
  $values = Get-Content -Raw $secretPath | ConvertFrom-Json
  $env:IDP_URL = "https://supportops-lab-idp.fly.dev"
  $env:WEB_ORIGIN = "https://supportops-lab-web.fly.dev"
  $env:IDP_ADMIN_PASSWORD = $values.KEYCLOAK_ADMIN_PASSWORD
  try {
    & python (Join-Path $root "ops/stack/idp_clients.py")
    if ($LASTEXITCODE -ne 0) { throw "Applying the console OIDC client failed with exit code $LASTEXITCODE" }
  }
  finally {
    Remove-Item Env:IDP_ADMIN_PASSWORD
  }
}

function Write-PreservedVolumes {
  foreach ($app in $apps) {
    $volumes = Read-FlyJson -Arguments @("volumes", "list", "--app", $app.Name, "--json") -AllowMissing
    foreach ($volume in @($volumes)) {
      if ($volume) { Write-Output "preserved: $($app.Name) volume $($volume.name) $($volume.size_gb)GB (still billed while it exists)" }
    }
  }
}

function Invoke-Destroy {
  $existing = Read-FlyJson -Arguments @("apps", "list", "--json")
  $names = @($apps | ForEach-Object { $_.Name })
  [array]::Reverse($names)
  foreach ($name in $names) {
    if ($existing | Where-Object Name -eq $name) {
      Invoke-Fly -DryRun:$DryRun -Arguments @("apps", "destroy", $name, "--yes")
    }
    else {
      Write-Output "$name`: not deployed, nothing to destroy"
    }
  }
}

$evidence = if ($env:FLY_EVIDENCE_DIR) { $env:FLY_EVIDENCE_DIR } else { Join-Path $root "artifacts/evidence/fly" }
$transcript = -not $DryRun -and $Action -ne "Status"
if ($transcript) {
  New-Item -ItemType Directory -Force -Path $evidence | Out-Null
  Start-Transcript -Path (Join-Path $evidence "provision-$($Action.ToLowerInvariant()).txt") -Append | Out-Null
}

Push-Location $root
try {
  switch ($Action) {
    "Stage" { Invoke-Stage }
    "Build" { Invoke-Build }
    "Deploy" { Invoke-Deploy }
    "Status" { & $power -Action Status -Only $Only }
    "Up" {
      Invoke-Stage
      & $power -Action Start -ExistingOnly -DryRun:$DryRun -Only $Only
      Invoke-Deploy
      & $power -Action Start -DryRun:$DryRun -Only $Only
      Invoke-ClientSync
      Write-Output "Up finished. Volumes and machines:"
      & $power -Action Status -Only $Only
    }
    "Down" {
      if ($DestroyData) {
        Invoke-Destroy
        Write-Output "Destroyed the stack apps above, including their attached volumes."
      }
      else {
        & $power -Action Stop -DryRun:$DryRun -Only $Only
        Write-PreservedVolumes
        Write-Output "Down finished. Machines are stopped; bring them back with -Action Up."
      }
    }
  }
}
finally {
  Pop-Location
  if ($transcript) { Stop-Transcript | Out-Null }
}
