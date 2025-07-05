import logging
from typing import Dict, Any, List
from datetime import datetime
from .gemini_client import GeminiAIService

logger = logging.getLogger(__name__)

class PriorityScorer:
    """
    AI-powered task priority scoring system
    Analyzes tasks based on urgency, importance, context, and workload
    """
    
    def __init__(self, gemini_client: GeminiAIService):
        self.gemini = gemini_client
        self.scoring_factors = {
            'urgency': 0.3,
            'importance': 0.25,
            'context_relevance': 0.2,
            'workload_impact': 0.15,
            'dependency_factor': 0.1
        }
    
    async def calculate_priority_score(self, task: Dict[str, Any], context: Dict[str, Any], workload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive priority score using AI
        
        Args:
            task: Task data including title, description, category
            context: Context analysis results
            workload: Current workload analysis
            
        Returns:
            Priority analysis with score and reasoning
        """
        try:
            # Step 1: Analyze task characteristics
            task_analysis = await self.analyze_task_characteristics(task)
            
            # Step 2: Evaluate urgency factors
            urgency_score = await self.evaluate_urgency(task, context)
            
            # Step 3: Assess importance
            importance_score = await self.evaluate_importance(task, context)
            
            # Step 4: Check context relevance
            context_relevance = await self.evaluate_context_relevance(task, context)
            
            # Step 5: Analyze workload impact
            workload_impact = await self.evaluate_workload_impact(task, workload)
            
            # Step 6: Check dependencies
            dependency_factor = await self.evaluate_dependencies(task, context)
            
            # Step 7: Calculate weighted score
            final_score = self.calculate_weighted_score({
                'urgency': urgency_score,
                'importance': importance_score,
                'context_relevance': context_relevance,
                'workload_impact': workload_impact,
                'dependency_factor': dependency_factor
            })
            
            # Step 8: Generate reasoning
            reasoning = await self.generate_priority_reasoning(task, final_score, {
                'urgency': urgency_score,
                'importance': importance_score,
                'context_relevance': context_relevance,
                'workload_impact': workload_impact,
                'dependency_factor': dependency_factor
            })
            
            return {
                'priority_score': final_score,
                'score_breakdown': {
                    'urgency': urgency_score,
                    'importance': importance_score,
                    'context_relevance': context_relevance,
                    'workload_impact': workload_impact,
                    'dependency_factor': dependency_factor
                },
                'reasoning': reasoning,
                'priority_level': self.get_priority_level(final_score),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Priority scoring failed: {str(e)}")
            return {
                'priority_score': 50,  # Default medium priority
                'score_breakdown': {},
                'reasoning': f"Priority scoring failed: {str(e)}",
                'priority_level': 'medium',
                'error': str(e)
            }
    
    async def analyze_task_characteristics(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze task characteristics using AI
        """
        try:
            task_text = f"Title: {task.get('title', '')}\nDescription: {task.get('description', '')}\nCategory: {task.get('category', 'Unknown')}"
            
            prompt = f"""
            Analyze the characteristics of this task:
            
            {task_text}
            
            Please identify:
            1. Task complexity (1-10 scale)
            2. Time requirements (estimated hours)
            3. Skill level needed (beginner/intermediate/expert)
            4. Resource requirements
            5. Potential impact
            
            Return as JSON:
            {{
                "complexity": 7,
                "time_estimate": 4,
                "skill_level": "intermediate",
                "resource_requirements": ["software", "data"],
                "potential_impact": "high/medium/low",
                "characteristics": ["technical", "collaborative", "time-sensitive"]
            }}
            """
            
            result = await self.gemini.generate_structured_response(prompt)
            return result if 'error' not in result else {}
            
        except Exception as e:
            logger.error(f"Task characteristic analysis failed: {str(e)}")
            return {}
    
    async def evaluate_urgency(self, task: Dict[str, Any], context: Dict[str, Any]) -> float:
        """
        AI-powered urgency evaluation
        """
        try:
            context_summary = context.get('context_summary', '')
            priority_insights = context.get('priority_insights', {})
            
            prompt = f"""
            Evaluate the urgency of this task based on the context:
            
            Task: {task.get('title', '')}
            Description: {task.get('description', '')}
            Current Context: {context_summary}
            Priority Insights: {priority_insights}
            
            Consider:
            - Time-sensitive elements
            - External deadlines
            - Dependencies on other tasks
            - Impact of delay
            - Context urgency indicators
            
            Return a score from 0-100 and brief reasoning.
            Format: {{"score": 75, "reasoning": "High urgency due to..."}}
            """
            
            result = await self.gemini.generate_structured_response(prompt)
            
            if 'error' not in result and 'score' in result:
                return min(100, max(0, float(result['score'])))
            else:
                return 50.0  # Default medium urgency
                
        except Exception as e:
            logger.error(f"Urgency evaluation failed: {str(e)}")
            return 50.0
    
    async def evaluate_importance(self, task: Dict[str, Any], context: Dict[str, Any]) -> float:
        """
        AI-powered importance evaluation
        """
        try:
            context_summary = context.get('context_summary', '')
            
            prompt = f"""
            Evaluate the importance of this task:
            
            Task: {task.get('title', '')}
            Description: {task.get('description', '')}
            Category: {task.get('category', 'Unknown')}
            Context: {context_summary}
            
            Consider:
            - Strategic value
            - Impact on goals
            - Stakeholder importance
            - Long-term consequences
            - Business value
            
            Return a score from 0-100 and brief reasoning.
            Format: {{"score": 80, "reasoning": "High importance because..."}}
            """
            
            result = await self.gemini.generate_structured_response(prompt)
            
            if 'error' not in result and 'score' in result:
                return min(100, max(0, float(result['score'])))
            else:
                return 50.0  # Default medium importance
                
        except Exception as e:
            logger.error(f"Importance evaluation failed: {str(e)}")
            return 50.0
    
    async def evaluate_context_relevance(self, task: Dict[str, Any], context: Dict[str, Any]) -> float:
        """
        Evaluate how relevant the task is to current context
        """
        try:
            context_summary = context.get('context_summary', '')
            extracted_tasks = context.get('extracted_tasks', [])
            
            # Check if task is related to extracted tasks
            task_title = task.get('title', '').lower()
            task_desc = task.get('description', '').lower()
            
            relevance_score = 50.0  # Base score
            
            # Check for keyword matches with extracted tasks
            for extracted_task in extracted_tasks:
                extracted_title = extracted_task.get('title', '').lower()
                extracted_desc = extracted_task.get('description', '').lower()
                
                # Simple keyword matching
                common_words = set(task_title.split()) & set(extracted_title.split())
                if len(common_words) > 0:
                    relevance_score += 20
                
                # Check description similarity
                if any(word in task_desc for word in extracted_desc.split()):
                    relevance_score += 15
            
            # Cap the score
            return min(100, relevance_score)
            
        except Exception as e:
            logger.error(f"Context relevance evaluation failed: {str(e)}")
            return 50.0
    
    async def evaluate_workload_impact(self, task: Dict[str, Any], workload: Dict[str, Any]) -> float:
        """
        Evaluate how the task impacts current workload
        """
        try:
            workload_level = workload.get('workload_level', 'normal')
            action_item_count = workload.get('action_item_count', 0)
            
            # Base score - higher workload means lower impact score
            if workload_level == 'high':
                base_score = 30.0
            elif workload_level == 'medium':
                base_score = 50.0
            else:
                base_score = 70.0
            
            # Adjust based on action item count
            if action_item_count > 10:
                base_score -= 20
            elif action_item_count > 5:
                base_score -= 10
            
            return max(0, base_score)
            
        except Exception as e:
            logger.error(f"Workload impact evaluation failed: {str(e)}")
            return 50.0
    
    async def evaluate_dependencies(self, task: Dict[str, Any], context: Dict[str, Any]) -> float:
        """
        Evaluate task dependencies
        """
        try:
            task_desc = task.get('description', '').lower()
            
            # Check for dependency indicators
            dependency_keywords = ['after', 'depends on', 'waiting for', 'blocked by', 'requires']
            
            dependency_score = 50.0  # Base score
            
            for keyword in dependency_keywords:
                if keyword in task_desc:
                    dependency_score += 20  # Higher score for dependent tasks
            
            return min(100, dependency_score)
            
        except Exception as e:
            logger.error(f"Dependency evaluation failed: {str(e)}")
            return 50.0
    
    def calculate_weighted_score(self, scores: Dict[str, float]) -> float:
        """
        Calculate weighted priority score
        """
        try:
            weighted_sum = 0
            total_weight = 0
            
            for factor, weight in self.scoring_factors.items():
                if factor in scores:
                    weighted_sum += scores[factor] * weight
                    total_weight += weight
            
            if total_weight > 0:
                return weighted_sum / total_weight
            else:
                return 50.0
                
        except Exception as e:
            logger.error(f"Weighted score calculation failed: {str(e)}")
            return 50.0
    
    def get_priority_level(self, score: float) -> str:
        """
        Convert numeric score to priority level
        """
        if score >= 80:
            return 'high'
        elif score >= 60:
            return 'medium-high'
        elif score >= 40:
            return 'medium'
        elif score >= 20:
            return 'low-medium'
        else:
            return 'low'
    
    async def generate_priority_reasoning(self, task: Dict[str, Any], final_score: float, breakdown: Dict[str, float]) -> str:
        """
        Generate human-readable reasoning for priority score
        """
        try:
            prompt = f"""
            Generate a brief explanation for this task's priority score:
            
            Task: {task.get('title', '')}
            Final Score: {final_score}/100
            Score Breakdown:
            - Urgency: {breakdown.get('urgency', 0)}/100
            - Importance: {breakdown.get('importance', 0)}/100
            - Context Relevance: {breakdown.get('context_relevance', 0)}/100
            - Workload Impact: {breakdown.get('workload_impact', 0)}/100
            - Dependencies: {breakdown.get('dependency_factor', 0)}/100
            
            Provide a 2-3 sentence explanation of why this task has this priority level.
            Focus on the most significant factors.
            """
            
            response = await self.gemini.generate_content(prompt, temperature=0.3)
            return response if response else f"Priority score: {final_score}/100"
            
        except Exception as e:
            logger.error(f"Priority reasoning generation failed: {str(e)}")
            return f"Priority score: {final_score}/100"
    
    async def batch_prioritize_tasks(self, tasks: List[Dict[str, Any]], context: Dict[str, Any], workload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Prioritize multiple tasks at once
        """
        try:
            prioritized_tasks = []
            
            for task in tasks:
                priority_result = await self.calculate_priority_score(task, context, workload)
                prioritized_tasks.append({
                    **task,
                    'ai_priority_score': priority_result['priority_score'],
                    'ai_priority_level': priority_result['priority_level'],
                    'ai_priority_reasoning': priority_result['reasoning']
                })
            
            # Sort by priority score (highest first)
            prioritized_tasks.sort(key=lambda x: x['ai_priority_score'], reverse=True)
            
            return prioritized_tasks
            
        except Exception as e:
            logger.error(f"Batch prioritization failed: {str(e)}")
            return tasks  # Return original tasks if prioritization fails 