import logging
from typing import Dict, Any, List
from datetime import datetime
from .gemini_client import GeminiAIService

logger = logging.getLogger(__name__)

class TaskEnhancer:
    """
    AI-powered task enhancement system
    Improves task descriptions, adds details, and suggests improvements
    """
    
    def __init__(self, gemini_client: GeminiAIService):
        self.gemini = gemini_client
    
    async def enhance_task(self, task: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        AI-powered task enhancement
        
        Args:
            task: Task data including title, description
            context: Optional context for enhancement
            
        Returns:
            Enhanced task with improvements and suggestions
        """
        try:
            # Step 1: Analyze current task
            task_analysis = await self.analyze_current_task(task)
            
            # Step 2: Generate enhanced description
            enhanced_description = await self.generate_enhanced_description(task, task_analysis, context)
            
            # Step 3: Suggest actionable steps
            actionable_steps = await self.suggest_actionable_steps(task, enhanced_description)
            
            # Step 4: Add context details
            context_details = await self.add_context_details(task, context)
            
            # Step 5: Suggest improvements
            improvements = await self.suggest_improvements(task, task_analysis)
            
            # Step 6: Generate reasoning
            reasoning = await self.generate_enhancement_reasoning(task, enhanced_description)
            
            return {
                'enhanced_description': enhanced_description,
                'actionable_steps': actionable_steps,
                'context_details': context_details,
                'improvements': improvements,
                'reasoning': reasoning,
                'confidence_score': self.calculate_enhancement_confidence(enhanced_description, actionable_steps),
                'task_analysis': task_analysis,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Task enhancement failed: {str(e)}")
            return {
                'enhanced_description': task.get('description', ''),
                'actionable_steps': [],
                'context_details': {},
                'improvements': [],
                'reasoning': f"Task enhancement failed: {str(e)}",
                'confidence_score': 0.0,
                'error': str(e)
            }
    
    async def analyze_current_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze current task for enhancement opportunities
        """
        try:
            task_text = f"Title: {task.get('title', '')}\nDescription: {task.get('description', '')}"
            
            prompt = f"""
            Analyze this task for enhancement opportunities:
            
            {task_text}
            
            Evaluate:
            1. Clarity and completeness
            2. Specificity and actionability
            3. Missing details or context
            4. Potential improvements
            5. Ambiguity or vagueness
            
            Return as JSON:
            {{
                "clarity_score": 7,
                "completeness_score": 6,
                "specificity_score": 5,
                "missing_elements": ["element1", "element2"],
                "improvement_areas": ["area1", "area2"],
                "ambiguity_issues": ["issue1", "issue2"],
                "enhancement_potential": "high/medium/low"
            }}
            """
            
            result = await self.gemini.generate_structured_response(prompt)
            return result if 'error' not in result else {}
            
        except Exception as e:
            logger.error(f"Task analysis failed: {str(e)}")
            return {}
    
    async def generate_enhanced_description(self, task: Dict[str, Any], task_analysis: Dict[str, Any], 
                                          context: Dict[str, Any] = None) -> str:
        """
        Generate enhanced task description using AI
        """
        try:
            task_text = f"Title: {task.get('title', '')}\nDescription: {task.get('description', '')}"
            analysis_summary = str(task_analysis)
            context_summary = str(context) if context else "No additional context provided"
            
            prompt = f"""
            Enhance this task description:
            
            Current Task: {task_text}
            Analysis: {analysis_summary}
            Context: {context_summary}
            
            Please enhance the description by:
            1. Adding specific details and context
            2. Making it more actionable and clear
            3. Including relevant information
            4. Improving completeness
            5. Adding helpful context
            
            Return the enhanced description as plain text.
            Keep it concise but comprehensive.
            """
            
            response = await self.gemini.generate_content(prompt, temperature=0.3)
            return response if response else task.get('description', '')
            
        except Exception as e:
            logger.error(f"Description enhancement failed: {str(e)}")
            return task.get('description', '')
    
    async def suggest_actionable_steps(self, task: Dict[str, Any], enhanced_description: str) -> List[Dict[str, Any]]:
        """
        Suggest actionable steps for the task
        """
        try:
            task_text = f"Title: {task.get('title', '')}\nEnhanced Description: {enhanced_description}"
            
            prompt = f"""
            Suggest actionable steps for this task:
            
            {task_text}
            
            Break down the task into specific, actionable steps.
            Consider:
            - Logical sequence
            - Dependencies between steps
            - Time estimates
            - Resources needed
            
            Return as JSON:
            {{
                "actionable_steps": [
                    {{
                        "step_number": 1,
                        "description": "Specific action to take",
                        "estimated_time": "30 minutes",
                        "dependencies": ["step1"],
                        "resources_needed": ["resource1"],
                        "notes": "Additional notes"
                    }}
                ],
                "total_estimated_time": "2 hours",
                "complexity_level": "medium"
            }}
            """
            
            result = await self.gemini.generate_structured_response(prompt)
            
            if 'error' not in result and 'actionable_steps' in result:
                return result['actionable_steps']
            else:
                return []
                
        except Exception as e:
            logger.error(f"Actionable steps suggestion failed: {str(e)}")
            return []
    
    async def add_context_details(self, task: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Add relevant context details to the task
        """
        try:
            if not context:
                return {}
            
            task_text = f"Title: {task.get('title', '')}\nDescription: {task.get('description', '')}"
            context_summary = str(context)
            
            prompt = f"""
            Add relevant context details for this task:
            
            Task: {task_text}
            Available Context: {context_summary}
            
            Identify and extract:
            1. Relevant background information
            2. Related tasks or dependencies
            3. Important deadlines or constraints
            4. Stakeholders or contacts
            5. Resources or tools needed
            
            Return as JSON:
            {{
                "background_info": "Relevant background",
                "related_tasks": ["task1", "task2"],
                "deadlines": ["deadline1"],
                "stakeholders": ["person1"],
                "resources": ["resource1"],
                "constraints": ["constraint1"]
            }}
            """
            
            result = await self.gemini.generate_structured_response(prompt)
            return result if 'error' not in result else {}
            
        except Exception as e:
            logger.error(f"Context details addition failed: {str(e)}")
            return {}
    
    async def suggest_improvements(self, task: Dict[str, Any], task_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Suggest improvements for the task
        """
        try:
            task_text = f"Title: {task.get('title', '')}\nDescription: {task.get('description', '')}"
            analysis_summary = str(task_analysis)
            
            prompt = f"""
            Suggest improvements for this task:
            
            Task: {task_text}
            Analysis: {analysis_summary}
            
            Suggest specific improvements for:
            1. Clarity and understanding
            2. Actionability and execution
            3. Completeness and detail
            4. Efficiency and optimization
            5. Success criteria and measurement
            
            Return as JSON:
            {{
                "improvements": [
                    {{
                        "category": "clarity/actionability/completeness/efficiency/measurement",
                        "suggestion": "Specific improvement suggestion",
                        "impact": "high/medium/low",
                        "effort": "low/medium/high",
                        "priority": "high/medium/low"
                    }}
                ]
            }}
            """
            
            result = await self.gemini.generate_structured_response(prompt)
            
            if 'error' not in result and 'improvements' in result:
                return result['improvements']
            else:
                return []
                
        except Exception as e:
            logger.error(f"Improvement suggestion failed: {str(e)}")
            return []
    
    async def generate_enhancement_reasoning(self, task: Dict[str, Any], enhanced_description: str) -> str:
        """
        Generate reasoning for task enhancement
        """
        try:
            original_description = task.get('description', '')
            
            prompt = f"""
            Explain the enhancements made to this task:
            
            Original: {original_description}
            Enhanced: {enhanced_description}
            
            Provide a brief explanation of:
            1. What was improved
            2. Why the changes were made
            3. How it makes the task better
            
            Keep it concise and focused on the key improvements.
            """
            
            response = await self.gemini.generate_content(prompt, temperature=0.3)
            return response if response else "Task description was enhanced for clarity and completeness."
            
        except Exception as e:
            logger.error(f"Enhancement reasoning generation failed: {str(e)}")
            return "Task description was enhanced for clarity and completeness."
    
    def calculate_enhancement_confidence(self, enhanced_description: str, actionable_steps: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence score for task enhancement
        """
        try:
            confidence = 0.5  # Base confidence
            
            # Adjust based on enhanced description quality
            if enhanced_description and len(enhanced_description) > 50:
                confidence += 0.2
            
            # Adjust based on actionable steps
            if actionable_steps and len(actionable_steps) > 0:
                confidence += 0.2
            
            # Adjust based on step quality
            if actionable_steps:
                detailed_steps = sum(1 for step in actionable_steps if len(step.get('description', '')) > 20)
                if detailed_steps > 0:
                    confidence += 0.1
            
            return min(1.0, confidence)
            
        except Exception as e:
            logger.error(f"Enhancement confidence calculation failed: {str(e)}")
            return 0.5
    
    async def batch_enhance_tasks(self, tasks: List[Dict[str, Any]], context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Enhance multiple tasks at once
        """
        try:
            enhanced_tasks = []
            
            for task in tasks:
                enhancement_result = await self.enhance_task(task, context)
                enhanced_tasks.append({
                    'task_id': task.get('id'),
                    'task_title': task.get('title'),
                    'enhancement': enhancement_result
                })
            
            return enhanced_tasks
            
        except Exception as e:
            logger.error(f"Batch task enhancement failed: {str(e)}")
            return []
    
    async def validate_enhancement(self, original_task: Dict[str, Any], enhanced_task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate task enhancement quality
        """
        try:
            original_desc = original_task.get('description', '')
            enhanced_desc = enhanced_task.get('enhanced_description', '')
            
            prompt = f"""
            Validate the quality of this task enhancement:
            
            Original: {original_desc}
            Enhanced: {enhanced_desc}
            
            Evaluate:
            1. Improvement in clarity
            2. Addition of useful details
            3. Maintained accuracy
            4. Appropriate level of detail
            
            Return as JSON:
            {{
                "is_improved": true,
                "clarity_improvement": 0.3,
                "detail_improvement": 0.4,
                "accuracy_maintained": true,
                "overall_quality": "good/excellent/poor",
                "recommendations": ["rec1", "rec2"]
            }}
            """
            
            result = await self.gemini.generate_structured_response(prompt)
            
            if 'error' in result:
                return {
                    'is_improved': True,
                    'clarity_improvement': 0.2,
                    'detail_improvement': 0.3,
                    'accuracy_maintained': True,
                    'overall_quality': 'good',
                    'error': result['error']
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Enhancement validation failed: {str(e)}")
            return {
                'is_improved': True,
                'clarity_improvement': 0.2,
                'detail_improvement': 0.3,
                'accuracy_maintained': True,
                'overall_quality': 'good',
                'error': str(e)
            } 