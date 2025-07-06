"""Consolidated AI Service for reducing API calls while maintaining functionality."""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from .gemini_client import GeminiAIService

logger = logging.getLogger(__name__)


class ConsolidatedAIService:
    """Consolidated AI service that reduces API calls by combining multiple analyses."""
    
    def __init__(self, gemini_client: GeminiAIService):
        self.gemini = gemini_client
    
    async def comprehensive_task_analysis(self, task: Dict[str, Any], context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Single comprehensive AI call that handles task enhancement, category suggestion, 
        priority scoring, and deadline suggestion in one request.
        """
        try:
            # Prepare comprehensive prompt
            task_title = task.get('title', '')
            task_description = task.get('description', '')
            
            # Process context data
            context_text = ""
            if context_data:
                if isinstance(context_data, dict):
                    context_text = context_data.get('content', '')
                else:
                    context_text = str(context_data)
            
            prompt = f"""
            Perform comprehensive analysis of this task and provide all recommendations in a single response:
            
            TASK:
            Title: {task_title}
            Description: {task_description}
            
            CONTEXT: {context_text}
            
            TODAY'S DATE: {datetime.now().strftime('%Y-%m-%d')}
            
            REQUIREMENTS:
            1. ENHANCE TASK: Create a COMPREHENSIVE and DETAILED description (minimum 200-300 words) with:
               - Technical specifications and requirements
               - Step-by-step actionable steps with specific details
               - Clear deliverables and expected outcomes
               - Success criteria and quality standards
               - Dependencies and prerequisites
               - Timeline estimates and milestones
               - Risk factors and mitigation strategies
               - Resource requirements and tools needed
            
            2. SUGGEST CATEGORY: Recommend appropriate category with confidence score
            
            3. SCORE PRIORITY: Determine priority level (high/medium/low) with score (1-100) and reasoning
            
            4. SUGGEST DEADLINE: Provide 2-3 deadline suggestions in ISO format (YYYY-MM-DD) with reasons
            
            CRITICAL: The enhanced description must be DETAILED, COMPREHENSIVE, and ACTIONABLE with specific technical details, not generic statements.
            
            Return as JSON:
            {{
                "task_enhancement": {{
                    "enhanced_title": "Improved, specific title with action verb",
                    "enhanced_description": "COMPREHENSIVE description (200-300 words) with detailed technical specifications, step-by-step implementation guide, specific deliverables, success criteria, dependencies, timeline estimates, risk assessment, and resource requirements. Include specific technologies, frameworks, tools, and methodologies. Provide concrete examples and measurable outcomes.",
                    "actionable_steps": [
                        "Step 1: Detailed description with specific actions, tools, and expected outcomes",
                        "Step 2: Technical implementation details with code examples or process descriptions",
                        "Step 3: Quality assurance and testing procedures with specific criteria",
                        "Step 4: Deployment and delivery process with timeline",
                        "Step 5: Documentation and handover requirements"
                    ],
                    "technical_requirements": "Detailed list of specific technologies, frameworks, libraries, tools, and platforms required for implementation",
                    "deliverables": "Specific outputs, documents, code, reports, or artifacts that will be produced",
                    "success_criteria": "Measurable and specific criteria for determining successful completion",
                    "confidence_score": 0.85
                }},
                "category_suggestion": {{
                    "primary_suggestion": {{
                        "name": "Category Name",
                        "reason": "Why this category fits",
                        "confidence": 0.9
                    }},
                    "alternative_categories": [
                        {{"name": "Alt Category 1", "confidence": 0.7}},
                        {{"name": "Alt Category 2", "confidence": 0.6}}
                    ]
                }},
                "priority_analysis": {{
                    "priority_score": 75,
                    "priority_level": "high",
                    "reasoning": "Why this priority level",
                    "urgency_factors": ["Factor 1", "Factor 2"],
                    "impact_assessment": "Potential impact description"
                }},
                "deadline_suggestions": [
                    {{
                        "date": "{(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}",
                        "reason": "Based on task complexity and urgency",
                        "urgency": "high",
                        "confidence": 0.8
                    }},
                    {{
                        "date": "{(datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')}",
                        "reason": "Conservative estimate with buffer time",
                        "urgency": "medium",
                        "confidence": 0.7
                    }}
                ],
                "overall_analysis": {{
                    "summary": "Brief summary of key insights and recommendations",
                    "risk_factors": ["Risk 1", "Risk 2"],
                    "recommendations": "General recommendations for task management"
                }}
            }}
            """
            
            result = await self.gemini.generate_structured_response(prompt)
            
            if 'error' in result:
                logger.error(f"Comprehensive analysis failed: {result['error']}")
                return self._generate_fallback_analysis(task, context_text)
            
            return result
            
        except Exception as e:
            logger.error(f"Comprehensive task analysis failed: {str(e)}")
            return self._generate_fallback_analysis(task, context_text)
    
    async def context_analysis(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Single AI call for comprehensive context analysis including task extraction, 
        priority patterns, workload analysis, and category suggestions.
        """
        try:
            # Process context data
            if isinstance(context_data, dict):
                context_text = context_data.get('content', '')
            else:
                context_text = str(context_data)
            
            if not context_text.strip():
                return self._generate_empty_context_analysis()
            
            prompt = f"""
            Analyze this context comprehensively and extract all relevant information:
            
            CONTEXT: {context_text}
            
            TODAY'S DATE: {datetime.now().strftime('%Y-%m-%d')}
            
            REQUIREMENTS:
            1. EXTRACT TASKS: Identify all actionable tasks with detailed titles, comprehensive descriptions (100-200 words each), and priorities
            2. ANALYZE PRIORITY PATTERNS: Determine overall urgency level and priority distribution
            3. ASSESS WORKLOAD: Evaluate current workload level and temporal distribution
            4. SUGGEST CATEGORIES: Recommend categories for organizing extracted tasks
            5. GENERATE DEADLINE SUGGESTIONS: Suggest deadlines based on context time references
            
            CRITICAL: Each extracted task description must be DETAILED and COMPREHENSIVE with specific requirements, deliverables, and implementation details.
            
            Return as JSON:
            {{
                "extracted_tasks": [
                    {{
                        "title": "Task title with action verb",
                        "description": "COMPREHENSIVE description (100-200 words) with detailed requirements, specific deliverables, implementation approach, success criteria, and technical specifications. Include specific technologies, tools, or methodologies if mentioned in context.",
                        "priority": "high/medium/low",
                        "confidence": 0.8
                    }}
                ],
                "priority_analysis": {{
                    "urgency_level": "high/medium/low",
                    "priority_distribution": {{"high": 3, "medium": 2, "low": 1}},
                    "total_indicators": 6,
                    "insights": "Priority pattern analysis"
                }},
                "workload_analysis": {{
                    "workload_level": "high/medium/low",
                    "action_item_count": 5,
                    "temporal_distribution": {{"immediate": 2, "short_term": 2, "long_term": 1}},
                    "insights": "Workload assessment"
                }},
                "category_suggestions": [
                    {{
                        "name": "Category Name",
                        "reason": "Why this category is relevant",
                        "confidence": 0.9,
                        "relevance": "high"
                    }}
                ],
                "deadline_suggestions": [
                    {{
                        "date": "{(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}",
                        "reason": "Based on context time references",
                        "urgency": "high",
                        "confidence": 0.8
                    }}
                ],
                "context_summary": "Comprehensive summary of context analysis and key insights"
            }}
            """
            
            result = await self.gemini.generate_structured_response(prompt)
            
            if 'error' in result:
                logger.error(f"Context analysis failed: {result['error']}")
                return self._generate_fallback_context_analysis(context_text)
            
            return result
            
        except Exception as e:
            logger.error(f"Context analysis failed: {str(e)}")
            return self._generate_fallback_context_analysis(context_text)
    
    async def health_check(self) -> bool:
        """Simple health check with minimal API call."""
        try:
            response = await self.gemini.generate_content("Health check", temperature=0.1)
            return bool(response and len(response.strip()) > 0)
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False
    
    def _generate_fallback_analysis(self, task: Dict[str, Any], context_text: str) -> Dict[str, Any]:
        """Generate fallback analysis when AI fails."""
        return {
            "task_enhancement": {
                "enhanced_title": task.get('title', ''),
                "enhanced_description": task.get('description', ''),
                "actionable_steps": [],
                "technical_requirements": "",
                "deliverables": "",
                "success_criteria": "",
                "confidence_score": 0.0
            },
            "category_suggestion": {
                "primary_suggestion": {"name": "General", "reason": "Fallback category", "confidence": 0.0},
                "alternative_categories": []
            },
            "priority_analysis": {
                "priority_score": 50,
                "priority_level": "medium",
                "reasoning": "Default priority level",
                "urgency_factors": [],
                "impact_assessment": ""
            },
            "deadline_suggestions": [
                {
                    "date": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                    "reason": "Default deadline suggestion",
                    "urgency": "medium",
                    "confidence": 0.0
                }
            ],
            "overall_analysis": {
                "summary": "Analysis failed, using fallback values",
                "risk_factors": [],
                "recommendations": ""
            }
        }
    
    def _generate_empty_context_analysis(self) -> Dict[str, Any]:
        """Generate empty context analysis when no context is provided."""
        return {
            "extracted_tasks": [],
            "priority_analysis": {
                "urgency_level": "normal",
                "priority_distribution": {},
                "total_indicators": 0,
                "insights": "No context provided"
            },
            "workload_analysis": {
                "workload_level": "normal",
                "action_item_count": 0,
                "temporal_distribution": {},
                "insights": "No context provided"
            },
            "category_suggestions": [],
            "deadline_suggestions": [],
            "context_summary": "No context data provided"
        }
    
    def _generate_fallback_context_analysis(self, context_text: str) -> Dict[str, Any]:
        """Generate fallback context analysis when AI fails."""
        return {
            "extracted_tasks": [],
            "priority_analysis": {
                "urgency_level": "normal",
                "priority_distribution": {},
                "total_indicators": 0,
                "insights": "Context analysis failed"
            },
            "workload_analysis": {
                "workload_level": "normal",
                "action_item_count": 0,
                "temporal_distribution": {},
                "insights": "Context analysis failed"
            },
            "category_suggestions": [],
            "deadline_suggestions": [],
            "context_summary": f"Context analysis failed for: {context_text[:100]}..."
        } 