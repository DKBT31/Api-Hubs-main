# ResumeAI Parser - Virtual Environment Startup Script
# Clean, single-run startup for the ResumeAI Parser

Write-Host ""
Write-Host "ResumeAI Parser - Starting in Virtual Environment" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan

# Check if virtual environment exists
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
    Write-Host "Run: python -m venv .venv" -ForegroundColor Yellow
    Write-Host "Then: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Add Tesseract to PATH (if available)
$tesseractPath = "C:\Program Files\Tesseract-OCR"
if (Test-Path "$tesseractPath\tesseract.exe") {
    $env:PATH += ";$tesseractPath"
    Write-Host "Tesseract found and added to PATH" -ForegroundColor Green
} else {
    Write-Host "Tesseract not found - will use EasyOCR only" -ForegroundColor Yellow
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .venv\Scripts\Activate.ps1

# Display environment info
Write-Host "Virtual Environment Info:" -ForegroundColor Cyan
Write-Host "Python: $((& .venv\Scripts\python.exe --version))" -ForegroundColor White
$packageCount = (& .venv\Scripts\pip.exe list | Measure-Object).Count - 2
Write-Host "   Packages: $packageCount installed" -ForegroundColor White

Write-Host ""
Write-Host "Starting ResumeAI Parser..." -ForegroundColor Green
Write-Host "API Documentation: http://127.0.0.1:9003/docs" -ForegroundColor Cyan
Write-Host "Upload Endpoint: http://127.0.0.1:9003/upload" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server using virtual environment Python
& .venv\Scripts\python.exe main.py