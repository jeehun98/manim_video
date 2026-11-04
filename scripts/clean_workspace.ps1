param([switch]$Apply)

# Default: report only. Run with -Apply after stopping all renders.
$ErrorActionPreference = 'Stop'
$workspaceRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$prefix = $workspaceRoot.TrimEnd('\') + '\'
$cacheNames = @('__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache')
$targets = [Collections.Generic.List[string]]::new()

function Find-CleanupTargets([string]$Directory) {
    foreach ($item in Get-ChildItem -LiteralPath $Directory -Force) {
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
        if ($item.PSIsContainer) {
            if ($item.Name -in @('.git', '.venv', '.tools', 'archive', 'exports')) { continue }
            $inMedia = $item.FullName.StartsWith((Join-Path $workspaceRoot 'media') + '\', [StringComparison]::OrdinalIgnoreCase)
            if ($item.Name -in $cacheNames -or ($inMedia -and $item.Name -in @('partial_movie_files', 'Tex', 'texts'))) {
                $targets.Add($item.FullName)
            } else { Find-CleanupTargets $item.FullName }
        } elseif ($item.Extension -eq '.log' -and (
            $Directory -eq $workspaceRoot -or
            $item.FullName.StartsWith((Join-Path $workspaceRoot 'episodes') + '\', [StringComparison]::OrdinalIgnoreCase) -or
            $item.FullName.StartsWith((Join-Path $workspaceRoot 'longforms') + '\', [StringComparison]::OrdinalIgnoreCase))) {
            $targets.Add($item.FullName)
        }
    }
}

Find-CleanupTargets $workspaceRoot
$bytes = 0L
$files = 0
foreach ($target in $targets) {
    $resolved = [IO.Path]::GetFullPath($target)
    if (-not $resolved.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Target outside workspace: $resolved"
    }
    $item = Get-Item -LiteralPath $resolved
    $contents = if ($item.PSIsContainer) { @(Get-ChildItem -LiteralPath $resolved -File -Recurse -Force) } else { @($item) }
    $files += $contents.Count
    $bytes += ($contents | Measure-Object Length -Sum).Sum
    if ($Apply) { Remove-Item -LiteralPath $resolved -Recurse -Force }
}
[pscustomobject]@{ Applied = [bool]$Apply; Targets = $targets.Count; Files = $files; MiB = [math]::Round($bytes / 1MB, 2) }
