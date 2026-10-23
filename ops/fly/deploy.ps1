param(
  [ValidateSet("Stage", "Build", "Deploy")]
  [string]$Action = "Build",
  [string[]]$Only = @()
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "../.." )).Path
$evidence = Join-Path $root "artifacts/evidence/fly"
New-Item -ItemType Directory -Force -Path $evidence | Out-Null
$log = Join-Path $evidence "provision-$($Action.ToLowerInvariant()).txt"
Start-Transcript -Path $log -Append | Out-Null

function Invoke-Fly {
  param([string[]]$Arguments)
  $output = & fly @Arguments 2>&1
  $output | ForEach-Object { Write-Output $_.ToString() }
  if ($LASTEXITCODE -ne 0) { throw "fly $($Arguments -join ' ') failed with exit code $LASTEXITCODE" }
}

$apps = @(
  @{ Name = "supportops-lab-db"; Config = "fly/postgres/fly.toml"; Context = "ops/fly/postgres"; Volume = @{ Name = "pg_data"; Size = 10 } },
  @{ Name = "supportops-lab-redis"; Config = "fly/redis/fly.toml"; Context = "ops/fly/redis"; Volume = @{ Name = "redis_data"; Size = 1 } },
  @{ Name = "supportops-lab-idp"; Config = "fly/idp/fly.toml"; Context = "ops/fly/idp" },
  @{ Name = "supportops-lab-sns"; Config = "fly/sns/fly.toml"; Context = "ops/fly/sns" },
  @{ Name = "supportops-lab-jaeger"; Config = "fly/jaeger/fly.toml"; Context = "ops/fly/jaeger" },
  @{ Name = "supportops-lab-mcp"; Config = "fly/mcp/fly.toml"; Context = "projects/p05" },
  @{ Name = "supportops-lab-p04"; Config = "fly/p04/fly.toml"; Context = "projects/p04" },
  @{ Name = "supportops-lab-p05"; Config = "fly/p05/fly.toml"; Context = "projects/p05"; Volume = @{ Name = "p05_graph"; Size = 1 } }
)
if ($Only.Count -gt 0) {
  $apps = @($apps | Where-Object { $Only -contains $_.Name })
  if ($apps.Count -eq 0) { throw "No configured Fly app matches -Only $($Only -join ', ')." }
}

Push-Location $root
try {
  if ($Action -eq "Stage") {
    $existing = & fly apps list --json | ConvertFrom-Json
    if ($LASTEXITCODE -ne 0) { throw "Unable to read the Fly app inventory." }
    foreach ($app in $apps) {
      if (-not ($existing | Where-Object Name -eq $app.Name)) {
        Invoke-Fly -Arguments @("apps", "create", $app.Name, "--org", "personal", "--yes")
      }
    }
    foreach ($app in $apps) {
      if ($app.Volume) {
        $volumes = & fly volumes list --app $app.Name --json 2>$null
        if ($LASTEXITCODE -ne 0) { $volumes = "[]" }
        $existingVolumes = @($volumes | ConvertFrom-Json)
        if (-not ($existingVolumes | Where-Object Name -eq $app.Volume.Name)) {
          Invoke-Fly -Arguments @("volumes", "create", $app.Volume.Name, "--app", $app.Name, "--region", "iad", "--size", "$($app.Volume.Size)", "--snapshot-retention", "14", "--yes")
        }
      }
    }
    & (Join-Path $PSScriptRoot "prepare-secrets.ps1") -Action Import
  }

  if ($Action -eq "Build") {
    foreach ($app in $apps) {
      $config = Join-Path $root $app.Config
      $context = Join-Path $root $app.Context
      Invoke-Fly -Arguments @("deploy", $context, "--config", $config, "--app", $app.Name, "--remote-only", "--build-only", "--yes")
    }
  }

  if ($Action -eq "Deploy") {
    foreach ($app in $apps) {
      $config = Join-Path $root $app.Config
      $context = Join-Path $root $app.Context
      Invoke-Fly -Arguments @("deploy", $context, "--config", $config, "--app", $app.Name, "--remote-only", "--yes", "--ha=false")
      $groups = if ($app.Name -in @("supportops-lab-p04", "supportops-lab-p05")) { @("app", "worker") } else { @("app") }
      foreach ($group in $groups) {
        Invoke-Fly -Arguments @("scale", "count", "1", "--process-group", $group, "--app", $app.Name, "--yes")
      }
    }
  }
}
finally {
  Pop-Location
  Stop-Transcript | Out-Null
}
