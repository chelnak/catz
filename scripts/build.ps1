param(
    [Parameter(Mandatory=$False)]
    [Switch]$BuildForPlatform
)

$ErrorActionPreference = "Stop"
Import-Module -Name "$PSScriptRoot/BuildHelpers.psm1" -Force

New-BuildEnvironment
Set-Version
$BuildForPlatform.IsPresent ? Start-PlatformSpecificBuild : Start-GenericBuild
