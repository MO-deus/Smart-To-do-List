import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from .gemini_client import GeminiAIService

logger = logging.getLogger(__name__)

class DeadlineSuggester:
    """
    AI-powered deadline suggestion system
    Analyzes task complexity, workload, and context to suggest realistic deadlines
    """
    
    def __init__(self, gemini_client: GeminiAIService):
        self.gemini = gemini_client
    
    async def suggest_deadline(self, task: Dict[str, Any], context: Dict[str, Any], workload: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered deadline suggestion
        
        Args:
            task: Task data including title, description, category
            context: Context analysis results
            workload: Current workload analysis
            
        Returns:
            Deadline suggestions with reasoning
        """
        try:
            # Step 1: Analyze task complexity
            complexity_analysis = await self.analyze_task_complexity(task)
            
            # Step 2: Estimate time requirements
            time_requirements = await self.estimate_time_requirements(task, complexity_analysis)
            
            # Step 3: Check schedule availability
            schedule_analysis = await self.analyze_schedule_availability(context, workload)
            
            # Step 4: Consider dependencies
            dependency_analysis = await self.analyze_dependencies(task, context)
            
            # Step 5: Generate deadline suggestions
            deadline_suggestions = await self.generate_deadline_suggestions(
                task, time_requirements, schedule_analysis, dependency_analysis
            )
            
            # Step 6: Generate reasoning
            reasoning = await self.generate_deadline_reasoning(task, deadline_suggestions)
            
            return {
                'suggested_deadlines': deadline_suggestions,
                'reasoning': reasoning,
                'confidence_score': self.calculate_deadline_confidence(deadline_suggestions),
                'complexity_analysis': complexity_analysis,
                'time_requirements': time_requirements,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Deadline suggestion failed: {str(e)}")
            return {
                'suggested_deadlines': [],
                'reasoning': f"Deadline suggestion failed: {str(e)}",
                'confidence_score': 0.0,
                'error': str(e)
            }
    
    async def analyze_task_complexity(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze task complexity using AI
        """
        try:
            task_text = f"Title: {task.get('title', '')}\nDescription: {task.get('description', '')}\nCategory: {task.get('category', 'Unknown')}"
            
            prompt = f"""
            Analyze the complexity of this task:
            
            {task_text}
            
            Consider:
            - Number of subtasks required
            - Skill level needed
            - Research requirements
            - Coordination with others
            - Technical complexity
            - Resource requirements
            
            Return as JSON:
            {{
                "complexity_score": 7,
                "estimated_hours": 4,
                "subtasks_count": 3,
                "skill_level": "intermediate",
                "coordination_needed": true,
                "research_required": false,
                "technical_complexity": "medium",
                "confidence": 0.85
            }}
            """
            
            result = await self.gemini.generate_structured_response(prompt)
            return result if 'error' not in result else {}
            
        except Exception as e:
            logger.error(f"Task complexity analysis failed: {str(e)}")
            return {}
    
    async def estimate_time_requirements(self, task: Dict[str, Any], complexity_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estimate time requirements for the task
        """
        try:
            # Use complexity analysis if available
            if complexity_analysis and 'estimated_hours' in complexity_analysis:
                base_hours = complexity_analysis['estimated_hours']
            else:
                # Fallback estimation based on task characteristics
                base_hours = self.estimate_hours_from_task(task)
            
            # Adjust for complexity factors
            complexity_score = complexity_analysis.get('complexity_score', 5)
            coordination_needed = complexity_analysis.get('coordination_needed', False)
            research_required = complexity_analysis.get('research_required', False)
            
            # Apply multipliers
            total_hours = base_hours
            
            if coordination_needed:
                total_hours *= 1.5  # 50% more time for coordination
            
            if research_required:
                total_hours *= 1.3  # 30% more time for research
            
            # Adjust based on complexity score
            complexity_multiplier = 1 + (complexity_score - 5) * 0.1
            total_hours *= complexity_multiplier
            
            return {
                'base_hours': base_hours,
                'total_hours': round(total_hours, 1),
                'complexity_multiplier': complexity_multiplier,
                'coordination_factor': 1.5 if coordination_needed else 1.0,
                'research_factor': 1.3 if research_required else 1.0
            }
            
        except Exception as e:
            logger.error(f"Time requirement estimation failed: {str(e)}")
            return {'base_hours': 2, 'total_hours': 2}
    
    def estimate_hours_from_task(self, task: Dict[str, Any]) -> float:
        """
        Fallback method to estimate hours from task characteristics
        """
        title = task.get('title', '').lower()
        description = task.get('description', '').lower()
        category = task.get('category', '').lower()
        
        # Simple keyword-based estimation
        if any(word in title or word in description for word in ['quick', 'simple', 'basic']):
            return 1.0
        elif any(word in title or word in description for word in ['review', 'check', 'verify']):
            return 2.0
        elif any(word in title or word in description for word in ['create', 'build', 'develop']):
            return 4.0
        elif any(word in title or word in description for word in ['complex', 'detailed', 'comprehensive']):
            return 6.0
        else:
            return 3.0  # Default
    
    async def analyze_schedule_availability(self, context: Dict[str, Any], workload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze schedule availability and workload
        """
        try:
            workload_level = workload.get('workload_level', 'normal')
            action_item_count = workload.get('action_item_count', 0)
            
            # Calculate available capacity
            if workload_level == 'high':
                daily_capacity = 2  # hours per day
            elif workload_level == 'medium':
                daily_capacity = 4  # hours per day
            else:
                daily_capacity = 6  # hours per day
            
            # Adjust for existing tasks
            existing_task_load = min(action_item_count * 0.5, daily_capacity * 0.7)
            available_capacity = daily_capacity - existing_task_load
            
            return {
                'workload_level': workload_level,
                'daily_capacity': daily_capacity,
                'existing_task_load': existing_task_load,
                'available_capacity': max(0, available_capacity),
                'recommended_daily_work': min(available_capacity, 4)  # Cap at 4 hours per day
            }
            
        except Exception as e:
            logger.error(f"Schedule availability analysis failed: {str(e)}")
            return {
                'workload_level': 'normal',
                'daily_capacity': 4,
                'available_capacity': 3,
                'recommended_daily_work': 3
            }
    
    async def analyze_dependencies(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze task dependencies
        """
        try:
            task_desc = task.get('description', '').lower()
            task_title = task.get('title', '').lower()
            
            # Check for dependency indicators
            dependency_keywords = ['after', 'depends on', 'waiting for', 'blocked by', 'requires', 'following']
            
            dependencies = []
            for keyword in dependency_keywords:
                if keyword in task_desc or keyword in task_title:
                    dependencies.append({
                        'type': 'explicit',
                        'keyword': keyword,
                        'description': f"Task mentions '{keyword}' indicating dependencies"
                    })
            
            # Check for implicit dependencies in context
            extracted_tasks = context.get('extracted_tasks', [])
            for extracted_task in extracted_tasks:
                if self.tasks_are_related(task, extracted_task):
                    dependencies.append({
                        'type': 'implicit',
                        'related_task': extracted_task.get('title', ''),
                        'description': f"Related to extracted task: {extracted_task.get('title', '')}"
                    })
            
            return {
                'has_dependencies': len(dependencies) > 0,
                'dependency_count': len(dependencies),
                'dependencies': dependencies,
                'estimated_delay_days': len(dependencies) * 1  # 1 day per dependency
            }
            
        except Exception as e:
            logger.error(f"Dependency analysis failed: {str(e)}")
            return {
                'has_dependencies': False,
                'dependency_count': 0,
                'dependencies': [],
                'estimated_delay_days': 0
            }
    
    def tasks_are_related(self, task1: Dict[str, Any], task2: Dict[str, Any]) -> bool:
        """
        Check if two tasks are related
        """
        title1 = task1.get('title', '').lower()
        title2 = task2.get('title', '').lower()
        
        # Simple keyword matching
        words1 = set(title1.split())
        words2 = set(title2.split())
        
        common_words = words1 & words2
        return len(common_words) >= 2  # At least 2 common words
    
    async def generate_deadline_suggestions(self, task: Dict[str, Any], time_requirements: Dict[str, Any], 
                                          schedule_analysis: Dict[str, Any], dependency_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate deadline suggestions
        """
        try:
            total_hours = time_requirements.get('total_hours', 3)
            available_capacity = schedule_analysis.get('available_capacity', 3)
            dependency_delay = dependency_analysis.get('estimated_delay_days', 0)
            
            # Calculate working days needed
            if available_capacity > 0:
                working_days_needed = max(1, round(total_hours / available_capacity))
            else:
                working_days_needed = max(1, round(total_hours / 3))  # Fallback to 3 hours per day
            
            # Add buffer for dependencies
            total_days_needed = working_days_needed + dependency_delay
            
            # Generate suggestions
            suggestions = []
            
            # Conservative deadline (add 50% buffer)
            conservative_days = int(total_days_needed * 1.5)
            conservative_date = datetime.now() + timedelta(days=conservative_days)
            suggestions.append({
                'type': 'conservative',
                'deadline': conservative_date.isoformat(),
                'days_from_now': conservative_days,
                'reasoning': f"Conservative estimate with 50% buffer for {total_days_needed} working days"
            })
            
            # Realistic deadline
            realistic_days = total_days_needed
            realistic_date = datetime.now() + timedelta(days=realistic_days)
            suggestions.append({
                'type': 'realistic',
                'deadline': realistic_date.isoformat(),
                'days_from_now': realistic_days,
                'reasoning': f"Realistic estimate based on {total_hours} hours of work"
            })
            
            # Aggressive deadline (if possible)
            if total_days_needed > 1:
                aggressive_days = max(1, int(total_days_needed * 0.7))
                aggressive_date = datetime.now() + timedelta(days=aggressive_days)
                suggestions.append({
                    'type': 'aggressive',
                    'deadline': aggressive_date.isoformat(),
                    'days_from_now': aggressive_days,
                    'reasoning': f"Aggressive estimate with 30% reduction in timeline"
                })
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Deadline suggestion generation failed: {str(e)}")
            # Fallback suggestion
            fallback_date = datetime.now() + timedelta(days=3)
            return [{
                'type': 'fallback',
                'deadline': fallback_date.isoformat(),
                'days_from_now': 3,
                'reasoning': 'Fallback suggestion due to calculation error'
            }]
    
    async def generate_deadline_reasoning(self, task: Dict[str, Any], deadline_suggestions: List[Dict[str, Any]]) -> str:
        """
        Generate human-readable reasoning for deadline suggestions
        """
        try:
            if not deadline_suggestions:
                return "Unable to generate deadline suggestions."
            
            # Use the realistic suggestion as primary
            realistic_suggestion = next((s for s in deadline_suggestions if s['type'] == 'realistic'), deadline_suggestions[0])
            
            prompt = f"""
            Generate a brief explanation for this task's deadline suggestion:
            
            Task: {task.get('title', '')}
            Suggested Deadline: {realistic_suggestion['deadline']}
            Days from now: {realistic_suggestion['days_from_now']}
            Reasoning: {realistic_suggestion['reasoning']}
            
            Provide a 2-3 sentence explanation of why this deadline is suggested.
            Consider task complexity, workload, and dependencies.
            """
            
            response = await self.gemini.generate_content(prompt, temperature=0.3)
            return response if response else realistic_suggestion['reasoning']
            
        except Exception as e:
            logger.error(f"Deadline reasoning generation failed: {str(e)}")
            return "Deadline suggestion based on task analysis."
    
    def calculate_deadline_confidence(self, deadline_suggestions: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence score for deadline suggestions
        """
        try:
            if not deadline_suggestions:
                return 0.0
            
            # Base confidence
            confidence = 0.7
            
            # Adjust based on number of suggestions
            if len(deadline_suggestions) >= 3:
                confidence += 0.1
            
            # Adjust based on suggestion types
            has_realistic = any(s['type'] == 'realistic' for s in deadline_suggestions)
            if has_realistic:
                confidence += 0.1
            
            # Adjust based on reasoning quality
            has_reasoning = all('reasoning' in s for s in deadline_suggestions)
            if has_reasoning:
                confidence += 0.1
            
            return min(1.0, confidence)
            
        except Exception as e:
            logger.error(f"Confidence calculation failed: {str(e)}")
            return 0.5 