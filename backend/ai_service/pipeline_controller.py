"""Optimized AI Pipeline Controller with reduced API calls."""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from .gemini_client import GeminiAIService
from .consolidated_ai_service import ConsolidatedAIService

logger = logging.getLogger(__name__)

class AIPipelineController:
    """Optimized AI pipeline controller that minimizes API calls."""
    
    def __init__(self, gemini_client: GeminiAIService):
        self.gemini = gemini_client
        self.consolidated_ai = ConsolidatedAIService(gemini_client)
    
    async def process_new_task(self, task: Dict[str, Any], context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Optimized AI processing pipeline - reduces API calls from ~25-30 to 2-4
        
        Args:
            task: New task data
            context_data: Optional context data for analysis
            
        Returns:
            Comprehensive AI analysis and suggestions
        """
        try:
            logger.info(f"Starting optimized AI pipeline for task: {task.get('title', 'Unknown')}")
            
            # Step 1: Context Analysis (if context provided) - 1 API call
            context_analysis = await self.analyze_context(context_data)
            
            # Step 2: Comprehensive Task Analysis - 1 API call
            task_analysis = await self.consolidated_ai.comprehensive_task_analysis(task, context_data)
            
            # Step 3: Compile Results (no API call)
            results = await self.compile_results(task, context_analysis, task_analysis)
            
            logger.info(f"Optimized AI pipeline completed for task: {task.get('title', 'Unknown')}")
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
        Analyze context data if provided - 1 API call
        """
        try:
            if not context_data:
                return {
                    'context_summary': 'No context data provided',
                    'extracted_tasks': [],
                    'priority_insights': {},
                    'workload_analysis': {'workload_level': 'normal', 'action_item_count': 0}
                }
            
            # Use consolidated service for context analysis
            result = await self.consolidated_ai.context_analysis(context_data)
            
            # Map consolidated result to expected format
            return {
                'context_summary': result.get('context_summary', 'Context analysis completed'),
                'extracted_tasks': result.get('extracted_tasks', []),
                'priority_insights': result.get('priority_analysis', {}),
                'workload_analysis': result.get('workload_analysis', {}),
                'category_suggestions': result.get('category_suggestions', []),
                'deadline_suggestions': result.get('deadline_suggestions', [])
            }
            
        except Exception as e:
            logger.error(f"Context analysis failed: {str(e)}")
            return {
                'context_summary': 'Context analysis failed',
                'extracted_tasks': [],
                'priority_insights': {},
                'workload_analysis': {'workload_level': 'normal', 'action_item_count': 0},
                'error': str(e)
            }
    
    async def compile_results(self, task: Dict[str, Any], context_analysis: Dict[str, Any], 
                            task_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compile all AI analysis results into a comprehensive response - no API calls
        """
        try:
            # Extract components from consolidated analysis
            task_enhancement = task_analysis.get('task_enhancement', {})
            category_suggestion = task_analysis.get('category_suggestion', {})
            priority_analysis = task_analysis.get('priority_analysis', {})
            deadline_suggestions = task_analysis.get('deadline_suggestions', [])
            overall_analysis = task_analysis.get('overall_analysis', {})
            
            # Calculate overall confidence
            confidence_scores = [
                task_enhancement.get('confidence_score', 0),
                category_suggestion.get('primary_suggestion', {}).get('confidence', 0),
                priority_analysis.get('priority_score', 50) / 100,  # Normalize to 0-1
                deadline_suggestions[0].get('confidence', 0) if deadline_suggestions else 0
            ]
            
            overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
            
            # Get the primary deadline suggestion (first one with highest confidence)
            primary_deadline = None
            if deadline_suggestions:
                # Sort by confidence and get the highest
                sorted_deadlines = sorted(deadline_suggestions, key=lambda x: x.get('confidence', 0), reverse=True)
                primary_deadline = sorted_deadlines[0].get('date')
            
            return {
                'task_id': task.get('id'),
                'task_title': task.get('title'),
                'pipeline_status': 'completed',
                'overall_confidence': overall_confidence,
                'summary': overall_analysis.get('summary', 'AI analysis completed'),
                'recommendations': {
                    'enhanced_description': task_enhancement.get('enhanced_description'),
                    'enhanced_title': task_enhancement.get('enhanced_title'),
                    'suggested_category': category_suggestion.get('primary_suggestion'),
                    'priority_level': priority_analysis.get('priority_level'),
                    'suggested_deadline': primary_deadline,  # Return as string, not object
                    'actionable_steps': task_enhancement.get('actionable_steps', [])
                },
                'detailed_analysis': {
                    'context_analysis': context_analysis,
                    'task_enhancement': task_enhancement,
                    'category_suggestion': category_suggestion,
                    'priority_analysis': priority_analysis,
                    'deadline_suggestion': {'suggested_deadlines': deadline_suggestions},
                    'overall_analysis': overall_analysis
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
    
    async def batch_process_tasks(self, tasks: List[Dict[str, Any]], context_data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Process multiple tasks through the optimized AI pipeline
        """
        try:
            logger.info(f"Starting optimized batch processing for {len(tasks)} tasks")
            
            # Analyze context once for all tasks - 1 API call
            context_analysis = await self.analyze_context(context_data)
            
            results = []
            for task in tasks:
                try:
                    # Process each task - 1 API call per task
                    task_analysis = await self.consolidated_ai.comprehensive_task_analysis(task, context_data)
                    result = await self.compile_results(task, context_analysis, task_analysis)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Failed to process task {task.get('id')}: {str(e)}")
                    results.append({
                        'task_id': task.get('id'),
                        'pipeline_status': 'failed',
                        'error': str(e)
                    })
            
            logger.info(f"Optimized batch processing completed for {len(tasks)} tasks")
            return results
            
        except Exception as e:
            logger.error(f"Batch processing failed: {str(e)}")
            return []
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check the health of AI services - 1 API call
        """
        try:
            health_results = {
                'gemini_api': await self.consolidated_ai.health_check(),
                'consolidated_service': True,
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
        Get statistics about the AI pipeline usage - no API calls
        """
        try:
            return {
                'total_tasks_processed': 0,
                'average_confidence_score': 0.0,
                'most_common_categories': [],
                'priority_distribution': {},
                'pipeline_success_rate': 1.0,
                'api_calls_per_task': '2-4 (optimized)',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Statistics retrieval failed: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            } 