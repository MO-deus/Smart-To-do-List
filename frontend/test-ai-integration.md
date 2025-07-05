# AI Integration Testing Guide

## Overview
This guide provides sample data and test scenarios to verify the AI integration between the frontend and backend of the Smart Todo List application.

## Prerequisites
1. Backend server running on `http://127.0.0.1:8000`
2. Frontend server running on `http://localhost:3000`
3. Valid Gemini API key configured in backend `.env` file
4. AI services healthy (check the green indicator on the test page)

## Test Page Access
Navigate to: `http://localhost:3000/ai-test`

## Sample Data for Testing

### 1. Task Creation Test Data

#### Basic Tasks
```json
{
  "title": "Prepare quarterly report",
  "description": "Need to compile sales data and create presentation for Q3 review meeting"
}
```

```json
{
  "title": "Client meeting follow-up",
  "description": "Send proposal to ABC Corp and schedule follow-up call"
}
```

```json
{
  "title": "Update website content",
  "description": "Review and update product descriptions and pricing information"
}
```

#### Complex Tasks
```json
{
  "title": "Project milestone review",
  "description": "Conduct comprehensive review of Q4 project milestones, identify blockers, and update stakeholders on progress. Include risk assessment and resource allocation analysis."
}
```

```json
{
  "title": "Team training session",
  "description": "Organize training session for new team members on the updated development workflow and coding standards. Prepare materials and schedule follow-up sessions."
}
```

### 2. Context Analysis Test Data

#### Email Context
```
Subject: Weekly Team Update - Urgent Items

Hi team,

We have several urgent items that need attention this week:

1. The client presentation for TechCorp is scheduled for Thursday at 2 PM. Please ensure all slides are ready and the demo environment is working.

2. The quarterly sales report needs to be finalized by Friday. Marketing team needs the data by Wednesday to prepare their materials.

3. We have a new team member starting next Monday. Please prepare their onboarding materials and set up their development environment.

4. The website needs to be updated with the new product pricing before the end of the week.

5. Don't forget about the monthly team retrospective meeting on Friday at 3 PM.

Let me know if you have any questions or need help with any of these tasks.

Best regards,
Sarah
```

#### Meeting Notes
```
Project Status Meeting - January 15, 2024

Attendees: John, Maria, Alex, Lisa

Key Points:
- Project deadline moved to Friday due to client request
- Need to finish backend API integration by Wednesday
- Documentation needs to be updated with latest API changes
- Team sync meeting scheduled for Wednesday at 10 AM
- Code review process needs to be completed by Thursday
- Testing phase should start on Thursday
- Deployment planning for Friday

Action Items:
- John: Complete API integration
- Maria: Update documentation
- Alex: Prepare testing environment
- Lisa: Schedule deployment review

Next meeting: Wednesday at 10 AM
```

#### Slack/Message Context
```
[10:30 AM] John: Hey team, just got an email from the client. They want to move the project deadline to this Friday instead of next week.

[10:32 AM] Maria: That's going to be tight. We still need to finish the API integration and testing.

[10:35 AM] Alex: I can help with the testing. What's the current status of the API?

[10:40 AM] John: API is about 80% done. Need to finish the authentication endpoints and error handling.

[10:45 AM] Lisa: I'll update the project timeline and notify stakeholders. Also, we need to prepare the demo for the client meeting on Thursday.

[10:50 AM] Maria: I'll prioritize the documentation updates. We need to make sure everything is ready for the handover.

[10:55 AM] Alex: Should we schedule a quick sync meeting tomorrow to review progress?

[11:00 AM] John: Good idea. Let's meet at 2 PM tomorrow to go through everything.
```

### 3. Edge Cases and Error Testing

#### Empty or Minimal Input
```json
{
  "title": "",
  "description": ""
}
```

#### Very Long Input
```json
{
  "title": "This is a very long task title that exceeds normal length expectations and should test how the AI handles extremely long inputs in the task creation process",
  "description": "This is an extremely detailed description that goes on and on with lots of information about what needs to be done, including multiple steps, considerations, requirements, dependencies, and additional context that might be relevant for understanding the full scope of work required to complete this task successfully."
}
```

#### Special Characters and Formatting
```json
{
  "title": "Task with special chars: @#$%^&*()",
  "description": "Description with line breaks\nand special formatting\n- bullet points\n- numbered lists\n1. First item\n2. Second item"
}
```

## Test Scenarios

### Scenario 1: Basic AI Task Creation
1. Navigate to the AI test page
2. Click "Create AI Task"
3. Enter a basic task title (e.g., "Prepare quarterly report")
4. Click "Get Suggestions"
5. Verify AI provides category and description suggestions
6. Apply suggestions and create the task
7. Verify task is created successfully

### Scenario 2: Context Analysis
1. Copy one of the email context samples above
2. Paste into the context analyzer
3. Click "Analyze Context"
4. Verify tasks are extracted correctly
5. Check that insights and suggested actions are provided
6. Verify urgency assessment is reasonable

### Scenario 3: AI Health Monitoring
1. Check the AI health indicator at the top of the page
2. If red, verify backend is running and API key is configured
3. If yellow, wait for health check to complete
4. If green, proceed with testing

### Scenario 4: Error Handling
1. Test with empty inputs
2. Test with very long inputs
3. Test with special characters
4. Verify appropriate error messages are displayed
5. Verify graceful fallback to non-AI mode when AI is unavailable

### Scenario 5: Category Suggestions
1. Create tasks with different types of content
2. Verify AI suggests appropriate categories
3. Test with existing categories vs. new categories
4. Verify category creation works correctly

### Scenario 6: Description Enhancement
1. Enter a basic task description
2. Use AI enhancement feature
3. Verify enhanced description is more detailed and actionable
4. Test with different types of tasks (technical, business, personal)

## Expected Behaviors

### AI Task Creation
- ✅ AI health check shows green indicator
- ✅ "Get Suggestions" button is enabled when title is entered
- ✅ AI provides relevant category suggestions
- ✅ AI enhances task descriptions
- ✅ Suggestions can be applied to form fields
- ✅ Task creation works with AI enhancements
- ✅ Fallback to regular creation when AI is disabled

### Context Analysis
- ✅ Extracts tasks from various context types
- ✅ Provides key insights and suggested actions
- ✅ Assesses urgency level appropriately
- ✅ Handles different input formats gracefully
- ✅ Displays results in organized sections

### Error Handling
- ✅ Graceful handling of API errors
- ✅ Clear error messages for users
- ✅ Fallback mechanisms when AI is unavailable
- ✅ Input validation and sanitization

## Troubleshooting

### Common Issues

1. **AI Health Check Fails**
   - Verify backend server is running
   - Check Gemini API key in `.env` file
   - Ensure all AI service dependencies are installed

2. **Suggestions Not Working**
   - Check browser console for errors
   - Verify API endpoints are accessible
   - Check network connectivity

3. **Context Analysis Fails**
   - Ensure context data is properly formatted
   - Check for special characters that might cause issues
   - Verify AI service is responding

4. **Task Creation Fails**
   - Check required fields are filled
   - Verify category exists or can be created
   - Check backend logs for errors

### Debug Information
- Check browser developer tools console for errors
- Check backend Django logs for API errors
- Verify API endpoints are responding correctly
- Test individual AI services using the backend test scripts

## Performance Testing

### Load Testing
- Test with multiple concurrent users
- Test with large amounts of context data
- Verify response times are reasonable
- Check memory usage during heavy usage

### Stress Testing
- Test with very long inputs
- Test with rapid successive requests
- Verify system stability under load
- Check error handling under stress

## Success Criteria

✅ All AI features work correctly with sample data
✅ Error handling is graceful and informative
✅ Performance is acceptable for typical usage
✅ UI is responsive and user-friendly
✅ AI suggestions are relevant and helpful
✅ Context analysis extracts meaningful information
✅ Task creation works with and without AI enhancements 