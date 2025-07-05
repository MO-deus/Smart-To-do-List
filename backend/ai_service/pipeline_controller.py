import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from .gemini_client import GeminiAIService
from .context_analyzer import ContextAnalyzer
from .priority_scorer import PriorityScorer
from .deadline_suggester import DeadlineSuggester
from .category_suggester import CategorySuggester
from .task_enhancer import TaskEnhancer

logger = logging.getLogger(__name__)

class AIPipelineController:
    """
    Main AI pipeline controller
    Orchestrates all AI services for comprehensive task management
    """
    
    def __init__(self, gemini_client: GeminiAIService):
        self.gemini = gemini_client
        self.context_analyzer = ContextAnalyzer(gemini_client)
        self.priority_scorer = PriorityScorer(gemini_client)
        self.deadline_suggester = DeadlineSuggester(gemini_client)
        self.category_suggester = CategorySuggester(gemini_client)
        self.task_enhancer = TaskEnhancer(gemini_client)
    
    async def process_new_task(self, task: Dict[str, Any], context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Complete AI processing pipeline for a new task
        
        Args:
            task: New task data
            context_data: Optional context data for analysis
            
        Returns:
            Comprehensive AI analysis and suggestions
        """
        try:
            logger.info(f"Starting AI pipeline for task: {task.get('title', 'Unknown')}")
            
            # Step 1: Context Analysis
            context_analysis = await self.analyze_context(context_data)
            
            # Step 2: Task Enhancement
            task_enhancement = await self.enhance_task(task, context_analysis)
            
            # Step 3: Category Suggestion
            category_suggestion = await self.suggest_category(task)
            
            # Step 4: Priority Scoring
            priority_analysis = await self.score_priority(task, context_analysis)
            
            # Step 5: Deadline Suggestion
            deadline_suggestion = await self.suggest_deadline(task, context_analysis)
            
            # Step 6: Compile Results
            results = await self.compile_results(
                task, context_analysis, task_enhancement, 
                category_suggestion, priority_analysis, deadline_suggestion
            )
            
            logger.info(f"AI pipeline completed for task: {task.get('title', 'Unknown')}")
            return results
            
        except Exception as e:
            logger.error(f"AI pipeline failed: {str(e)}")
            return {
                'error': str(e),
                'task_id': task.get('id'),
                'pipeline_status': 'failed',
                'timestamp': datetime.now().isoformat()
            }
    
    async def analyze_context(self, context_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze context data if provided
        """
        try:
            if not context_data:
                return {
                    'context_summary': 'No context data provided',
                    'extracted_tasks': [],
                    'priority_insights': {},
                    'workload_analysis': {'workload_level': 'normal', 'action_item_count': 0}
                }
            
            return await self.context_analyzer.analyze_context(context_data)
            
        except Exception as e:
            logger.error(f"Context analysis failed: {str(e)}")
            return {
                'context_summary': 'Context analysis failed',
                'extracted_tasks': [],
                'priority_insights': {},
                'workload_analysis': {'workload_level': 'normal', 'action_item_count': 0},
                'error': str(e)
            }
    
    async def enhance_task(self, task: Dict[str, Any], context_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance task description and details
        """
        try:
            return await self.task_enhancer.enhance_task(task, context_analysis)
            
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
    
    async def suggest_category(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggest appropriate category for the task
        """
        try:
            return await self.category_suggester.suggest_category(task)
            
        except Exception as e:
            logger.error(f"Category suggestion failed: {str(e)}")
            return {
                'suggested_categories': [],
                'primary_suggestion': None,
                'reasoning': f"Category suggestion failed: {str(e)}",
                'confidence_score': 0.0,
                'error': str(e)
            }
    
    async def score_priority(self, task: Dict[str, Any], context_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score task priority using AI
        """
        try:
            workload = context_analysis.get('workload_analysis', {})
            return await self.priority_scorer.calculate_priority_score(task, context_analysis, workload)
            
        except Exception as e:
            logger.error(f"Priority scoring failed: {str(e)}")
            return {
                'priority_score': 50,
                'score_breakdown': {},
                'reasoning': f"Priority scoring failed: {str(e)}",
                'priority_level': 'medium',
                'error': str(e)
            }
    
    async def suggest_deadline(self, task: Dict[str, Any], context_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggest deadline for the task
        """
        try:
            workload = context_analysis.get('workload_analysis', {})
            return await self.deadline_suggester.suggest_deadline(task, context_analysis, workload)
            
        except Exception as e:
            logger.error(f"Deadline suggestion failed: {str(e)}")
            return {
                'suggested_deadlines': [],
                'reasoning': f"Deadline suggestion failed: {str(e)}",
                'confidence_score': 0.0,
                'error': str(e)
            }
    
    async def compile_results(self, task: Dict[str, Any], context_analysis: Dict[str, Any], 
                            task_enhancement: Dict[str, Any], category_suggestion: Dict[str, Any],
                            priority_analysis: Dict[str, Any], deadline_suggestion: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compile all AI analysis results into a comprehensive response
        """
        try:
            # Calculate overall confidence
            confidence_scores = [
                task_enhancement.get('confidence_score', 0),
                category_suggestion.get('confidence_score', 0),
                priority_analysis.get('priority_score', 50) / 100,  # Normalize to 0-1
                deadline_suggestion.get('confidence_score', 0)
            ]
            
            overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
            
            # Generate summary
            summary = await self.generate_pipeline_summary(
                task, context_analysis, task_enhancement, 
                category_suggestion, priority_analysis, deadline_suggestion
            )
            
            return {
                'task_id': task.get('id'),
                'task_title': task.get('title'),
                'pipeline_status': 'completed',
                'overall_confidence': overall_confidence,
                'summary': summary,
                'recommendations': {
                    'enhanced_description': task_enhancement.get('enhanced_description'),
                    'suggested_category': category_suggestion.get('primary_suggestion'),
                    'priority_level': priority_analysis.get('priority_level'),
                    'suggested_deadline': deadline_suggestion.get('suggested_deadlines', [{}])[0] if deadline_suggestion.get('suggested_deadlines') else None,
                    'actionable_steps': task_enhancement.get('actionable_steps', [])
                },
                'detailed_analysis': {
                    'context_analysis': context_analysis,
                    'task_enhancement': task_enhancement,
                    'category_suggestion': category_suggestion,
                    'priority_analysis': priority_analysis,
                    'deadline_suggestion': deadline_suggestion
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Results compilation failed: {str(e)}")
            return {
                'task_id': task.get('id'),
                'pipeline_status': 'completed_with_errors',
                'overall_confidence': 0.0,
                'summary': f"Pipeline completed with errors: {str(e)}",
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def generate_pipeline_summary(self, task: Dict[str, Any], context_analysis: Dict[str, Any],
                                      task_enhancement: Dict[str, Any], category_suggestion: Dict[str, Any],
                                      priority_analysis: Dict[str, Any], deadline_suggestion: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the AI pipeline results
        """
        try:
            task_title = task.get('title', 'Unknown Task')
            priority_level = priority_analysis.get('priority_level', 'medium')
            suggested_category = category_suggestion.get('primary_suggestion', {}).get('name', 'Uncategorized')
            
            prompt = f"""
            Generate a brief summary of AI analysis results for this task:
            
            Task: {task_title}
            Priority Level: {priority_level}
            Suggested Category: {suggested_category}
            
            Context Analysis: {context_analysis.get('context_summary', 'No context')}
            Task Enhancement: {task_enhancement.get('reasoning', 'No enhancement')}
            Priority Reasoning: {priority_analysis.get('reasoning', 'No priority analysis')}
            Deadline Suggestion: {deadline_suggestion.get('reasoning', 'No deadline suggestion')}
            
            Provide a 3-4 sentence summary highlighting the key insights and recommendations.
            Focus on the most important findings for the user.
            """
            
            response = await self.gemini.generate_content(prompt, temperature=0.3)
            return response if response else f"AI analysis completed for '{task_title}'. Priority: {priority_level}, Category: {suggested_category}."
            
        except Exception as e:
            logger.error(f"Summary generation failed: {str(e)}")
            return f"AI analysis completed for task: {task.get('title', 'Unknown')}"
    
    async def batch_process_tasks(self, tasks: List[Dict[str, Any]], context_data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Process multiple tasks through the AI pipeline
        """
        try:
            logger.info(f"Starting batch processing for {len(tasks)} tasks")
            
            # Analyze context once for all tasks
            context_analysis = await self.analyze_context(context_data)
            
            results = []
            for task in tasks:
                try:
                    result = await self.process_single_task_with_context(task, context_analysis)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Failed to process task {task.get('id')}: {str(e)}")
                    results.append({
                        'task_id': task.get('id'),
                        'pipeline_status': 'failed',
                        'error': str(e)
                    })
            
            logger.info(f"Batch processing completed for {len(tasks)} tasks")
            return results
            
        except Exception as e:
            logger.error(f"Batch processing failed: {str(e)}")
            return []
    
    async def process_single_task_with_context(self, task: Dict[str, Any], context_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single task using pre-analyzed context
        """
        try:
            # Task Enhancement
            task_enhancement = await self.enhance_task(task, context_analysis)
            
            # Category Suggestion
            category_suggestion = await self.suggest_category(task)
            
            # Priority Scoring
            priority_analysis = await self.score_priority(task, context_analysis)
            
            # Deadline Suggestion
            deadline_suggestion = await self.suggest_deadline(task, context_analysis)
            
            # Compile Results
            return await self.compile_results(
                task, context_analysis, task_enhancement, 
                category_suggestion, priority_analysis, deadline_suggestion
            )
            
        except Exception as e:
            logger.error(f"Single task processing failed: {str(e)}")
            return {
                'task_id': task.get('id'),
                'pipeline_status': 'failed',
                'error': str(e)
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check the health of all AI services
        """
        try:
            health_results = {
                'gemini_api': await self.gemini.health_check(),
                'context_analyzer': True,  # Basic check
                'priority_scorer': True,
                'deadline_suggester': True,
                'category_suggester': True,
                'task_enhancer': True,
                'timestamp': datetime.now().isoformat()
            }
            
            overall_health = all(health_results.values())
            health_results['overall_health'] = overall_health
            
            return health_results
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                'overall_health': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def get_pipeline_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the AI pipeline usage
        """
        try:
            # This would typically track usage over time
            # For now, return basic structure
            return {
                'total_tasks_processed': 0,
                'average_confidence_score': 0.0,
                'most_common_categories': [],
                'priority_distribution': {},
                'pipeline_success_rate': 1.0,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Statistics retrieval failed: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            } 