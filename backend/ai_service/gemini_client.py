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
            
            Return as JSON:
            {{
                "extracted_tasks": [
                    {{
                        "title": "Task title",
                        "description": "Detailed description",
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