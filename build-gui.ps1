param(
    [Parameter()]
    [String] $Python = (Join-Path $PSScriptRoot '..\.venv\Scripts\python.exe')
)

$ErrorActionPreference = 'Stop'
$pythonPath = (Resolve-Path -LiteralPath $Python).Path

Push-Location $PSScriptRoot
try {
    & $pythonPath -m PyInstaller --noconfirm --clean CoreCycler.spec
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller failed with exit code $LASTEXITCODE"
    }
    $builtExecutable = Join-Path $PSScriptRoot 'dist\CoreCycler.exe'
    $targetExecutable = Join-Path $PSScriptRoot 'CoreCycler.exe'
    try {
        Copy-Item -LiteralPath $builtExecutable -Destination $targetExecutable -Force
        Write-Host 'Built CoreCycler.exe beside the CoreCycler engine files.'
    }
    catch [System.IO.IOException] {
        $pendingExecutable = Join-Path $PSScriptRoot 'CoreCycler.new.exe'
        try {
            Copy-Item -LiteralPath $builtExecutable -Destination $pendingExecutable -Force
        }
        catch [System.IO.IOException] {
            $pendingExecutable = Join-Path $PSScriptRoot `
                ('CoreCycler.' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.exe')
            Copy-Item -LiteralPath $builtExecutable -Destination $pendingExecutable
        }
        Write-Warning 'CoreCycler.exe is currently running and could not be replaced.'
        Write-Host "The updated build was saved as $([IO.Path]::GetFileName($pendingExecutable))."
    }
}
finally {
    Pop-Location
}
