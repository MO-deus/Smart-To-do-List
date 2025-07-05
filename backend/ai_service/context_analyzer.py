import json
import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta
from .gemini_client import GeminiAIService

logger = logging.getLogger(__name__)

class ContextAnalyzer:
    """
    Analyzes context data (WhatsApp messages, emails, notes) to extract insights
    and actionable tasks
    """
    
    def __init__(self, gemini_client: GeminiAIService):
        self.gemini = gemini_client
        
    async def analyze_context(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main context analysis pipeline
        
        Args:
            context_data: Dictionary containing context from various sources
            
        Returns:
            Analysis results with extracted tasks and insights
        """
        try:
            # Step 1: Preprocess context data
            processed_context = await self.preprocess_context(context_data)
            
            # Step 2: Extract tasks from context
            extracted_tasks = await self.extract_tasks_from_context(processed_context)
            
            # Step 3: Analyze priority patterns
            priority_insights = await self.analyze_priority_patterns(processed_context)
            
            # Step 4: Generate workload insights
            workload_analysis = await self.analyze_workload(processed_context)
            
            # Step 5: Generate category suggestions
            category_suggestions = await self.generate_category_suggestions(processed_context)
            
            # Step 6: Create context summary
            context_summary = await self.create_context_summary(processed_context)
            
            return {
                'extracted_tasks': extracted_tasks,
                'priority_insights': priority_insights,
                'workload_analysis': workload_analysis,
                'category_suggestions': category_suggestions,
                'context_summary': context_summary,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Context analysis failed: {str(e)}")
            return {
                'error': str(e),
                'extracted_tasks': [],
                'priority_insights': {},
                'workload_analysis': {},
                'category_suggestions': [],
                'context_summary': "Analysis failed"
            }
    
    async def preprocess_context(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and structure context data for AI processing
        """
        processed = {
            'text_content': []
        }
        
        # Process simple text content (from manual input)
        if 'content' in context_data:
            processed['text_content'].append({
                'source': context_data.get('source', 'manual_input'),
                'content': context_data.get('content', ''),
                'timestamp': context_data.get('timestamp', ''),
                'sender': 'user'
            })
        
        # Process WhatsApp messages
        if 'whatsapp_messages' in context_data:
            for msg in context_data['whatsapp_messages']:
                processed['text_content'].append({
                    'source': 'whatsapp',
                    'content': msg.get('content', ''),
                    'timestamp': msg.get('timestamp', ''),
                    'sender': msg.get('sender', '')
                })
        
        # Process emails
        if 'emails' in context_data:
            for email in context_data['emails']:
                processed['text_content'].append({
                    'source': 'email',
                    'content': f"Subject: {email.get('subject', '')}\nBody: {email.get('body', '')}",
                    'timestamp': email.get('timestamp', ''),
                    'sender': email.get('sender', '')
                })
        
        # Process notes
        if 'notes' in context_data:
            for note in context_data['notes']:
                processed['text_content'].append({
                    'source': 'note',
                    'content': note.get('content', ''),
                    'timestamp': note.get('timestamp', ''),
                    'title': note.get('title', '')
                })
        
        return processed
    
    async def extract_tasks_from_context(self, processed_context: Dict[str, Any]) -> List[Dict]:
        """
        Extract actionable tasks from processed context using AI
        """
        try:
            # Combine all text content
            combined_text = "\n\n".join([
                f"[{item['source']}] {item['content']}"
                for item in processed_context['text_content']
            ])
            
            if not combined_text.strip():
                return []
            
            # Use AI to extract tasks
            analysis_result = await self.gemini.analyze_text(combined_text, 'extract_tasks')
            
            if 'error' in analysis_result:
                logger.warning(f"AI task extraction failed: {analysis_result['error']}")
                return []
            
            extracted_tasks = analysis_result.get('extracted_tasks', [])
            
            # Add metadata to extracted tasks
            for task in extracted_tasks:
                task['source'] = 'context_analysis'
                task['extraction_timestamp'] = datetime.now().isoformat()
                task['confidence'] = task.get('confidence', 0.7)
            
            return extracted_tasks
            
        except Exception as e:
            logger.error(f"Task extraction failed: {str(e)}")
            return []
    
    async def analyze_priority_patterns(self, processed_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze priority patterns in the context using AI
        """
        try:
            # Combine all text content for AI analysis
            combined_text = "\n\n".join([
                f"[{item['source']}] {item['content']}"
                for item in processed_context['text_content']
            ])
            
            if not combined_text.strip():
                return {
                    'priority_distribution': {},
                    'urgency_level': 'normal',
                    'insights': 'No content to analyze'
                }
            
            # Use AI to analyze priority patterns
            ai_result = await self.gemini.analyze_text(combined_text, 'priority_analysis')
            
            if 'error' in ai_result:
                logger.warning(f"AI priority analysis failed: {ai_result['error']}")
                return {
                    'priority_distribution': {},
                    'urgency_level': 'normal',
                    'insights': 'Priority analysis failed'
                }
            
            return {
                'priority_distribution': ai_result.get('priority_distribution', {}),
                'urgency_level': ai_result.get('urgency_level', 'normal'),
                'total_priority_indicators': ai_result.get('total_indicators', 0),
                'insights': ai_result.get('insights', 'AI priority analysis completed')
            }
            
        except Exception as e:
            logger.error(f"Priority pattern analysis failed: {str(e)}")
            return {'error': str(e)}
    
    async def analyze_workload(self, processed_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze current workload based on context and generate deadline suggestions using AI
        """
        try:
            text_content = processed_context['text_content']
            
            # Combine all text content for AI analysis
            combined_text = "\n\n".join([
                f"[{item['source']}] {item['content']}"
                for item in text_content
            ])
            
            if not combined_text.strip():
                return {
                    'action_item_count': 0,
                    'temporal_distribution': {},
                    'workload_level': 'normal',
                    'suggested_deadlines': [],
                    'insights': 'No content to analyze'
                }
            
            # Use AI to analyze workload and generate deadline suggestions
            ai_result = await self.gemini.analyze_text(combined_text, 'workload_analysis')
            
            if 'error' in ai_result:
                logger.warning(f"AI workload analysis failed: {ai_result['error']}")
                return {
                    'action_item_count': 0,
                    'temporal_distribution': {},
                    'workload_level': 'normal',
                    'suggested_deadlines': [],
                    'insights': 'Workload analysis failed'
                }
            
            # Generate deadline suggestions using AI
            suggested_deadlines = await self.generate_deadline_suggestions([], text_content)
            
            return {
                'action_item_count': ai_result.get('action_item_count', 0),
                'temporal_distribution': ai_result.get('temporal_distribution', {}),
                'workload_level': ai_result.get('workload_level', 'normal'),
                'suggested_deadlines': suggested_deadlines,
                'insights': ai_result.get('insights', 'AI workload analysis completed')
            }
            
        except Exception as e:
            logger.error(f"Workload analysis failed: {str(e)}")
            return {'error': str(e)}
    
    async def generate_deadline_suggestions(self, temporal_data: List[Dict], text_content: List[Dict]) -> List[Dict]:
        """
        Generate deadline suggestions based on temporal data and context using AI
        """
        try:
            # Combine all text content for AI analysis
            combined_text = "\n\n".join([
                f"[{item['source']}] {item['content']}"
                for item in text_content
            ])
            
            if not combined_text.strip():
                logger.warning("No text content available for deadline suggestions")
                return []
            
            logger.info(f"Generating deadline suggestions for text: {combined_text[:200]}...")
            
            # Use AI to generate deadline suggestions
            ai_result = await self.gemini.analyze_text(combined_text, 'deadline_suggestions')
            
            if 'error' in ai_result:
                logger.warning(f"AI deadline suggestions failed: {ai_result['error']}")
                return []
            
            logger.info(f"AI deadline result: {ai_result}")
            
            suggested_deadlines = ai_result.get('suggested_deadlines', [])
            logger.info(f"Raw suggested deadlines: {suggested_deadlines}")
            
            # Validate and format dates
            validated_deadlines = []
            for deadline in suggested_deadlines:
                try:
                    # Ensure date is in ISO format
                    date_str = deadline.get('date', '')
                    if date_str:
                        # Parse and validate the date
                        from datetime import datetime
                        parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
                        # Ensure it's not in the past
                        if parsed_date.date() >= datetime.now().date():
                            validated_deadlines.append({
                                'date': parsed_date.strftime('%Y-%m-%d'),
                                'reason': deadline.get('reason', 'AI suggested deadline'),
                                'confidence': deadline.get('confidence', 0.7),
                                'urgency_level': deadline.get('urgency_level', 'medium')
                            })
                            logger.info(f"Validated deadline: {parsed_date.strftime('%Y-%m-%d')} - {deadline.get('reason', 'AI suggested deadline')}")
                        else:
                            logger.warning(f"Skipping past date: {date_str}")
                    else:
                        logger.warning(f"Empty date in deadline suggestion: {deadline}")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Invalid date format in AI suggestion: {e}, deadline: {deadline}")
                    continue
            
            # Sort by confidence and return top 5
            validated_deadlines.sort(key=lambda x: x['confidence'], reverse=True)
            result = validated_deadlines[:5]
            logger.info(f"Final validated deadlines: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Deadline suggestion generation failed: {str(e)}")
            return []
    
    async def create_context_summary(self, processed_context: Dict[str, Any]) -> str:
        """
        Create a summary of the context analysis using AI
        """
        try:
            # Combine all text content for AI analysis
            combined_text = "\n\n".join([
                f"[{item['source']}] {item['content']}"
                for item in processed_context['text_content']
            ])
            
            if not combined_text.strip():
                return "No content to analyze."
            
            # Use AI to generate a meaningful summary
            ai_result = await self.gemini.analyze_text(combined_text, 'context_summary')
            
            if 'error' in ai_result:
                logger.warning(f"AI context summary failed: {ai_result['error']}")
                return "AI analysis failed."
            
            summary = ai_result.get('summary', '')
            if summary and summary.strip():
                return summary.strip()
            else:
                return "No summary generated."
            
        except Exception as e:
            logger.error(f"Context summary creation failed: {str(e)}")
            return "Summary generation failed."
    
    async def generate_category_suggestions(self, processed_context: Dict[str, Any]) -> List[Dict]:
        """
        Generate category suggestions based on context using AI
        """
        try:
            # Combine all text content for AI analysis
            combined_text = "\n\n".join([
                f"[{item['source']}] {item['content']}"
                for item in processed_context['text_content']
            ])
            
            if not combined_text.strip():
                logger.warning("No text content available for category suggestions")
                return []
            
            logger.info(f"Generating category suggestions for text: {combined_text[:200]}...")
            
            # Use AI to generate category suggestions
            ai_result = await self.gemini.analyze_text(combined_text, 'category_suggestions')
            
            if 'error' in ai_result:
                logger.warning(f"AI category suggestions failed: {ai_result['error']}")
                return []
            
            logger.info(f"AI category result: {ai_result}")
            
            suggested_categories = ai_result.get('suggested_categories', [])
            logger.info(f"Raw suggested categories: {suggested_categories}")
            
            # Validate and format categories
            validated_categories = []
            for category in suggested_categories:
                try:
                    name = category.get('name', '').strip()
                    if name and len(name) <= 50:  # Limit category name length
                        validated_categories.append({
                            'name': name,
                            'reason': category.get('reason', 'AI suggested category'),
                            'confidence': category.get('confidence', 0.7),
                            'relevance': category.get('relevance', 'medium')
                        })
                        logger.info(f"Validated category: {name} - {category.get('reason', 'AI suggested category')}")
                    else:
                        logger.warning(f"Invalid category name: {name}")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Invalid category format: {e}, category: {category}")
                    continue
            
            # Sort by confidence and return top 5
            validated_categories.sort(key=lambda x: x['confidence'], reverse=True)
            result = validated_categories[:5]
            logger.info(f"Final validated categories: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Category suggestion generation failed: {str(e)}")
            return [] 