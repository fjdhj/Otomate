#Set-ExecutionPolicy RemoteSigned

# Install Chocolatey (a package manager for Windows, if not already installed)
Set-ExecutionPolicy Bypass -Scope Process -Force;
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;
Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install graphviz using Chocolatey
choco install graphviz -y

# Install Python packages using pip
pip install pandas
pip install graphviz

Write-Host "Installation completed!"
