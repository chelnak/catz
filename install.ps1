$JcatPath = "$ENV:USERPROFILE\AppData\Local\Programs\jcat"
$ENV:PATH="$ENV:PATH;$JcatPath"

$LatestRelease = Invoke-RestMethod -Method Get -Uri "https://api.github.com/repos/chelnak/jcat/releases/latest"
$LatestAsset = $LatestRelease.assets.Where{$_.name -Like "*.msi"}

Invoke-RestMethod -Method Get -Uri $LatestAsset.browser_download_url -OutFile $ENV:TEMP/$LatestAsset.name -FollowRelLink

& msiexec /i $ENV:TEMP\$LatestAsset.name

Write-Warning -Message "$JcatPath needs to be added to the PATH environment variable"