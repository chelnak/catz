param(
    [Parameter(Mandatory=$False)]
    [Switch]$BuildForPlatform
)

$ErrorActionPreference = "Stop"
$ProjectRoot = "$PSScriptRoot/.."

Import-Module -Name "$PSScriptRoot/BuildHelpers.psm1" -Force

Set-Version

# --- Start multi platform build if true, otherwise default.
if ($BuildForPlatform.IsPresent) {
    Start-PlatformSpecificBuild
} else {
    # --- Default - Build a generic python package
    New-PyPiPackage
}
