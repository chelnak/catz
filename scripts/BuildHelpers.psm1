$ErrorActionPreference = "Stop"
$SCRIPT:ProjectRoot = "$PSScriptRoot/.."
$SCRIPT:ArtifactsDir = "$ProjectRoot/artifacts"
$SCRIPT:Wix = "$SCRIPT:ArtifactsDir/wix"

$OldPythonPath = $Env:PYTHONPATH
$Env:PYTHONPATH = ""


function Write-Header {

    param(
        [Parameter(Mandatory=$True)]
        [String]$Message
    )

    $MessageLength = $Message.Length
    $Line = "#" * ($MessageLength + 10)
    $WhiteSpace = " " * 8

@"

#$Line
# $Message$WhiteSpace#
#$Line

"@
}


function Get-WixBinaries {
    $WixDownloadUrl = "https://github.com/wixtoolset/wix3/releases/download/wix3112rtm/wix311-binaries.zip"
    $WixBinariesLoc = "$SCRIPT:ArtifactsDir/wix-binaries.zip"

    if (!(Test-Path -Path WixBinariesLoc)) {
        Invoke-RestMethod -Method Get -Uri $WixDownloadUrl -OutFile $WixBinariesLoc
        Expand-Archive -Path $WixBinariesLoc -DestinationPath "$SCRIPT:ArtifactsDir/wix"
    }
}


function Set-Version {

    $BuildVersion = $ENV:GITVERSION_SEMVER

    if (!$BuildVersion) {
        Write-Host "BuildVersion is not set, assuming development"
        return
    }

    $Config = Get-Content -Path "$ProjectRoot/jcat/config/config.py" -Raw
    [Version]$ConfigVersion = [regex]::matches($Config, "'version':\s'(\d*.\d*.\d*)'").Groups[1].Value
    $Config -Replace $ConfigVersion.ToString(), [Version]$BuildVersion.ToString() 
    $Config | Set-Content -Path "$ProjectRoot/jcat/config/config.py" -Force
    Write-Host "BuildVersion set to $BuildVersion"
}


function New-PyPiPackage {

    Write-Header -Message "Starting PyPi package build"

    python setup.py bdist_wheel -d $SCRIPT:ArtifactsDir
    python setup.py sdist -d $SCRIPT:ArtifactsDir
}


function New-DebPackage {

    Write-Header -Message "Starting deb package build"

    sudo apt-get install python-stdeb fakeroot python-all -y
    python setup.py --command-packages=stdeb.command bdist_deb
    Move-Item -Path $SCRIPT:ProjectRoot/deb_dist/*.deb -Destination $SCRIPT:ArtifactsDir
}


function New-MsiPackage {

    #Get-WixBinaries

    Write-Host "WINDOWS"
    # try {
    #     pip3 install -r $ProjectRoot/requirements.txt
    
    #     Push-Location   
    #     Set-Location -Path $ProjectRoot
    
    #     Remove-Item -Path build, dist -Recurse -Force -ErrorAction SilentlyContinue
        
    #     python ./setup.py $BuildCmd
        
    #     $ArtifactPath = Get-Item -Path build/exe*
    #     $ArchiveName = $ArtifactPath.BaseName.Replace("exe", "jcat")
        
    #     $Null = New-Item -Path dist -ItemType Directory
    #     Compress-Archive -Path "$($ArtifactPath.FullName)/*" -DestinationPath dist/$ArchiveName.zip
        
    
    # } catch {
    #     Write-Error -Message "$_"
    # } finally {
    #     $Env:PYTHONPATH = $OldPythonPath 
    #     Pop-Location
    # }    

}

function Start-OsxBuild {

}



function Start-PlatformSpecificBuild {

    $Platform = $PSVersionTable.Platform

    Write-Header -Message "Starting [$Platform] platform build steps"

    switch($Platform) {
        "Win32NT" {
            New-MsiPackage
            break
        }

        "Unix" {
            $Release = Get-Content "/etc/os-release" -Raw | ConvertFrom-StringData
            New-DebPackage
            break
        }
    }

}