#!/bin/bash

# Smart Todo List Setup Script
# This script sets up both backend and frontend for development

set -e  # Exit on any error

echo "🚀 Smart Todo List Setup Script"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python is not installed. Please install Python 3.8+ first."
        exit 1
    fi
}

# Check if Node.js is installed
check_node() {
    print_status "Checking Node.js installation..."
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js $NODE_VERSION found"
    else
        print_error "Node.js is not installed. Please install Node.js 18+ first."
        exit 1
    fi
}

# Check if npm is installed
check_npm() {
    print_status "Checking npm installation..."
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_success "npm $NPM_VERSION found"
    else
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Create virtual environment
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install requirements
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Check if .env file exists
    if [ ! -f .env ]; then
        print_warning "No .env file found. Creating template..."
        cat > .env << EOF
# Django Configuration
SECRET_KEY=your-django-secret-key-here
DEBUG=True

# Database Configuration (PostgreSQL)
DB_NAME=smart_todo_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# AI Configuration
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.5-flash-lite-preview-06-17

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000
EOF
        print_warning "Please update the .env file with your actual configuration values."
    else
        print_success ".env file already exists"
    fi
    
    # Run migrations
    print_status "Running database migrations..."
    python manage.py makemigrations
    python manage.py migrate
    
    print_success "Backend setup completed!"
    cd ..
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    # Check if .env.local file exists
    if [ ! -f .env.local ]; then
        print_warning "No .env.local file found. Creating template..."
        cat > .env.local << EOF
# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api
EOF
        print_success ".env.local file created"
    else
        print_success ".env.local file already exists"
    fi
    
    print_success "Frontend setup completed!"
    cd ..
}

# Main setup function
main() {
    echo "Starting setup process..."
    
    # Check prerequisites
    check_python
    check_node
    check_npm
    
    # Setup backend
    setup_backend
    
    # Setup frontend
    setup_frontend
    
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Update backend/.env with your database and AI API credentials"
    echo "2. Start the backend server:"
    echo "   cd backend"
    echo "   source venv/bin/activate"
    echo "   python manage.py runserver"
    echo ""
    echo "3. Start the frontend server (in a new terminal):"
    echo "   cd frontend"
    echo "   npm run dev"
    echo ""
    echo "4. Open http://localhost:3000 in your browser"
    echo ""
    echo "For detailed setup instructions, see README.md"
}

# Run main function
main "$@" 