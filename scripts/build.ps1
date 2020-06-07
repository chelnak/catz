$ErrorActionPreference = "Stop"
$ProjectRoot = "$PSScriptRoot/.."

Import-Module -Name "$PSScriptRoot/BuildHelpers.psm1" -Force

Set-Version

New-PyPiPackage

Start-PlatformSpecificBuild
