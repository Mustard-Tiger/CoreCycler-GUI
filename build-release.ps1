param(
    [string]$OutputDirectory = (Join-Path (Split-Path -Parent $PSScriptRoot) "CoreCycler-GUI-Release")
)

$ErrorActionPreference = "Stop"
$sourceDirectory = $PSScriptRoot
$outputDirectory = [System.IO.Path]::GetFullPath($OutputDirectory)
$expectedParent = [System.IO.Path]::GetFullPath((Split-Path -Parent $sourceDirectory))

if ((Split-Path -Parent $outputDirectory) -ne $expectedParent) {
    throw "The release directory must be an immediate child of $expectedParent"
}

if (Test-Path -LiteralPath $outputDirectory) {
    Remove-Item -LiteralPath $outputDirectory -Recurse -Force
}

New-Item -ItemType Directory -Path $outputDirectory | Out-Null

$rootFiles = @(
    "CHANGELOG.txt",
    "CORECYCLER-README.txt",
    "CoreCycler.exe",
    "icon.ico",
    "LICENSE",
    "README.md",
    "Run CoreCycler.bat",
    "script-corecycler.ps1",
    "THIRD_PARTY_NOTICES.md"
)

foreach ($file in $rootFiles) {
    Copy-Item -LiteralPath (Join-Path $sourceDirectory $file) -Destination $outputDirectory
}

foreach ($directory in @("configs", "helpers")) {
    Copy-Item -LiteralPath (Join-Path $sourceDirectory $directory) -Destination $outputDirectory -Recurse
}

$releaseTestPrograms = Join-Path $outputDirectory "test_programs"
New-Item -ItemType Directory -Path $releaseTestPrograms | Out-Null

foreach ($program in @("linpack", "p95", "y-cruncher", "y-cruncher-0.7.10")) {
    Copy-Item -LiteralPath (Join-Path $sourceDirectory "test_programs\$program") -Destination $releaseTestPrograms -Recurse
}

# AIDA64 is third-party trial software and is intentionally not redistributed.
# Keep only the project's installation instructions, as in the original release.
$releaseAida64 = Join-Path $releaseTestPrograms "aida64"
New-Item -ItemType Directory -Path $releaseAida64 | Out-Null
Copy-Item -LiteralPath (Join-Path $sourceDirectory "test_programs\aida64\aida64.txt") -Destination $releaseAida64

$releaseTools = Join-Path $outputDirectory "tools"
New-Item -ItemType Directory -Path $releaseTools | Out-Null

foreach ($tool in @("IntelVoltageControl", "ryzen-smu-cli", "SMUDebugTool", "ZenTimings")) {
    Copy-Item -LiteralPath (Join-Path $sourceDirectory "tools\$tool") -Destination $releaseTools -Recurse
}

foreach ($file in Get-ChildItem -LiteralPath (Join-Path $sourceDirectory "tools") -File) {
    Copy-Item -LiteralPath $file.FullName -Destination $releaseTools
}

$archivePath = "$outputDirectory.zip"
if (Test-Path -LiteralPath $archivePath) {
    Remove-Item -LiteralPath $archivePath -Force
}

Compress-Archive -LiteralPath $outputDirectory -DestinationPath $archivePath -CompressionLevel Optimal

$releaseBytes = (Get-ChildItem -LiteralPath $outputDirectory -File -Recurse | Measure-Object -Property Length -Sum).Sum
$archiveBytes = (Get-Item -LiteralPath $archivePath).Length

[PSCustomObject]@{
    ReleaseDirectory = $outputDirectory
    ReleaseSizeMB = [math]::Round($releaseBytes / 1MB, 2)
    Archive = $archivePath
    ArchiveSizeMB = [math]::Round($archiveBytes / 1MB, 2)
}
