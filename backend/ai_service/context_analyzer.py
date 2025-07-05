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
                return self._generate_fallback_deadlines(combined_text)
            
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
            
            # If no valid deadlines from AI, generate fallback deadlines
            if not validated_deadlines:
                logger.info("No valid AI deadlines, generating fallback deadlines")
                return self._generate_fallback_deadlines(combined_text)
            
            # Sort by confidence and return top 5
            validated_deadlines.sort(key=lambda x: x['confidence'], reverse=True)
            result = validated_deadlines[:5]
            logger.info(f"Final validated deadlines: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Deadline suggestion generation failed: {str(e)}")
            return self._generate_fallback_deadlines(combined_text)
    
    def _generate_fallback_deadlines(self, text_content: str) -> List[Dict]:
        """
        Generate fallback deadline suggestions when AI fails or provides invalid dates
        """
        from datetime import datetime, timedelta
        
        today = datetime.now().date()
        fallback_deadlines = []
        
        # Generate deadlines based on common patterns in the text
        text_lower = text_content.lower()
        
        # Tomorrow
        if 'tomorrow' in text_lower:
            tomorrow = today + timedelta(days=1)
            fallback_deadlines.append({
                'date': tomorrow.strftime('%Y-%m-%d'),
                'reason': 'Based on "tomorrow" reference in context',
                'confidence': 0.9,
                'urgency_level': 'high'
            })
        
        # This week
        if 'this week' in text_lower or 'end of week' in text_lower:
            # Find next Friday
            days_until_friday = (4 - today.weekday()) % 7
            if days_until_friday == 0:
                days_until_friday = 7  # If today is Friday, use next Friday
            friday = today + timedelta(days=days_until_friday)
            fallback_deadlines.append({
                'date': friday.strftime('%Y-%m-%d'),
                'reason': 'Based on "this week" or "end of week" reference',
                'confidence': 0.8,
                'urgency_level': 'medium'
            })
        
        # Next week
        if 'next week' in text_lower:
            next_week = today + timedelta(days=7)
            fallback_deadlines.append({
                'date': next_week.strftime('%Y-%m-%d'),
                'reason': 'Based on "next week" reference',
                'confidence': 0.8,
                'urgency_level': 'medium'
            })
        
        # 2 weeks
        if '2 weeks' in text_lower or 'two weeks' in text_lower:
            two_weeks = today + timedelta(days=14)
            fallback_deadlines.append({
                'date': two_weeks.strftime('%Y-%m-%d'),
                'reason': 'Based on "2 weeks" reference',
                'confidence': 0.7,
                'urgency_level': 'low'
            })
        
        # End of month
        if 'end of month' in text_lower or 'month end' in text_lower:
            # Get last day of current month
            if today.month == 12:
                end_of_month = datetime(today.year + 1, 1, 1) - timedelta(days=1)
            else:
                end_of_month = datetime(today.year, today.month + 1, 1) - timedelta(days=1)
            fallback_deadlines.append({
                'date': end_of_month.strftime('%Y-%m-%d'),
                'reason': 'Based on "end of month" reference',
                'confidence': 0.7,
                'urgency_level': 'low'
            })
        
        # Add some default suggestions if we don't have enough
        if len(fallback_deadlines) < 3:
            # Add tomorrow as default
            tomorrow = today + timedelta(days=1)
            if not any(d['date'] == tomorrow.strftime('%Y-%m-%d') for d in fallback_deadlines):
                fallback_deadlines.append({
                    'date': tomorrow.strftime('%Y-%m-%d'),
                    'reason': 'Default immediate deadline',
                    'confidence': 0.6,
                    'urgency_level': 'high'
                })
            
            # Add 3 days from now
            three_days = today + timedelta(days=3)
            if not any(d['date'] == three_days.strftime('%Y-%m-%d') for d in fallback_deadlines):
                fallback_deadlines.append({
                    'date': three_days.strftime('%Y-%m-%d'),
                    'reason': 'Default short-term deadline',
                    'confidence': 0.5,
                    'urgency_level': 'medium'
                })
            
            # Add 1 week from now
            one_week = today + timedelta(days=7)
            if not any(d['date'] == one_week.strftime('%Y-%m-%d') for d in fallback_deadlines):
                fallback_deadlines.append({
                    'date': one_week.strftime('%Y-%m-%d'),
                    'reason': 'Default medium-term deadline',
                    'confidence': 0.4,
                    'urgency_level': 'low'
                })
        
        # Sort by confidence and return top 5
        fallback_deadlines.sort(key=lambda x: x['confidence'], reverse=True)
        return fallback_deadlines[:5]
    
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
                return self._generate_fallback_summary(processed_context)
            
            summary = ai_result.get('summary', '')
            if summary and summary.strip():
                return summary.strip()
            else:
                return self._generate_fallback_summary(processed_context)
            
        except Exception as e:
            logger.error(f"Context summary creation failed: {str(e)}")
            return self._generate_fallback_summary(processed_context)
    
    def _generate_fallback_summary(self, processed_context: Dict[str, Any]) -> str:
        """
        Generate a basic fallback summary when AI fails
        """
        text_content = processed_context['text_content']
        
        if not text_content:
            return "No content to analyze."
        
        # Count sources
        sources = set(item['source'] for item in text_content)
        
        # Get a sample of content for context
        sample_content = text_content[0]['content'][:100] if text_content else ""
        
        return f"Analyzed content from {len(sources)} sources. Sample content: {sample_content}..."
    
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
                return self._generate_fallback_categories(combined_text)
            
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
            
            # If no valid categories from AI, generate fallback categories
            if not validated_categories:
                logger.info("No valid AI categories, generating fallback categories")
                return self._generate_fallback_categories(combined_text)
            
            # Sort by confidence and return top 5
            validated_categories.sort(key=lambda x: x['confidence'], reverse=True)
            result = validated_categories[:5]
            logger.info(f"Final validated categories: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Category suggestion generation failed: {str(e)}")
            return self._generate_fallback_categories(combined_text)
    
    def _generate_fallback_categories(self, text_content: str) -> List[Dict]:
        """
        Generate fallback category suggestions when AI fails
        """
        fallback_categories = []
        text_lower = text_content.lower()
        
        # Work-related categories
        if any(word in text_lower for word in ['project', 'report', 'proposal', 'document']):
            fallback_categories.append({
                'name': 'Work',
                'reason': 'Based on work-related content',
                'confidence': 0.8,
                'relevance': 'high'
            })
        
        if any(word in text_lower for word in ['meeting', 'client', 'presentation']):
            fallback_categories.append({
                'name': 'Communication',
                'reason': 'Based on communication-related content',
                'confidence': 0.7,
                'relevance': 'medium'
            })
        
        if any(word in text_lower for word in ['deadline', 'schedule', 'plan']):
            fallback_categories.append({
                'name': 'Planning',
                'reason': 'Based on planning and scheduling content',
                'confidence': 0.6,
                'relevance': 'medium'
            })
        
        # Personal categories
        if any(word in text_lower for word in ['home', 'family', 'personal']):
            fallback_categories.append({
                'name': 'Personal',
                'reason': 'Based on personal content',
                'confidence': 0.7,
                'relevance': 'high'
            })
        
        if any(word in text_lower for word in ['health', 'exercise', 'fitness']):
            fallback_categories.append({
                'name': 'Health',
                'reason': 'Based on health-related content',
                'confidence': 0.8,
                'relevance': 'high'
            })
        
        # Add default categories if we don't have enough
        if len(fallback_categories) < 5:
            default_categories = [
                {'name': 'General', 'reason': 'Default category', 'confidence': 0.5, 'relevance': 'low'},
                {'name': 'Tasks', 'reason': 'General task category', 'confidence': 0.4, 'relevance': 'low'},
                {'name': 'Important', 'reason': 'Important items', 'confidence': 0.3, 'relevance': 'low'}
            ]
            
            for default_cat in default_categories:
                if len(fallback_categories) < 5 and not any(cat['name'] == default_cat['name'] for cat in fallback_categories):
                    fallback_categories.append(default_cat)
        
        # Sort by confidence and return top 5
        fallback_categories.sort(key=lambda x: x['confidence'], reverse=True)
        return fallback_categories[:5] 