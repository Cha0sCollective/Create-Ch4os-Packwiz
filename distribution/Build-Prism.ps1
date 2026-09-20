# Builds a standard Prism instance. Packwiz performs installation and updates.
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Output,
    [string]$CacheDirectory,
    [ValidateSet('public','beta')][string]$Channel = 'public',
    [string]$PackUrl,
    [string]$VersionTag,
    [string]$SourceRevision = 'HEAD'
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
if ($VersionTag -and ($PackUrl -or $PSBoundParameters.ContainsKey('Channel') -or $PSBoundParameters.ContainsKey('SourceRevision'))) { throw 'VersionTag cannot be combined with Channel, SourceRevision or PackUrl.' }
if ($VersionTag -and $VersionTag -cnotmatch '^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$') { throw 'Use a stable version tag such as v0.2.2.' }
if ($VersionTag) { $SourceRevision = "refs/tags/$VersionTag" }
if ($SourceRevision.StartsWith('-')) { throw 'Invalid source revision.' }
$packRevision = & git -C $repo rev-parse --verify "$SourceRevision^{commit}"
if ($LASTEXITCODE -ne 0) { throw 'Source revision must resolve to a commit.' }
if ($VersionTag) { $PackUrl = "https://raw.githubusercontent.com/Cha0sCollective/Create-Ch4os-Packwiz/$packRevision/pack/pack.toml" }
if (-not $PackUrl) { $PackUrl = "https://raw.githubusercontent.com/Cha0sCollective/Create-Ch4os-Packwiz/$Channel/pack/pack.toml" }
if (-not $CacheDirectory) { $CacheDirectory = Join-Path $repo 'dist/prism-tools' }
$packagingRepo = $repo
$sourceStage = Join-Path ([IO.Path]::GetTempPath()) ('ch4os-prism-source-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $sourceStage | Out-Null
$stage = $null
try {
& git -C $repo archive --format=zip --output="$sourceStage/source.zip" $packRevision
if ($LASTEXITCODE -ne 0) { throw 'Could not export source revision.' }
Expand-Archive -LiteralPath "$sourceStage/source.zip" -DestinationPath "$sourceStage/source"
$repo = Join-Path $sourceStage 'source'
$utf8 = New-Object Text.UTF8Encoding($false)
$profile = Get-Content -LiteralPath (Join-Path $repo 'distribution/profile.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$runtime = Get-Content -LiteralPath (Join-Path $repo 'distribution/runtime.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$tools = Get-Content -LiteralPath (Join-Path $repo 'distribution/prism-tools.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$selection = if ($VersionTag) { $VersionTag } else { $Channel }
$profile.id = 'Create-Ch4oS-' + $selection.Replace('.', '-')
$profile.name = 'Create: Ch4oS - ' + $selection
$behavior = if ($VersionTag) { "Fixed version $VersionTag. Does not follow Public or Beta." } else { "Follows the $Channel branch for updates at launch." }
if ($runtime.launch.client.garbageCollector -cne 'generational-zgc') { throw 'Review Prism Java arguments when the pack collector changes.' }
$uri = [Uri]$PackUrl
if (-not $uri.IsAbsoluteUri -or ($uri.Scheme -ne 'https' -and -not ($uri.Scheme -eq 'http' -and $uri.IsLoopback))) {
    throw 'Use an HTTPS pack address, or loopback HTTP for a local test.'
}
$PackUrl = $uri.AbsoluteUri
if ($profile.id -notmatch '^[A-Za-z0-9][A-Za-z0-9_-]*$' -or $profile.name -match '[\r\n]') { throw 'Invalid Prism instance identity.' }
$outputPath = [IO.Path]::GetFullPath($Output)
if ((Test-Path -LiteralPath $outputPath) -or (Test-Path -LiteralPath ($outputPath + '.sha256'))) { throw 'Choose a new output ZIP; existing artifacts are not overwritten.' }
$revision = & git -C $packagingRepo rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Build from a Git checkout.' }
$dirty = & git -C $packagingRepo status --porcelain --untracked-files=normal
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
$iconSource = Join-Path $repo 'branding/icon.png'
$iconKey = 'default'
if (Test-Path -LiteralPath $iconSource -PathType Leaf) {
    $iconKey = $profile.id
    Copy-Item -LiteralPath $iconSource -Destination (Join-Path $instance ($iconKey + '.png'))
}
$guide = "# Create: Ch4oS - $selection`n`n$behavior`n`nImport this ZIP into Prism Launcher. Use Java 21 and allow the Packwiz pre-launch command.`nPack URL: $PackUrl`n`nFixed versions still download their mods from upstream providers. Use a separate instance to change versions; do not downgrade a live world.`n"
[IO.File]::WriteAllText((Join-Path $instance 'README.md'), $guide, $utf8)
$components = [ordered]@{ formatVersion = 1; components = @(
    [ordered]@{ uid = 'net.minecraft'; version = $runtime.minecraft; important = $true },
    [ordered]@{ uid = 'net.neoforged'; version = $runtime.neoforge.version; important = $true }
) }
[IO.File]::WriteAllText((Join-Path $instance 'mmc-pack.json'), ($components | ConvertTo-Json -Depth 5) + "`n", $utf8)
$config = @'
[General]
InstanceType=OneSix
name=PACK_NAME
iconKey=PACK_ICON
OverrideMemory=true
MinMemAlloc=1024
MaxMemAlloc=12288
OverrideJavaLocation=false
OverrideJavaArgs=true
JvmArgs=-XX:+UseZGC -XX:+ZGenerational
OverrideCommands=true
PreLaunchCommand="$INST_JAVA" -jar packwiz-installer-bootstrap.jar --bootstrap-no-update -s client "PACK_URL"
'@
$config = $config.Replace('PACK_NAME', $profile.name).Replace('PACK_ICON', $iconKey).Replace('PACK_URL', $PackUrl)
[IO.File]::WriteAllText((Join-Path $instance 'instance.cfg'), $config + "`n", $utf8)
$provenance = "Create: Ch4oS Prism import`nSelection: $selection`n$behavior`nHistorical profile version: $($profile.version)`nBuild source: $revision`nPack source: $packRevision`nPack address: $PackUrl`nPackwiz bootstrap: $($tools.bootstrap.version)`nPackwiz installer: $($tools.installer.version)`n"
[IO.File]::WriteAllText((Join-Path $instance 'release.txt'), $provenance, $utf8)
Add-Type -AssemblyName System.IO.Compression.FileSystem
[IO.Compression.ZipFile]::CreateFromDirectory($stage, $outputPath)
$hash = (Get-FileHash -LiteralPath $outputPath -Algorithm SHA256).Hash.ToLowerInvariant()
[IO.File]::WriteAllText(($outputPath + '.sha256'), "$hash  $([IO.Path]::GetFileName($outputPath))`n", $utf8)
Write-Output "Prism ZIP: $outputPath"
Write-Output "SHA-256: $hash"
Write-Output "Pack address: $PackUrl"
} finally {
# Only the exact temporary directories created above are eligible for cleanup.
if ($stage -and [IO.Path]::GetFullPath($stage).StartsWith([IO.Path]::GetFullPath([IO.Path]::GetTempPath()), [StringComparison]::OrdinalIgnoreCase) -and (Split-Path -Leaf $stage) -match '^ch4os-prism-[0-9a-f]{32}$') {
    Remove-Item -LiteralPath $stage -Recurse -Force
}
if ([IO.Path]::GetFullPath($sourceStage).StartsWith([IO.Path]::GetFullPath([IO.Path]::GetTempPath()), [StringComparison]::OrdinalIgnoreCase) -and (Split-Path -Leaf $sourceStage) -match '^ch4os-prism-source-[0-9a-f]{32}$') {
    Remove-Item -LiteralPath $sourceStage -Recurse -Force
}
}
