$ErrorActionPreference = 'Stop'

Write-Host "Starting AAROHAN Prototype Demo..." -ForegroundColor Cyan

# Start Backend
Write-Host "Starting FastAPI Backend on port 8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; if (!(Test-Path .venv)) { python -m venv .venv }; .\.venv\Scripts\activate; pip install -r requirements.txt; uvicorn app.main:app --reload --port 8000"

# Start Frontend
Write-Host "Starting Next.js Frontend on port 3000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm install; npm run dev"

Write-Host "Done! The application will open shortly." -ForegroundColor Cyan
Write-Host "Backend API: http://localhost:8000/docs"
Write-Host "Frontend App: http://localhost:3000"
