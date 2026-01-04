$ErrorActionPreference = "Stop"

$DistDir = "infra/lambda/dist"
$OutDir  = "build/lambda"
$ZipPath = "$OutDir/lambda.zip"

if (Test-Path $DistDir) {
    Remove-Item -Recurse -Force $DistDir
}

New-Item -ItemType Directory -Path $DistDir -Force | Out-Null
New-Item -ItemType Directory -Path $OutDir  -Force | Out-Null

pip install -r requirements.txt -t $DistDir

Copy-Item -Recurse -Force src/* $DistDir

if (Test-Path $ZipPath) {
    Remove-Item -Force $ZipPath
}

Compress-Archive -Path "$DistDir/*" -DestinationPath $ZipPath
