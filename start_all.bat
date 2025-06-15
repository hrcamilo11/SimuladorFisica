@echo off

REM Iniciar el backend
start cmd /k "cd backend && pip install -r requirements.txt && cd .. && python -m backend.main"

REM Iniciar el frontend
start cmd /k "cd frontend && npm install && npm run dev"