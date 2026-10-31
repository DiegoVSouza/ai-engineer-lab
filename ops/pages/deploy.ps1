# Publish a static front to Cloudflare Pages (lab ADR-001). Dry run unless -Apply is given.
# Nothing here logs in or creates tokens: authenticate first with `wrangler login` or CLOUDFLARE_API_TOKEN.
param(
  [Parameter(Mandatory)][ValidateSet("console", "portfolio")][string]$Site,
  [switch]$Apply,
  [switch]$AllowDirty,
  [switch]$CreateProject
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$wrangler = if ($env:WRANGLER_BIN) { $env:WRANGLER_BIN } else { "wrangler" }
$evidenceDir = if ($env:PAGES_EVIDENCE_DIR) { $env:PAGES_EVIDENCE_DIR } else { Join-Path $root "artifacts/evidence/pages" }

# Single inventory: a Pages project name outside this list is never touched.
$sites = @{
  console   = @{ Project = "supportops-console"; Dir = "projects/p06"; Build = @("run", "-s", "build:pages") }
  portfolio = @{ Project = "diego-portifolio-ai"; Dir = "projects/p07"; Build = @("run", "-s", "build") }
}
$entry = $sites[$Site]
$project = if ($env:PAGES_PROJECT_OVERRIDE) { throw "PAGES_PROJECT_OVERRIDE is not supported: edit the inventory in ops/pages/deploy.ps1" } else { $entry.Project }
$dir = Join-Path $root $entry.Dir

if ($Site -eq "console") {
  if (-not $env:P05_API_URL) { $env:P05_API_URL = "https://supportops-lab-p05.fly.dev" }
  if (-not $env:OIDC_ISSUER) { $env:OIDC_ISSUER = "https://supportops-lab-idp.fly.dev/realms/supportops" }
  if (-not $env:OIDC_CLIENT_ID) { $env:OIDC_CLIENT_ID = "supportops-web" }
}

$commit = (git -C $dir rev-parse HEAD).Trim()
$dirty = [bool](git -C $dir status --porcelain)
$deployArgs = @("pages", "deploy", "dist", "--project-name", $project, "--branch", "main", "--commit-hash", $commit, "--commit-dirty=$($dirty.ToString().ToLower())")

Write-Output "site=$Site project=$project dir=$($entry.Dir) commit=$commit dirty=$dirty"
if ($CreateProject) { Write-Output "PLAN $wrangler pages project create $project --production-branch main" }
if (-not $env:PAGES_SKIP_BUILD) { Write-Output "PLAN (cd $($entry.Dir)) npm $($entry.Build -join ' ')" }
Write-Output "PLAN (cd $($entry.Dir)) $wrangler $($deployArgs -join ' ')"

if (-not $Apply) {
  Write-Output "DRY-RUN: nothing was built, uploaded or created. Add -Apply after the owner's go."
  exit 0
}
if ($dirty -and -not $AllowDirty) { throw "Refusing to publish an uncommitted tree for $Site. Commit first, or pass -AllowDirty and say why." }

Push-Location $dir
try {
  if (-not $env:PAGES_SKIP_BUILD) {
    & npm @($entry.Build)
    if ($LASTEXITCODE -ne 0) { throw "Build failed with exit code $LASTEXITCODE" }
  }
  if ($CreateProject) {
    & $wrangler pages project create $project --production-branch main
    if ($LASTEXITCODE -ne 0) { throw "Project create failed with exit code $LASTEXITCODE" }
  }
  & $wrangler @deployArgs
  if ($LASTEXITCODE -ne 0) { throw "wrangler deploy failed with exit code $LASTEXITCODE" }
}
finally {
  Pop-Location
}

New-Item -ItemType Directory -Force -Path $evidenceDir | Out-Null
$record = @{ site = $Site; project = $project; commit = $commit; dirty = $dirty; at = (Get-Date).ToUniversalTime().ToString("o") }
$record | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $evidenceDir "$Site-$(Get-Date -Format yyyyMMddTHHmmss).json")
Write-Output "DEPLOYED $project"
