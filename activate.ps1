# Check if venv exists, create if not
if (-not (Test-Path ".\venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    python -m venv venv
    
    Write-Host "Installing dependencies..." -ForegroundColor Green
    .\venv\Scripts\pip install -r requirements.txt
}

# Activate the virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
.\venv\Scripts\Activate.ps1

# Optional: Set environment variables from .env file
if (Test-Path ".\.env") {
    Write-Host "Loading environment variables..." -ForegroundColor Green
    Get-Content .\.env | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }
}

Write-Host "Environment ready!" -ForegroundColor Green

