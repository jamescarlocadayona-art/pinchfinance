$ErrorActionPreference = 'Stop'

$installDir = Join-Path $env:LOCALAPPDATA 'Programs\PinchFinance'
$sourceExe = Join-Path $PSScriptRoot 'PinchFinance.exe'
$targetExe = Join-Path $installDir 'PinchFinance.exe'
$startMenuDir = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Pinch Finance'
$shortcutPath = Join-Path $startMenuDir 'Pinch Finance.lnk'
$desktopShortcut = Join-Path ([Environment]::GetFolderPath('Desktop')) 'Pinch Finance.lnk'

if (-not (Test-Path $sourceExe)) {
    throw "PinchFinance.exe must be in the same folder as this installer."
}

New-Item -ItemType Directory -Force -Path $installDir | Out-Null
New-Item -ItemType Directory -Force -Path $startMenuDir | Out-Null
Copy-Item $sourceExe $targetExe -Force

$wsh = New-Object -ComObject WScript.Shell
foreach ($linkPath in @($shortcutPath, $desktopShortcut)) {
    $shortcut = $wsh.CreateShortcut($linkPath)
    $shortcut.TargetPath = $targetExe
    $shortcut.WorkingDirectory = $installDir
    $shortcut.Description = 'Pinch Finance'
    $shortcut.Save()
}

Start-Process $targetExe
Write-Host "Pinch Finance installed to $installDir"
Write-Host "Your finance database will be stored in $env:LOCALAPPDATA\PinchFinance"
