# 🤖 Smart Todo List with AI Integration

A full-stack web application for intelligent task management with AI-powered features like task prioritization, deadline suggestions, and context-aware recommendations.

## 🚀 Features

### Core Features
- ✅ **Task Management**: Create, edit, delete, and organize tasks
- ✅ **Smart Categorization**: AI-powered task categorization and tag suggestions
- ✅ **Priority Scoring**: AI-driven priority calculation based on context
- ✅ **Deadline Suggestions**: Intelligent deadline recommendations
- ✅ **Context Analysis**: Analyze emails, messages, and notes for task extraction
- ✅ **Task Enhancement**: AI-powered task description improvements

### AI Integration
- 🤖 **Google Gemini AI**: Advanced language model for intelligent analysis
- 📊 **Context Processing**: Extract actionable tasks from daily context
- 🎯 **Smart Prioritization**: AI-driven task ranking and urgency assessment
- 📅 **Intelligent Scheduling**: Deadline suggestions based on workload and complexity
- 🏷️ **Auto-categorization**: Smart category and tag suggestions

### User Interface
- 🎨 **Modern Design**: Clean, responsive interface with Tailwind CSS
- 🌙 **Dark Mode**: Automatic dark/light mode based on system preference
- 📱 **Mobile Responsive**: Works seamlessly on all devices
- ⚡ **Real-time Updates**: Instant feedback and updates

## 🏗️ Architecture

```
Smart Todo List/
├── backend/                 # Django REST API
│   ├── ai_service/         # AI integration services
│   ├── services/           # Business logic layer
│   ├── todo/              # Main Django app
│   └── tasks/             # AI-specific views
└── frontend/              # Next.js React app
    ├── src/
    │   ├── app/           # Next.js app router
    │   ├── components/    # React components
    │   ├── services/      # API client
    │   └── types/         # TypeScript definitions
```

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 18+**
- **PostgreSQL** (or Supabase account)
- **Google AI API Key** (Gemini)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd smart-todo-list
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the `backend/` directory:

```bash
# .env
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
```

#### Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

#### Start Backend Server
```bash
python manage.py runserver
```

The backend will be available at: `http://localhost:8000`

### 3. Frontend Setup

#### Install Node.js Dependencies
```bash
cd frontend
npm install
```

#### Environment Configuration
Create a `.env.local` file in the `frontend/` directory:

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

#### Start Frontend Development Server
```bash
npm run dev
```

The frontend will be available at: `http://localhost:3000`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Core Endpoints

#### Tasks
- `GET /tasks/` - Get all tasks
- `POST /tasks/` - Create new task
- `GET /tasks/{id}/` - Get specific task
- `PUT /tasks/{id}/` - Update task
- `DELETE /tasks/{id}/` - Delete task

#### Categories
- `GET /categories/` - Get all categories
- `POST /categories/` - Create new category

#### Context
- `GET /context/` - Get context entries
- `POST /context/` - Add context entry

### AI Endpoints

#### AI Health Check
```bash
GET /ai/health-check/
```
Response:
```json
{
  "status": "success",
  "ai_health": {
    "services_available": true,
    "gemini_client": true,
    "ai_pipeline": true
  },
  "model_info": {
    "current_model": "gemini-2.5-flash-lite-preview-06-17",
    "current_model_info": {
      "description": "Fast, cost-effective model with high rate limits",
      "best_for": "Structured analysis, JSON generation, task management"
    }
  }
}
```

#### Context Analysis
```bash
POST /ai/analyze-context/
```
Request:
```json
{
  "context": {
    "content": "Meeting scheduled for Friday. Need to prepare quarterly report.",
    "source": "email",
    "timestamp": "2024-01-01T10:00:00Z"
  }
}
```

#### Task Processing
```bash
POST /ai/process-task/
```
Request:
```json
{
  "task": {
    "title": "Prepare quarterly report",
    "description": "Create comprehensive quarterly sales report"
  },
  "context": {
    "content": "Deadline is Friday, client meeting scheduled"
  }
}
```

## 🧪 Sample Data

### Sample Context Data for Testing

#### Email Context
```
Subject: Client Meeting Preparation
From: manager@company.com
Date: 2024-01-01

Hi team,

We have a client meeting scheduled for Friday at 2 PM. Please prepare the quarterly sales report and have the new product demo ready. The client is particularly interested in our Q4 performance and upcoming features.

Also, don't forget to update the project documentation by end of this week.

Best regards,
Manager
```

#### WhatsApp Messages
```
[10:30 AM] Team Lead: Hey team, just got an email from the client. They want to move the project deadline to this Friday instead of next week.

[10:35 AM] Developer: That's tight! We need to finish the backend API integration and update documentation.

[10:40 AM] Designer: I'll prioritize the UI mockups for the new features.
```

#### Meeting Notes
```
Project Review Meeting - 2024-01-01

Action Items:
1. Complete backend API integration by Wednesday
2. Update project documentation by Friday
3. Prepare client presentation for Friday meeting
4. Test new features before demo

Deadlines:
- API Integration: Wednesday
- Documentation: Friday
- Client Meeting: Friday 2 PM
```

### Sample Tasks Generated by AI

```json
{
  "extracted_tasks": [
    {
      "title": "Prepare Quarterly Sales Report",
      "description": "Create comprehensive report for client meeting on Friday",
      "priority": "high",
      "deadline": "2024-01-05",
      "category": "Reports",
      "confidence": 0.95
    },
    {
      "title": "Update Project Documentation",
      "description": "Complete documentation updates by end of week",
      "priority": "medium",
      "deadline": "2024-01-05",
      "category": "Documentation",
      "confidence": 0.88
    },
    {
      "title": "Prepare Product Demo",
      "description": "Set up and test new product features for client demo",
      "priority": "high",
      "deadline": "2024-01-05",
      "category": "Presentations",
      "confidence": 0.92
    }
  ]
}
```

## 🎯 Usage Examples

### 1. Creating a Task with AI Enhancement

1. Navigate to the Dashboard
2. Click "Add Task"
3. Enter basic task information
4. Use AI suggestions for:
   - Priority level
   - Category selection
   - Deadline recommendations
   - Description enhancement

### 2. Context Analysis

1. Go to the Context page
2. Paste your context data (emails, messages, notes)
3. Click "Analyze Context"
4. Review AI-generated:
   - Extracted tasks
   - Priority suggestions
   - Deadline recommendations
   - Category suggestions

### 3. Smart Task Management

1. View tasks on the Dashboard
2. Use filters to organize by:
   - Status (Pending, In Progress, Completed)
   - Priority (High, Medium, Low)
   - Category
   - Search terms
3. Edit tasks with AI-powered suggestions

## 🔧 Configuration Options

### AI Model Selection

You can switch between different AI models by setting the `GEMINI_MODEL` environment variable:

```bash
# For highest rate limits (development)
GEMINI_MODEL=gemini-2.5-flash-lite-preview-06-17

# For standard performance
GEMINI_MODEL=gemini-2.5-flash

# For very high rate limits
GEMINI_MODEL=gemma-3-2b

# For complex analysis
GEMINI_MODEL=gemma-3-9b
```

See [AI Model Configuration Guide](backend/AI_MODEL_CONFIGURATION.md) for detailed information.

### Database Configuration

The application supports PostgreSQL. For production, consider using Supabase:

1. Create a Supabase project
2. Get your database credentials
3. Update the `.env` file with Supabase connection details

## 🚀 Deployment

### Backend Deployment

#### Using Railway
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push

#### Using Heroku
```bash
# Install Heroku CLI
heroku create your-app-name
heroku config:set SECRET_KEY=your-secret-key
heroku config:set GEMINI_API_KEY=your-api-key
git push heroku main
```

### Frontend Deployment

#### Using Vercel
1. Connect your GitHub repository to Vercel
2. Set environment variables
3. Deploy automatically

#### Using Netlify
1. Connect your repository to Netlify
2. Set build command: `npm run build`
3. Set publish directory: `out`

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

### AI Service Tests
```bash
cd backend
python -c "
import asyncio
from ai_service import GeminiAIService
from services import AIServiceFactory

async def test_ai():
    factory = AIServiceFactory()
    print('AI Services Available:', factory.services_available)
    print('Model Info:', factory.get_model_info())

asyncio.run(test_ai())
"
```

## 🐛 Troubleshooting

### Common Issues

#### AI Services Not Available
1. Check `GEMINI_API_KEY` is set correctly
2. Verify API key has sufficient quota
3. Check network connectivity

#### Database Connection Issues
1. Verify PostgreSQL is running
2. Check database credentials in `.env`
3. Ensure database exists

#### Frontend API Errors
1. Verify backend is running on port 8000
2. Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`
3. Ensure CORS is configured correctly

### Rate Limit Issues
If you encounter rate limit errors:
1. Switch to `gemini-2.5-flash-lite-preview-06-17` model
2. Implement request throttling
3. Check your API quota in Google AI Studio

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the troubleshooting section

---

**Built with ❤️ using Django, Next.js, and Google Gemini AI** 