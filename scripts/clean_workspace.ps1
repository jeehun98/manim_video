param([switch]$Apply, [switch]$Generated)

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
            if ($item.Name -in @('.git', '.venv', '.tools', 'archive')) { continue }
            if ($Generated -and $item.Name -eq 'media') {
                $targets.Add($item.FullName)
                continue
            }
            if ($item.Name -eq 'exports' -and -not $Generated) { continue }
            $inMedia = $item.FullName.StartsWith((Join-Path $workspaceRoot 'media') + '\', [StringComparison]::OrdinalIgnoreCase)
            if ($item.Name -in $cacheNames -or ($inMedia -and $item.Name -in @('partial_movie_files', 'Tex', 'texts'))) {
                $targets.Add($item.FullName)
            } else { Find-CleanupTargets $item.FullName }
        } elseif ($Generated -and (Test-GeneratedFile $item)) {
            $targets.Add($item.FullName)
        } elseif ($item.Extension -eq '.log' -and (
            $Directory -eq $workspaceRoot -or
            $item.FullName.StartsWith((Join-Path $workspaceRoot 'episodes') + '\', [StringComparison]::OrdinalIgnoreCase) -or
            $item.FullName.StartsWith((Join-Path $workspaceRoot 'longforms') + '\', [StringComparison]::OrdinalIgnoreCase))) {
            $targets.Add($item.FullName)
        }
    }
}

function Test-GeneratedFile($Item) {
    $relative = $Item.FullName.Substring($prefix.Length).Replace('\', '/')
    # Keep source audio and its same-stem video container (potential user input).
    if ($relative.StartsWith('exports/')) {
        if ($Item.Extension -in @('.mp3', '.wav', '.m4a', '.flac', '.ogg')) { return $false }
        foreach ($extension in @('.mp3', '.wav', '.m4a', '.flac', '.ogg')) {
            if (Test-Path -LiteralPath ([IO.Path]::ChangeExtension($Item.FullName, $extension))) { return $false }
        }
        return $Item.Extension -in @('.mp4', '.mov', '.webm', '.png', '.jpg', '.jpeg', '.svg', '.log')
    }
    if ($relative -notmatch '^(episodes|longforms|quantum_series)/') { return $false }
    if ($relative.StartsWith('longforms/svd05_lost_information/assets/')) { return $true }
    if ($Item.Extension -eq '.ass' -and $Item.Name -like 'captions*') { return $true }
    if ($Item.Extension -in @('.mp4', '.webm', '.pyc', '.pyo', '.log', '.o', '.obj')) { return $true }
    if ($Item.Extension -eq '.exe') {
        return (Test-Path -LiteralPath ([IO.Path]::ChangeExtension($Item.FullName, '.cu')))
    }
    if ($Item.Extension -in @('.png', '.jpg', '.jpeg') -and $relative -notmatch '/assets/') {
        return $relative -match '/qa(/|_)|/(check[^/]*|preview[^/]*|final_\d[^/]*|source\d+_check)\.(png|jpg|jpeg)$'
    }
    if ($Item.Name -match '^(concat.*\.txt|(preview_report|render_report|geometry_check|qa_final).*\.json|geometry_(shorts|longform)_\d+\.json|states_(shorts|longform)_\d+\.json)$') { return $true }
    # These numerical outputs have checked-in generation scripts.
    return $relative -in @(
        'episodes/science05_gravitational_collapse/collapse_data.npz',
        'longforms/svd05_lost_information/assets/svd_data.npz',
        'longforms/minimal_nn03_impact/demonstration_data.npz',
        'longforms/minimal06_universality/simulation_data.npz',
        'longforms/nature02_catenary/dynamics.npz',
        'longforms/minimal07_lottery/experiment_data.npz'
    )
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
[pscustomobject]@{ Applied = [bool]$Apply; Generated = [bool]$Generated; Targets = $targets.Count; Files = $files; MiB = [math]::Round($bytes / 1MB, 2) }
