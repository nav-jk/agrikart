@echo off
cd /d %~dp0

:: Start Backend (Django)
start "" /min cmd /c "cd C:\Users\navan\Documents\Home\SeriousStuff\agrikart\agrikart && python manage.py runserver"

:: Start Frontend (React + Vite)
start "" /min cmd /c "cd C:\Users\navan\Documents\Home\SeriousStuff\agrikart\agrikart-frontend && npm run dev"

:: Wait a few seconds for frontend to start, then open it
timeout /t 2 >nul
start "" "http://localhost:5173"



