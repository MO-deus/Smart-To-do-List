import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from django.conf import settings

# Load environment variables from .env file
# Find the project root (two levels up from this file)
project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / '.env')

logger = logging.getLogger(__name__)

class GeminiAIService:
    """
    Wrapper for Google Gemini AI API
    Handles authentication, API calls, and response processing
    """
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash"
        self.max_retries = 3
        
    async def generate_content(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generate content using Gemini AI
        
        Args:
            prompt: The input prompt for the AI
            temperature: Controls randomness (0.0 = deterministic, 1.0 = creative)
            
        Returns:
            Generated text response
        """
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            if response.text:
                return response.text
            else:
                logger.warning("Empty response from Gemini API")
                return ""
                
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            raise
    
    async def generate_structured_response(self, prompt: str, expected_format: str = "JSON") -> Dict[str, Any]:
        """
        Generate structured response (JSON) from Gemini AI
        
        Args:
            prompt: The input prompt
            expected_format: Expected response format (default: JSON)
            
        Returns:
            Parsed JSON response as dictionary
        """
        try:
            # Add format instruction to prompt
            formatted_prompt = f"{prompt}\n\nPlease respond in valid {expected_format} format."
            
            response_text = await self.generate_content(formatted_prompt, temperature=0.3)
            
            # Try to extract JSON from response
            try:
                # Look for JSON in the response
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx != -1 and end_idx != 0:
                    json_str = response_text[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    logger.warning("No JSON found in response")
                    return {"error": "No structured data found", "raw_response": response_text}
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {str(e)}")
                return {"error": "Invalid JSON response", "raw_response": response_text}
                
        except Exception as e:
            logger.error(f"Error generating structured response: {str(e)}")
            return {"error": str(e)}
    
    async def analyze_text(self, text: str, analysis_type: str) -> Dict[str, Any]:
        """
        Analyze text for specific purposes
        
        Args:
            text: Text to analyze
            analysis_type: Type of analysis (e.g., 'sentiment', 'extract_tasks', 'categorize')
            
        Returns:
            Analysis results
        """
        analysis_prompts = {
            'extract_tasks': f"""
            Analyze the following text and extract actionable tasks:
            
            Text: {text}
            
            Please identify and extract:
            1. Explicit tasks mentioned
            2. Implicit tasks that can be inferred
            3. Priority indicators (urgent, important, etc.)
            4. Deadlines or time constraints
            5. Dependencies between tasks
            
            IMPORTANT REQUIREMENTS:
            - For each task, provide a clear, specific, and fitting title to the context provided (max 60 characters)
            - Write concise, actionable descriptions (max 200 characters)
            - Avoid generic titles like "Task from Context Analysis"
            - Focus on what needs to be done, not what was analyzed
            
            Return as JSON:
            {{
                "extracted_tasks": [
                    {{
                        "title": "Concise, actionable task title",
                        "description": "Brief, specific description of what needs to be done",
                        "priority": "high/medium/low",
                        "deadline": "YYYY-MM-DD or null",
                        "category": "suggested_category",
                        "confidence": 0.85
                    }}
                ],
                "context_insights": "Key insights about schedule and priorities",
                "workload_analysis": "Analysis of current workload"
            }}
            """,
            
            'context_summary': f"""
            Analyze the following context and create a meaningful, human-readable summary:
            
            Context: {text}
            
            Please create a summary that:
            1. Captures the main themes and topics discussed
            2. Identifies key action items and priorities
            3. Highlights important deadlines or time constraints
            4. Provides insights about the overall context
            5. Is written in natural, conversational language
            
            Avoid generic phrases like "Analyzed content from X sources" or "Detected Y potential action items".
            Instead, focus on the actual content and what it means for the user.
            
            Return as JSON:
            {{
                "summary": "A meaningful, human-readable summary of the context",
                "key_themes": ["theme1", "theme2"],
                "action_items": ["item1", "item2"],
                "insights": "Key insights about the context"
            }}
            """,
            
            'priority_analysis': f"""
            Analyze the following context for priority indicators and urgency levels:
            
            Context: {text}
            
            Please identify:
            1. Priority indicators (urgent, important, critical, etc.)
            2. Urgency levels and time sensitivity
            3. Priority distribution across different types
            4. Overall urgency assessment
            
            Return as JSON:
            {{
                "priority_distribution": {{
                    "urgent": 2,
                    "important": 3,
                    "normal": 1
                }},
                "urgency_level": "high/medium/low",
                "total_indicators": 6,
                "insights": "Analysis of priority patterns and urgency"
            }}
            """,
            
            'workload_analysis': f"""
            Analyze the following context for workload assessment:
            
            Context: {text}
            
            Please identify:
            1. Number of action items and tasks
            2. Workload complexity and distribution
            3. Temporal patterns and deadlines
            4. Overall workload assessment
            
            Return as JSON:
            {{
                "action_item_count": 5,
                "temporal_distribution": {{
                    "immediate": 2,
                    "short_term": 1,
                    "medium_term": 2
                }},
                "workload_level": "high/medium/low",
                "insights": "Analysis of current workload and task distribution"
            }}
            """,
            
            'deadline_suggestions': f"""
            Analyze the following context and suggest appropriate deadlines in ISO format (YYYY-MM-DD):
            
            Context: {text}
            
            CRITICAL REQUIREMENTS:
            1. You MUST provide at least 3 deadline suggestions in ISO format (YYYY-MM-DD)
            2. Use TODAY'S DATE as the reference point for all calculations
            3. All suggested dates must be in the future (not today or in the past)
            4. Calculate actual dates based on time references in the context
            
            """,
            
            'categorize': f"""
            Categorize the following task:
            
            Task: {text}
            
            Please suggest:
            1. Primary category
            2. Subcategories
            3. Relevant tags
            4. Priority level
            5. Complexity score (1-10)
            
            Return as JSON:
            {{
                "primary_category": "category_name",
                "subcategories": ["sub1", "sub2"],
                "tags": ["tag1", "tag2"],
                "priority": "high/medium/low",
                "complexity_score": 7,
                "confidence": 0.85
            }}
            """,
            
            'enhance_description': f"""
            Enhance the following task description with more details and context:
            
            Task: {text}
            
            Please enhance by:
            1. Adding specific actionable steps
            2. Including relevant context
            3. Improving clarity and completeness
            4. Adding helpful details
            
            Return as JSON:
            {{
                "enhanced_description": "Enhanced task description",
                "actionable_steps": ["step1", "step2"],
                "context_details": "Relevant context information",
                "improvements_made": ["improvement1", "improvement2"]
            }}
            """,
            
            'category_suggestions': f"""
            Analyze the following context and suggest appropriate categories for task organization:
            
            Context: {text}
            
            CRITICAL REQUIREMENTS:
            1. You MUST provide at least 5 category suggestions
            2. Categories should be relevant to the context content
            3. Include both specific and general categories
            4. Consider different aspects of the content (work, personal, health, etc.)
            5. Categories should be concise (1-3 words) and actionable
            
            Please suggest categories based on:
            1. The main themes and topics in the context
            2. The type of tasks or activities mentioned
            3. The domain or field of work
            4. The urgency and priority levels
            5. The temporal aspects (deadlines, schedules)
            
            Consider various category types:
            - Work/Professional: Project, Meeting, Report, Client, etc.
            - Personal: Home, Family, Health, Finance, etc.
            - Learning: Study, Research, Training, etc.
            - Creative: Design, Writing, Art, etc.
            - Administrative: Planning, Organization, etc.
            
            Return as JSON:
            {{
                "suggested_categories": [
                    {{
                        "name": "Project Management",
                        "reason": "Based on project-related tasks and deadlines",
                        "confidence": 0.9,
                        "relevance": "high"
                    }},
                    {{
                        "name": "Client Relations",
                        "reason": "Based on client meeting and communication needs",
                        "confidence": 0.8,
                        "relevance": "medium"
                    }},
                    {{
                        "name": "Documentation",
                        "reason": "Based on report and proposal requirements",
                        "confidence": 0.7,
                        "relevance": "medium"
                    }},
                    {{
                        "name": "Planning",
                        "reason": "Based on scheduling and deadline management",
                        "confidence": 0.6,
                        "relevance": "low"
                    }},
                    {{
                        "name": "Communication",
                        "reason": "Based on meeting and presentation needs",
                        "confidence": 0.5,
                        "relevance": "low"
                    }}
                ],
                "context_analysis": "Analysis of context themes and category relevance",
                "recommendations": "General category organization recommendations"
            }}
            """
        }
        
        if analysis_type not in analysis_prompts:
            raise ValueError(f"Unknown analysis type: {analysis_type}")
        
        prompt = analysis_prompts[analysis_type]
        return await self.generate_structured_response(prompt)
    
    async def health_check(self) -> bool:
        """
        Check if Gemini API is working properly
        
        Returns:
            True if API is working, False otherwise
        """
        try:
            response = await self.generate_content("Hello, this is a health check.")
            return bool(response and len(response.strip()) > 0)
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False 