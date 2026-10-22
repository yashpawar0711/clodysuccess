@echo off
title Cloudy Success Django Server
color 0b
echo =======================================================
echo   CLOUDY SUCCESS - High-Performance Web Agency Studio
echo   Founder: Yash Pawar
echo =======================================================
echo.
echo Activating Virtual Environment 'env'...
call env\Scripts\activate.bat
echo Starting Django Server on http://127.0.0.1:8000/ ...
echo.
echo - Website:      http://127.0.0.1:8000/
echo - Admin Portal: http://127.0.0.1:8000/admin/
echo - Admin User:   admin  (Password: admin123)
echo.
python manage.py runserver 8000
pause
