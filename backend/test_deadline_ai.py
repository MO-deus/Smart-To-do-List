#!/usr/bin/env python3
"""
Test script to debug deadline suggestions from AI
"""

import asyncio
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from ai_service.gemini_client import GeminiAIService
from ai_service.context_analyzer import ContextAnalyzer

async def test_deadline_suggestions():
    """Test deadline suggestions with sample context"""
    
    # Initialize AI service
    gemini_client = GeminiAIService()
    context_analyzer = ContextAnalyzer(gemini_client)
    
    # Test context with explicit time references
    test_context = {
        'content': 'I need to finish the project report by next Friday. Also, the client meeting is in 2 weeks. And I have to submit the proposal tomorrow.',
        'source': 'manual_input',
        'timestamp': '2024-12-18T10:00:00Z'
    }
    
    print("Testing deadline suggestions...")
    print(f"Context: {test_context['content']}")
    print("-" * 50)
    
    try:
        # Test direct AI call
        print("1. Testing direct AI deadline suggestions...")
        ai_result = await gemini_client.analyze_text(test_context['content'], 'deadline_suggestions')
        print(f"AI Result: {ai_result}")
        
        if 'error' in ai_result:
            print(f"AI Error: {ai_result['error']}")
            return
        
        suggested_deadlines = ai_result.get('suggested_deadlines', [])
        print(f"Suggested Deadlines: {suggested_deadlines}")
        
        # Test through context analyzer
        print("\n2. Testing through context analyzer...")
        analysis_result = await context_analyzer.analyze_context(test_context)
        print(f"Full Analysis Result: {analysis_result}")
        
        workload_analysis = analysis_result.get('workload_analysis', {})
        deadlines = workload_analysis.get('suggested_deadlines', [])
        print(f"Context Analyzer Deadlines: {deadlines}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_deadline_suggestions()) 