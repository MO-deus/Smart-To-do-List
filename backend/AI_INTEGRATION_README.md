# 🤖 AI Integration for Smart Todo List

This document describes the AI integration features added to the Smart Todo List application using Google Gemini API.

## 🚀 Features

### 1. **Context Analysis**
- Analyzes WhatsApp messages, emails, and notes
- Extracts actionable tasks from context
- Identifies priority indicators and deadlines
- Provides workload insights

### 2. **AI-Powered Task Enhancement**
- Improves task descriptions with more details
- Suggests actionable steps for complex tasks
- Adds relevant context and background information
- Identifies missing elements and improvements

### 3. **Smart Priority Scoring**
- AI-driven priority calculation based on:
  - Urgency factors
  - Importance assessment
  - Context relevance
  - Workload impact
  - Task dependencies
- Provides detailed reasoning for priority levels

### 4. **Intelligent Deadline Suggestions**
- Analyzes task complexity and time requirements
- Considers current workload and schedule
- Suggests realistic deadlines with confidence scores
- Provides multiple deadline options (conservative, realistic, aggressive)

### 5. **Smart Category Suggestions**
- AI-powered task categorization
- Suggests new categories based on task content
- Matches tasks to existing categories
- Provides confidence scores for suggestions

## 🏗️ Architecture

### AI Service Components

```
ai_service/
├── __init__.py                 # Package initialization
├── gemini_client.py           # Google Gemini API wrapper
├── context_analyzer.py        # Context analysis service
├── task_enhancer.py           # Task enhancement service
├── priority_scorer.py         # Priority scoring service
├── deadline_suggester.py      # Deadline suggestion service
├── category_suggester.py      # Category suggestion service
└── pipeline_controller.py     # Main pipeline orchestrator
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/ai/process-task/` | POST | Process task through full AI pipeline |
| `/api/ai/create-enhanced-task/` | POST | Create task with AI enhancement |
| `/api/ai/batch-process/` | POST | Process multiple tasks |
| `/api/ai/health-check/` | GET | Check AI services health |
| `/api/ai/statistics/` | GET | Get AI pipeline statistics |
| `/api/ai/suggest-category/` | POST | Get category suggestions |
| `/api/ai/enhance-description/` | POST | Enhance task description |
| `/api/ai/analyze-context/` | POST | Analyze context data |

## 🛠️ Setup Instructions

### 1. **Install Dependencies**
```bash
cd backend
pip install google-genai
```

### 2. **Set Environment Variables**
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

### 3. **Test AI Services**
```bash
python test_ai_services.py
```

### 4. **Start the Backend Server**
```bash
python manage.py runserver
```

## 📝 Usage Examples

### Process a New Task with AI
```python
import requests

# Task data
task_data = {
    "title": "Prepare presentation for client meeting",
    "description": "Need to create slides for quarterly review"
}

# Context data (optional)
context_data = {
    "whatsapp_messages": [
        {"content": "Meeting scheduled for Friday", "timestamp": "2024-01-01T10:00:00Z"}
    ],
    "emails": [
        {"subject": "Client meeting prep", "body": "Please prepare slides by Thursday", "timestamp": "2024-01-01T09:00:00Z"}
    ]
}

# Process through AI pipeline
response = requests.post("http://localhost:8000/api/ai/process-task/", json={
    "task": task_data,
    "context": context_data
})

result = response.json()
print(f"Priority: {result['ai_analysis']['recommendations']['priority_level']}")
print(f"Category: {result['ai_analysis']['recommendations']['suggested_category']}")
print(f"Deadline: {result['ai_analysis']['recommendations']['suggested_deadline']}")
```

### Create Enhanced Task
```python
# Create task with AI enhancement
response = requests.post("http://localhost:8000/api/ai/create-enhanced-task/", json={
    "task": task_data,
    "context": context_data,
    "auto_create": True  # Automatically create the task
})

result = response.json()
if result['created_task']:
    print(f"Task created with ID: {result['created_task']['id']}")
```

### Get Category Suggestions
```python
response = requests.post("http://localhost:8000/api/ai/suggest-category/", json={
    "task": task_data
})

suggestions = response.json()['category_suggestions']
for suggestion in suggestions['suggested_categories']:
    print(f"Category: {suggestion['name']} (Confidence: {suggestion['confidence']})")
```

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### AI Service Settings
The AI services can be configured in the individual service files:

- **Priority Scoring Weights**: Adjust in `priority_scorer.py`
- **Deadline Calculation**: Modify in `deadline_suggester.py`
- **Context Analysis**: Customize in `context_analyzer.py`

## 🧪 Testing

### Run AI Service Tests
```bash
python test_ai_services.py
```

### Test Individual Components
```python
from ai_service import GeminiAIService, AIPipelineController

# Test Gemini client
gemini = GeminiAIService()
response = await gemini.generate_content("Test message")

# Test full pipeline
pipeline = AIPipelineController(gemini)
result = await pipeline.process_new_task(task_data)
```

## 📊 API Response Format

### Successful Response
```json
{
    "status": "success",
    "ai_analysis": {
        "task_id": "uuid",
        "pipeline_status": "completed",
        "overall_confidence": 0.85,
        "summary": "AI analysis summary...",
        "recommendations": {
            "enhanced_description": "Enhanced task description",
            "suggested_category": {"name": "Work", "confidence": 0.9},
            "priority_level": "high",
            "suggested_deadline": {"deadline": "2024-01-05", "type": "realistic"},
            "actionable_steps": [...]
        },
        "detailed_analysis": {
            "context_analysis": {...},
            "task_enhancement": {...},
            "category_suggestion": {...},
            "priority_analysis": {...},
            "deadline_suggestion": {...}
        }
    }
}
```

### Error Response
```json
{
    "error": "Error message",
    "status": "error"
}
```

## 🚨 Error Handling

The AI services include comprehensive error handling:

- **API Key Issues**: Clear error messages for missing/invalid API keys
- **Network Errors**: Graceful handling of API timeouts and connection issues
- **Invalid Input**: Validation of input data with helpful error messages
- **Service Unavailable**: Fallback responses when AI services are down

## 🔒 Security Considerations

- API keys are stored as environment variables
- All AI API calls are made server-side
- Input validation prevents malicious requests
- Error messages don't expose sensitive information

## 📈 Performance

- **Async Processing**: All AI operations are asynchronous
- **Caching**: Consider implementing response caching for repeated requests
- **Batch Processing**: Support for processing multiple tasks efficiently
- **Health Monitoring**: Built-in health checks for all services

## 🔮 Future Enhancements

- **Learning from User Feedback**: Improve suggestions based on user acceptance
- **Custom AI Models**: Support for fine-tuned models
- **Advanced Context Integration**: Calendar, weather, and external data sources
- **Real-time Processing**: WebSocket support for live AI suggestions
- **Multi-language Support**: AI processing in multiple languages

## 🆘 Troubleshooting

### Common Issues

1. **"AI services are not available"**
   - Check if `GEMINI_API_KEY` is set
   - Verify API key is valid
   - Check network connectivity

2. **"Priority scoring failed"**
   - Ensure task data includes title and description
   - Check if context data is properly formatted

3. **"Category suggestion failed"**
   - Verify task data is provided
   - Check if existing categories are accessible

### Debug Mode
Enable debug logging by setting:
```python
import logging
logging.getLogger('ai_service').setLevel(logging.DEBUG)
```

## 📞 Support

For issues with AI integration:
1. Check the troubleshooting section above
2. Run the test script: `python test_ai_services.py`
3. Check the Django logs for detailed error messages
4. Verify your Gemini API key and quota

---

**Note**: This AI integration requires a valid Google Gemini API key and internet connectivity to function properly. 