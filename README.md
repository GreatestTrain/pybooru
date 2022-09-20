

# Installation

* Michaelsoft Bindows:
````
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/GreatestTrain/pybooru/main/install.ps1'))
````

* Unix-like OS:
````
curl -H 'Cache-Control: no-cache, no-store' https://raw.githubusercontent.com/GreatestTrain/pybooru/main/install.sh | sh
````