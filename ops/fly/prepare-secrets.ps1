param(
  [ValidateSet("Prepare", "Import")]
  [string]$Action = "Prepare"
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "stack-apps.ps1")
$root = (Resolve-Path (Join-Path $PSScriptRoot "../.." )).Path
$privateDir = if ($env:FLY_SECRETS_DIR) { $env:FLY_SECRETS_DIR } else { Join-Path $root "artifacts/checkpoints/pre-fly-final-20261023" }
$secretPath = Join-Path $privateDir "fly-secrets.json"
$credentialPath = Join-Path $privateDir "demo-logins.txt"
New-Item -ItemType Directory -Force -Path $privateDir | Out-Null

function New-Secret {
  $bytes = [byte[]]::new(32)
  [System.Security.Cryptography.RandomNumberGenerator]::Fill($bytes)
  [Convert]::ToHexString($bytes).ToLowerInvariant()
}

if ($Action -eq "Prepare") {
  if (-not (Test-Path $secretPath)) {
    $values = [ordered]@{}
    @(
      "POSTGRES_SUPERUSER_PASSWORD", "P04_DB_PASSWORD", "P05_DB_PASSWORD", "KEYCLOAK_DB_PASSWORD",
      "REDIS_PASSWORD", "KEYCLOAK_ADMIN_PASSWORD", "SUPPORTOPS_CLIENT_SECRET",
      "AGENT_A_PASSWORD", "AGENT_B_PASSWORD", "APPROVER_PASSWORD", "P05_JWT_SECRET", "MCP_SIGNING_SECRET"
    ) | ForEach-Object { $values[$_] = New-Secret }
    $values | ConvertTo-Json | Set-Content -Encoding utf8NoBOM $secretPath
    @(
      "SupportOps Fly demo credentials",
      "Issuer: https://supportops-lab-idp.fly.dev/realms/supportops",
      "Admin username: lab-admin",
      "Admin password: $($values.KEYCLOAK_ADMIN_PASSWORD)",
      "Client ID: supportops-api",
      "Agent A username: agent-a (tenant-a)",
      "Agent A password: $($values.AGENT_A_PASSWORD)",
      "Agent B username: agent-b (tenant-b)",
      "Agent B password: $($values.AGENT_B_PASSWORD)",
      "Approver username: approver-a (tenant-a)",
      "Approver password: $($values.APPROVER_PASSWORD)",
      "Change these demo credentials after first use."
    ) | Set-Content -Encoding utf8NoBOM $credentialPath
  }
  Write-Output "Created private Fly secrets and demo credentials in the local checkpoint directory. Values were not printed."
  exit 0
}

if (-not (Test-Path $secretPath)) { throw "Run with -Action Prepare before importing secrets." }
$values = Get-Content -Raw $secretPath | ConvertFrom-Json -AsHashtable
$issuer = "https://supportops-lab-idp.fly.dev/realms/supportops"
$introspection = "$issuer/protocol/openid-connect/token/introspect"
$pgHost = "supportops-lab-db.flycast"
$redisHost = "supportops-lab-redis.flycast"
$p04Dsn = "postgresql://p04:$($values.P04_DB_PASSWORD)@$pgHost`:5432/p04"
$p05Dsn = "postgresql://p05:$($values.P05_DB_PASSWORD)@$pgHost`:5432/p05"
$p04Redis = "redis://:$($values.REDIS_PASSWORD)@$redisHost`:6379/1"
$p05Redis = "redis://:$($values.REDIS_PASSWORD)@$redisHost`:6379/0"
$apps = [ordered]@{
  "supportops-lab-db" = @{
    POSTGRES_PASSWORD = $values.POSTGRES_SUPERUSER_PASSWORD
    P04_DB_PASSWORD = $values.P04_DB_PASSWORD
    P05_DB_PASSWORD = $values.P05_DB_PASSWORD
    KEYCLOAK_DB_PASSWORD = $values.KEYCLOAK_DB_PASSWORD
  }
  "supportops-lab-redis" = @{ REDIS_PASSWORD = $values.REDIS_PASSWORD }
  "supportops-lab-idp" = @{
    KC_BOOTSTRAP_ADMIN_PASSWORD = $values.KEYCLOAK_ADMIN_PASSWORD
    KC_DB_PASSWORD = $values.KEYCLOAK_DB_PASSWORD
    SUPPORTOPS_CLIENT_SECRET = $values.SUPPORTOPS_CLIENT_SECRET
    SUPPORTOPS_AGENT_A_PASSWORD = $values.AGENT_A_PASSWORD
    SUPPORTOPS_AGENT_B_PASSWORD = $values.AGENT_B_PASSWORD
    SUPPORTOPS_APPROVER_PASSWORD = $values.APPROVER_PASSWORD
  }
  "supportops-lab-p04" = @{
    P04_DATABASE_URL = $p04Dsn
    P04_REDIS_URL = $p04Redis
    AWS_ACCESS_KEY_ID = "localstack"
    AWS_SECRET_ACCESS_KEY = "localstack"
  }
  "supportops-lab-p05" = @{
    P05_POSTGRES_DSN = $p05Dsn
    P05_REDIS_URL = $p05Redis
    JWT_SECRET = $values.P05_JWT_SECRET
    MCP_SIGNING_SECRET = $values.MCP_SIGNING_SECRET
    API_OIDC_INTROSPECTION_URL = $introspection
    API_OIDC_CLIENT_ID = "supportops-api"
    API_OIDC_CLIENT_SECRET = $values.SUPPORTOPS_CLIENT_SECRET
    API_OIDC_ISSUER = $issuer
    API_OIDC_AUDIENCE = "supportops-api"
  }
  "supportops-lab-mcp" = @{
    MCP_SIGNING_SECRET = $values.MCP_SIGNING_SECRET
    MCP_OIDC_INTROSPECTION_URL = $introspection
    MCP_OIDC_CLIENT_ID = "supportops-api"
    MCP_OIDC_CLIENT_SECRET = $values.SUPPORTOPS_CLIENT_SECRET
    MCP_OIDC_ISSUER = $issuer
    MCP_OIDC_AUDIENCE = "https://supportops-lab-mcp.fly.dev/mcp"
  }
}

foreach ($app in $apps.Keys) {
  Assert-StackApp -App $app
  $start = [System.Diagnostics.ProcessStartInfo]::new($script:FlyBin)
  $start.ArgumentList.Add("secrets")
  $start.ArgumentList.Add("import")
  $start.ArgumentList.Add("--stage")
  $start.ArgumentList.Add("--app")
  $start.ArgumentList.Add($app)
  $start.RedirectStandardInput = $true
  $start.RedirectStandardOutput = $true
  $start.RedirectStandardError = $true
  $start.UseShellExecute = $false
  $process = [System.Diagnostics.Process]::Start($start)
  foreach ($key in $apps[$app].Keys) { $process.StandardInput.WriteLine("$key=$($apps[$app][$key])") }
  $process.StandardInput.Close()
  $stdout = $process.StandardOutput.ReadToEnd()
  $stderr = $process.StandardError.ReadToEnd()
  $process.WaitForExit()
  if ($process.ExitCode -ne 0) { throw "Staging secrets for $app failed: $stderr" }
  Write-Output "Staged $($apps[$app].Count) secrets for $app. $($stdout.Trim())"
}
