@echo off

REM Iniciar el backend
start cmd /k "cd frontend\backend && pip install -r requirements.txt && python main.py"

REM Iniciar el frontend
start cmd /k "cd frontend && npm install && npm run dev"