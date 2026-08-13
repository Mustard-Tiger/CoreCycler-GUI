param(
    [Parameter()]
    [String] $Source = (Join-Path $PSScriptRoot '..\corecycler')
)

$ErrorActionPreference = 'Stop'
$sourceRoot = (Resolve-Path -LiteralPath $Source).Path
$targetRoot = (Resolve-Path -LiteralPath $PSScriptRoot).Path
$engineDirectories = @('configs', 'helpers', 'test_programs', 'tools')
$engineFiles = @(
    'script-corecycler.ps1',
    'Run CoreCycler.bat',
    'Run Multiconfig CoreCycler.bat'
)

foreach ($directory in $engineDirectories) {
    $sourceDirectory = Join-Path $sourceRoot $directory
    $targetDirectory = Join-Path $targetRoot $directory
    if (!(Test-Path -LiteralPath $sourceDirectory -PathType Container)) {
        throw "CoreCycler directory not found: $sourceDirectory"
    }
    New-Item -ItemType Directory -Path $targetDirectory -Force | Out-Null
    Get-ChildItem -LiteralPath $sourceDirectory -Force |
        Copy-Item -Destination $targetDirectory -Recurse -Force
}

foreach ($file in $engineFiles) {
    $sourceFile = Join-Path $sourceRoot $file
    if (!(Test-Path -LiteralPath $sourceFile -PathType Leaf)) {
        throw "CoreCycler file not found: $sourceFile"
    }
    Copy-Item -LiteralPath $sourceFile -Destination (Join-Path $targetRoot $file) -Force
}

$versionLine = Select-String -LiteralPath (Join-Path $targetRoot 'script-corecycler.ps1') `
    -Pattern '^\$version\s*=' | Select-Object -First 1
Write-Host "CoreCycler engine synchronized. $($versionLine.Line.Trim())"
Write-Host 'GUI-only files were preserved.'
