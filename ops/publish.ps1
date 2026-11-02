<#
.SYNOPSIS
Publish the whole product: the back (Fly stack) and both fronts (Cloudflare Pages).

.DESCRIPTION
Order: back first (Fly Up: secrets, apps, volumes, deploy, health; it includes the console, supportops-lab-web), then the portfolio (p07) on Cloudflare Pages.
It only chains the two existing scripts, so their guards still apply (fixed inventory of apps and projects, no uncommitted tree).
Dry run unless -Apply is given: a dry run builds, uploads and changes nothing. Real deploys spend money and change public URLs,
so run it only with the owner's go.

Authenticate first: `fly auth login` and `wrangler login` (or CLOUDFLARE_API_TOKEN). This script never logs in.

.PARAMETER Target
all (default: back and portfolio), back, front, portfolio, or console (Pages project must exist).

.PARAMETER Apply
Really publish. Without it every step is a dry run.

.PARAMETER AllowDirty
Let Pages publish a project with uncommitted changes. Commit first when you can.

.PARAMETER SkipChecks
Skip the typecheck and unit tests that run before the front is built.

.EXAMPLE
pwsh -File ops/publish.ps1                      # dry run of everything

.EXAMPLE
pwsh -File ops/publish.ps1 -Target portfolio -Apply
#>
param(
  [ValidateSet("all", "back", "front", "console", "portfolio")][string]$Target = "all",
  [switch]$Apply,
  [switch]$AllowDirty,
  [switch]$SkipChecks
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$flyDeploy = Join-Path $PSScriptRoot "fly/deploy.ps1"
$pagesDeploy = Join-Path $PSScriptRoot "pages/deploy.ps1"

$doBack = $Target -in @("all", "back")
$sites = switch ($Target) {
  # The console already runs on Fly (supportops-lab-web) and is published by the back step; it has no Pages project.
  # Ask for -Target console only after creating that project (ops/pages/deploy.ps1 -CreateProject).
  "all" { @("portfolio") }
  "front" { @("portfolio") }
  "console" { @("console") }
  "portfolio" { @("portfolio") }
  default { @() }
}
$projectOf = @{ console = "projects/p06"; portfolio = "projects/p07" }

function Step([string]$Name, [scriptblock]$Run) {
  Write-Output "`n=== $Name ==="
  & $Run
  if ($LASTEXITCODE -ne 0) { throw "$Name failed with exit code $LASTEXITCODE" }
}

Write-Output "publish target=$Target mode=$(if ($Apply) { 'APPLY' } else { 'DRY-RUN' })"

# 1. Gate: the fronts must typecheck and pass their unit tests before anything goes out.
if ($sites.Count -gt 0 -and -not $SkipChecks) {
  foreach ($site in $sites) {
    $dir = Join-Path $root $projectOf[$site]
    Step "checks $site" {
      Push-Location $dir
      try {
        & npm run -s typecheck
        if ($LASTEXITCODE -ne 0) { return }
        & npm test --silent
      }
      finally { Pop-Location }
    }
  }
}

# 2. Back: the Fly stack (db, redis, idp, p05, mcp, web). Up is idempotent.
if ($doBack) {
  Step "back (Fly)" {
    $args = @("-NoProfile", "-File", $flyDeploy, "-Action", "Up")
    if (-not $Apply) { $args += "-DryRun" }
    & pwsh @args
  }
}

# 3. Fronts: Cloudflare Pages. The Pages script builds, refuses a dirty tree and records evidence.
foreach ($site in $sites) {
  Step "front $site (Pages)" {
    $args = @("-NoProfile", "-File", $pagesDeploy, "-Site", $site)
    if ($Apply) { $args += "-Apply" }
    if ($AllowDirty) { $args += "-AllowDirty" }
    & pwsh @args
  }
}

Write-Output "`n$(if ($Apply) { 'PUBLISHED' } else { 'DRY-RUN complete: nothing was published. Add -Apply after the owners go.' })"
