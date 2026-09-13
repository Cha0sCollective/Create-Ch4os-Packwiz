# Builds a standard Prism instance. Packwiz performs installation and updates.
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Output,
    [string]$CacheDirectory,
    [ValidateSet('public','beta')][string]$Channel = 'public',
    [string]$PackUrl
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
if (-not $PackUrl) { $PackUrl = "https://raw.githubusercontent.com/Cha0sCollective/Create-Ch4os-Packwiz/$Channel/pack/pack.toml" }
if (-not $CacheDirectory) { $CacheDirectory = Join-Path $repo 'dist/prism-tools' }
$utf8 = New-Object Text.UTF8Encoding($false)
$profile = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'profile.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$runtime = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'runtime.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$tools = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'prism-tools.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($runtime.launch.client.garbageCollector -cne 'generational-zgc') { throw 'Review Prism Java arguments when the pack collector changes.' }
$uri = [Uri]$PackUrl
if (-not $uri.IsAbsoluteUri -or ($uri.Scheme -ne 'https' -and -not ($uri.Scheme -eq 'http' -and $uri.IsLoopback))) {
    throw 'Use an HTTPS pack address, or loopback HTTP for a local test.'
}
$PackUrl = $uri.AbsoluteUri
if ($profile.id -notmatch '^[A-Za-z0-9][A-Za-z0-9_-]*$' -or $profile.name -match '[\r\n]') { throw 'Invalid Prism instance identity.' }
$outputPath = [IO.Path]::GetFullPath($Output)
if (Test-Path -LiteralPath $outputPath) { throw 'Choose a new output ZIP; existing artifacts are not overwritten.' }
$revision = & git -C $repo rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Build from a Git checkout.' }
$dirty = & git -C $repo status --porcelain --untracked-files=normal
if ($LASTEXITCODE -ne 0 -or $dirty) { throw 'Commit or isolate local changes before building.' }
New-Item -ItemType Directory -Force -Path $CacheDirectory | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $outputPath) | Out-Null
$stage = Join-Path ([IO.Path]::GetTempPath()) ('ch4os-prism-' + [Guid]::NewGuid().ToString('N'))
$instance = Join-Path $stage $profile.id
$game = Join-Path $instance '.minecraft'
$notices = Join-Path $game 'third-party-notices'
New-Item -ItemType Directory -Path $notices | Out-Null
foreach ($name in @('bootstrap','installer')) {
    $tool = $tools.$name
    $cached = Join-Path $CacheDirectory ($tool.sha256 + '.jar')
    if (-not (Test-Path -LiteralPath $cached)) {
        $part = $cached + '.' + [Guid]::NewGuid().ToString('N') + '.tmp'
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -UseBasicParsing -Uri $tool.url -OutFile $part
        if ((Get-FileHash -LiteralPath $part -Algorithm SHA256).Hash.ToLowerInvariant() -cne $tool.sha256) { throw "Unexpected $name download hash." }
        Move-Item -LiteralPath $part -Destination $cached
    }
    if ((Get-FileHash -LiteralPath $cached -Algorithm SHA256).Hash.ToLowerInvariant() -cne $tool.sha256) { throw "Invalid cached $name JAR; remove it and retry." }
    $filename = if ($name -eq 'bootstrap') { 'packwiz-installer-bootstrap.jar' } else { 'packwiz-installer.jar' }
    Copy-Item -LiteralPath $cached -Destination (Join-Path $game $filename)
}
foreach ($notice in @('pack/third-party-notices/industrialized-architecture-LICENSE.txt', 'third-party/packwiz-installer-LICENSE.txt', 'third-party/packwiz-installer-bootstrap-LICENSE.txt')) {
    Copy-Item -LiteralPath (Join-Path $repo $notice) -Destination $notices
}
Copy-Item -LiteralPath (Join-Path $repo 'LICENSE.txt') -Destination $instance
Copy-Item -LiteralPath (Join-Path $repo 'docs/PRISM.md') -Destination (Join-Path $instance 'README.md')
$components = [ordered]@{ formatVersion = 1; components = @(
    [ordered]@{ uid = 'net.minecraft'; version = $runtime.minecraft; important = $true },
    [ordered]@{ uid = 'net.neoforged'; version = $runtime.neoforge.version; important = $true }
) }
[IO.File]::WriteAllText((Join-Path $instance 'mmc-pack.json'), ($components | ConvertTo-Json -Depth 5) + "`n", $utf8)
$config = @'
[General]
InstanceType=OneSix
name=PACK_NAME
iconKey=default
OverrideMemory=true
MinMemAlloc=1024
MaxMemAlloc=12288
OverrideJavaLocation=false
OverrideJavaArgs=true
JvmArgs=-XX:+UseZGC -XX:+ZGenerational
OverrideCommands=true
PreLaunchCommand="$INST_JAVA" -jar packwiz-installer-bootstrap.jar --bootstrap-no-update -s client "PACK_URL"
'@
$config = $config.Replace('PACK_NAME', $profile.name).Replace('PACK_URL', $PackUrl)
[IO.File]::WriteAllText((Join-Path $instance 'instance.cfg'), $config + "`n", $utf8)
$provenance = "Create: Ch4oS Prism import`nInitial pack version: $($profile.version)`nBuild source: $revision`nPack address: $PackUrl`nPackwiz bootstrap: $($tools.bootstrap.version)`nPackwiz installer: $($tools.installer.version)`n"
[IO.File]::WriteAllText((Join-Path $instance 'release.txt'), $provenance, $utf8)
Add-Type -AssemblyName System.IO.Compression.FileSystem
[IO.Compression.ZipFile]::CreateFromDirectory($stage, $outputPath)
$hash = (Get-FileHash -LiteralPath $outputPath -Algorithm SHA256).Hash.ToLowerInvariant()
[IO.File]::WriteAllText(($outputPath + '.sha256'), "$hash  $([IO.Path]::GetFileName($outputPath))`n", $utf8)
# Only the exact temporary directory created above is eligible for cleanup.
if ([IO.Path]::GetFullPath($stage).StartsWith([IO.Path]::GetFullPath([IO.Path]::GetTempPath()), [StringComparison]::OrdinalIgnoreCase) -and (Split-Path -Leaf $stage) -match '^ch4os-prism-[0-9a-f]{32}$') {
    Remove-Item -LiteralPath $stage -Recurse -Force
}
Write-Output "Prism ZIP: $outputPath"
Write-Output "SHA-256: $hash"
Write-Output "Pack address: $PackUrl"
