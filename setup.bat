@echo off
REM Smart Todo List Setup Script for Windows
REM This script sets up both backend and frontend for development

echo 🚀 Smart Todo List Setup Script
echo ================================

REM Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)
python --version
echo [SUCCESS] Python found

REM Check if Node.js is installed
echo [INFO] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)
node --version
echo [SUCCESS] Node.js found

REM Check if npm is installed
echo [INFO] Checking npm installation...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed. Please install npm first.
    pause
    exit /b 1
)
npm --version
echo [SUCCESS] npm found

REM Setup backend
echo [INFO] Setting up backend...
cd backend

REM Create virtual environment
echo [INFO] Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist .env (
    echo [WARNING] No .env file found. Creating template...
    (
        echo # Django Configuration
        echo SECRET_KEY=your-django-secret-key-here
        echo DEBUG=True
        echo.
        echo # Database Configuration ^(PostgreSQL^)
        echo DB_NAME=smart_todo_db
        echo DB_USER=your_db_user
        echo DB_PASSWORD=your_db_password
        echo DB_HOST=localhost
        echo DB_PORT=5432
        echo.
        echo # AI Configuration
        echo GEMINI_API_KEY=your-gemini-api-key-here
        echo GEMINI_MODEL=gemini-2.5-flash-lite-preview-06-17
        echo.
        echo # CORS Settings
        echo CORS_ALLOWED_ORIGINS=http://localhost:3000
    ) > .env
    echo [WARNING] Please update the .env file with your actual configuration values.
) else (
    echo [SUCCESS] .env file already exists
)

REM Run migrations
echo [INFO] Running database migrations...
python manage.py makemigrations
python manage.py migrate

echo [SUCCESS] Backend setup completed!
cd ..

REM Setup frontend
echo [INFO] Setting up frontend...
cd frontend

REM Install dependencies
echo [INFO] Installing Node.js dependencies...
npm install

REM Check if .env.local file exists
if not exist .env.local (
    echo [WARNING] No .env.local file found. Creating template...
    (
        echo # Frontend Configuration
        echo NEXT_PUBLIC_API_URL=http://localhost:8000/api
    ) > .env.local
    echo [SUCCESS] .env.local file created
) else (
    echo [SUCCESS] .env.local file already exists
)

echo [SUCCESS] Frontend setup completed!
cd ..

echo.
echo 🎉 Setup completed successfully!
echo.
echo Next steps:
echo 1. Update backend\.env with your database and AI API credentials
echo 2. Start the backend server:
echo    cd backend
echo    venv\Scripts\activate
echo    python manage.py runserver
echo.
echo 3. Start the frontend server ^(in a new terminal^):
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open http://localhost:3000 in your browser
echo.
echo For detailed setup instructions, see README.md
pause 