$ErrorActionPreference = "Stop"
$SCRIPT:ProjectRoot = "$PSScriptRoot/.."
$SCRIPT:ArtifactsDir = "$ProjectRoot/artifacts"
$SCRIPT:Wix = "$SCRIPT:ArtifactsDir/wix"

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

function New-BuildEnvironment {
    Write-Header -Message "Preparing build environment"
    pip install -r $ProjectRoot/requirements.txt
    $null = New-Item -Path $SCRIPT:ArtifactsDir -ItemType Directory
}


function Set-Version {
    Write-Header -Message "Configuring static version number"
    $BuildVersion = $ENV:GITVERSION_MAJORMINORPATCH

    if (!$BuildVersion) {
        Write-Warning -Message "BuildVersion is not set, assuming development"
        return
    }

    $Config = Get-Content -Path "$ProjectRoot/jcat/__init__.py" -Raw
    [Version]$ConfigVersion = [regex]::matches($Config, "VERSION\s=\s'(\d*.\d*.\d*)'").Groups[1].Value
    $Config -Replace $ConfigVersion.ToString(), [Version]$BuildVersion.ToString() 
    $Config | Set-Content -Path "$ProjectRoot/jcat/__init__.py" -Force
    Write-Host "BuildVersion set to $BuildVersion"
}


function New-PyPiPackage {
    Write-Header -Message "Starting PyPi package build"
    python setup.py bdist_wheel -d $SCRIPT:ArtifactsDir
    python setup.py sdist -d $SCRIPT:ArtifactsDir
}


function New-DebPackage {
    Write-Header -Message "Starting deb package build"

    sudo apt-get install python3-stdeb python3-setuptools python3-all python-all fakeroot -y
    python setup.py --command-packages=stdeb.command bdist_deb
    Move-Item -Path $SCRIPT:ProjectRoot/deb_dist/*.deb -Destination $SCRIPT:ArtifactsDir
}


function New-MsiPackage {
    Write-Header -Message "Starting msi package build"

    $null = New-Item -Path "$SCRIPT:ArtifactsDir/test-file.txt"
    # $WixDownloadUrl = "https://github.com/wixtoolset/wix3/releases/download/wix3112rtm/wix311-binaries.zip"
    # $WixBinariesLoc = "$SCRIPT:ArtifactsDir/wix-binaries.zip"

    # if (!(Test-Path -Path WixBinariesLoc)) {
    #     Invoke-RestMethod -Method Get -Uri $WixDownloadUrl -OutFile $WixBinariesLoc
    #     Expand-Archive -Path $WixBinariesLoc -DestinationPath "$SCRIPT:ArtifactsDir/wix"
    # }
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

function Start-GenericBuild {
    Write-Header -Message "Starting platform independent build steps"

    # --- Build a generic python package
    New-PyPiPackage
}

function Start-PlatformSpecificBuild {

    $Platform = $PSVersionTable.Platform

    Write-Header -Message "Starting specific build steps [$Platform]"

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

function Start-Linter {

    Write-Header -Message "Starting flake8 linting"
    $Result = flake8 $ProjectRoot/jcat/ --max-line-length=120 --tee

    if ($Result.Count -gt 0) {
        $Result
        Write-Error -Message "$($Result.Count) issues found while linting"
    }
}