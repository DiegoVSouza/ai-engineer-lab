# Single inventory of the Fly apps this stack owns. Dot-sourced by the operator
# scripts; every Fly call that names an app must go through Invoke-Fly or
# Read-FlyJson so nothing outside this list can be touched.

$script:FlyBin = if ($env:FLY_BIN) { $env:FLY_BIN } else { "fly" }
$script:ConfirmToken = "supportops-lab"

$script:StackApps = @(
  @{ Name = "supportops-lab-db"; Config = "fly/postgres/fly.toml"; Context = "ops/fly/postgres"; Volume = @{ Name = "pg_data"; Size = 10 }; Processes = @("app") },
  @{ Name = "supportops-lab-redis"; Config = "fly/redis/fly.toml"; Context = "ops/fly/redis"; Volume = @{ Name = "redis_data"; Size = 1 }; Processes = @("app") },
  @{ Name = "supportops-lab-idp"; Config = "fly/idp/fly.toml"; Context = "ops/fly/idp"; Processes = @("app") },
  @{ Name = "supportops-lab-sns"; Config = "fly/sns/fly.toml"; Context = "ops/fly/sns"; Processes = @("app") },
  @{ Name = "supportops-lab-jaeger"; Config = "fly/jaeger/fly.toml"; Context = "ops/fly/jaeger"; Processes = @("app") },
  @{ Name = "supportops-lab-mcp"; Config = "fly/mcp/fly.toml"; Context = "projects/p05"; Processes = @("app") },
  @{ Name = "supportops-lab-p04"; Config = "fly/p04/fly.toml"; Context = "projects/p04"; Processes = @("app", "worker") },
  @{ Name = "supportops-lab-p05"; Config = "fly/p05/fly.toml"; Context = "projects/p05"; Volume = @{ Name = "p05_graph"; Size = 1 }; Processes = @("app", "worker") }
)

$script:StackAppNames = @($script:StackApps | ForEach-Object { $_.Name })

function Assert-StackApp {
  param([string[]]$App)

  foreach ($name in $App) {
    if ($name -notin $script:StackAppNames) {
      throw "Refusing to touch '$name': it is not in the stack inventory (ops/fly/stack-apps.ps1)."
    }
  }
}

function Get-StackApps {
  param([string[]]$Only = @())

  if ($Only.Count -eq 0) { return $script:StackApps }
  Assert-StackApp -App $Only
  @($script:StackApps | Where-Object { $Only -contains $_.Name })
}

function Assert-FlyArguments {
  param([string[]]$Arguments)

  $appIndex = [array]::IndexOf($Arguments, "--app")
  if ($appIndex -ge 0) { Assert-StackApp -App $Arguments[$appIndex + 1] }
  if ($Arguments[0] -eq "apps" -and $Arguments[1] -in @("create", "destroy")) { Assert-StackApp -App $Arguments[2] }
}

function Invoke-Fly {
  param([string[]]$Arguments, [switch]$DryRun)

  Assert-FlyArguments -Arguments $Arguments
  if ($DryRun) {
    Write-Output "DRY-RUN fly $($Arguments -join ' ')"
    return
  }
  $output = & $script:FlyBin @Arguments 2>&1
  $code = $LASTEXITCODE
  $output | ForEach-Object { Write-Output $_.ToString() }
  if ($code -ne 0) { throw "fly $($Arguments -join ' ') failed with exit code $code" }
}

function Read-FlyJson {
  param([string[]]$Arguments, [switch]$AllowMissing)

  Assert-FlyArguments -Arguments $Arguments
  $json = & $script:FlyBin @Arguments 2>$null
  $code = $LASTEXITCODE
  $global:LASTEXITCODE = 0
  if ($code -ne 0) {
    if ($AllowMissing) { return $null }
    throw "fly $($Arguments -join ' ') failed with exit code $code"
  }
  if (-not $json) { return , @() }
  ($json -join "`n") | ConvertFrom-Json -NoEnumerate
}
