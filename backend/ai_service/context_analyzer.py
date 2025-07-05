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
            
            # Step 5: Create context summary
            context_summary = await self.create_context_summary(processed_context)
            
            return {
                'extracted_tasks': extracted_tasks,
                'priority_insights': priority_insights,
                'workload_analysis': workload_analysis,
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
                'context_summary': "Analysis failed"
            }
    
    async def preprocess_context(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and structure context data for AI processing
        """
        processed = {
            'text_content': [],
            'temporal_data': [],
            'priority_indicators': [],
            'action_items': []
        }
        
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
        
        # Extract temporal data
        processed['temporal_data'] = self.extract_temporal_data(processed['text_content'])
        
        # Extract priority indicators
        processed['priority_indicators'] = self.extract_priority_indicators(processed['text_content'])
        
        return processed
    
    def extract_temporal_data(self, text_content: List[Dict]) -> List[Dict]:
        """
        Extract temporal information from text content
        """
        temporal_data = []
        
        for item in text_content:
            content = item['content'].lower()
            
            # Look for date/time patterns
            if any(word in content for word in ['today', 'tomorrow', 'next week', 'this week']):
                temporal_data.append({
                    'source': item['source'],
                    'temporal_reference': self.extract_temporal_reference(content),
                    'content': item['content']
                })
        
        return temporal_data
    
    def extract_temporal_reference(self, content: str) -> str:
        """
        Extract temporal reference from content
        """
        if 'today' in content:
            return 'today'
        elif 'tomorrow' in content:
            return 'tomorrow'
        elif 'next week' in content:
            return 'next_week'
        elif 'this week' in content:
            return 'this_week'
        else:
            return 'unknown'
    
    def extract_priority_indicators(self, text_content: List[Dict]) -> List[Dict]:
        """
        Extract priority indicators from text content
        """
        priority_indicators = []
        
        priority_keywords = {
            'urgent': ['urgent', 'asap', 'immediately', 'right away', 'emergency'],
            'important': ['important', 'critical', 'essential', 'vital', 'key'],
            'high_priority': ['high priority', 'top priority', 'priority 1'],
            'deadline': ['deadline', 'due date', 'by', 'before', 'until']
        }
        
        for item in text_content:
            content = item['content'].lower()
            
            for priority_type, keywords in priority_keywords.items():
                if any(keyword in content for keyword in keywords):
                    priority_indicators.append({
                        'source': item['source'],
                        'priority_type': priority_type,
                        'content': item['content'],
                        'confidence': 0.8
                    })
        
        return priority_indicators
    
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
        Analyze priority patterns in the context
        """
        try:
            priority_indicators = processed_context['priority_indicators']
            
            if not priority_indicators:
                return {
                    'priority_distribution': {},
                    'urgency_level': 'normal',
                    'insights': 'No priority indicators found'
                }
            
            # Count priority types
            priority_counts = {}
            for indicator in priority_indicators:
                priority_type = indicator['priority_type']
                priority_counts[priority_type] = priority_counts.get(priority_type, 0) + 1
            
            # Determine overall urgency level
            urgency_level = 'normal'
            if priority_counts.get('urgent', 0) > 0:
                urgency_level = 'high'
            elif priority_counts.get('important', 0) > 2:
                urgency_level = 'medium'
            
            return {
                'priority_distribution': priority_counts,
                'urgency_level': urgency_level,
                'total_priority_indicators': len(priority_indicators),
                'insights': f"Found {len(priority_indicators)} priority indicators across {len(set(ind['source'] for ind in priority_indicators))} sources"
            }
            
        except Exception as e:
            logger.error(f"Priority pattern analysis failed: {str(e)}")
            return {'error': str(e)}
    
    async def analyze_workload(self, processed_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze current workload based on context
        """
        try:
            text_content = processed_context['text_content']
            temporal_data = processed_context['temporal_data']
            
            # Count action items
            action_item_count = len([item for item in text_content if self.is_action_item(item['content'])])
            
            # Analyze temporal distribution
            temporal_distribution = {}
            for item in temporal_data:
                ref = item['temporal_reference']
                temporal_distribution[ref] = temporal_distribution.get(ref, 0) + 1
            
            # Determine workload level
            workload_level = 'normal'
            if action_item_count > 10:
                workload_level = 'high'
            elif action_item_count > 5:
                workload_level = 'medium'
            
            return {
                'action_item_count': action_item_count,
                'temporal_distribution': temporal_distribution,
                'workload_level': workload_level,
                'insights': f"Identified {action_item_count} potential action items"
            }
            
        except Exception as e:
            logger.error(f"Workload analysis failed: {str(e)}")
            return {'error': str(e)}
    
    def is_action_item(self, content: str) -> bool:
        """
        Check if content contains action items
        """
        action_keywords = [
            'need to', 'have to', 'must', 'should', 'will', 'going to',
            'plan to', 'intend to', 'schedule', 'book', 'call', 'email',
            'meet', 'review', 'complete', 'finish', 'submit', 'send'
        ]
        
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in action_keywords)
    
    async def create_context_summary(self, processed_context: Dict[str, Any]) -> str:
        """
        Create a summary of the context analysis
        """
        try:
            text_content = processed_context['text_content']
            priority_indicators = processed_context['priority_indicators']
            temporal_data = processed_context['temporal_data']
            
            summary_parts = []
            
            # Add source summary
            sources = set(item['source'] for item in text_content)
            summary_parts.append(f"Analyzed content from {len(sources)} sources: {', '.join(sources)}")
            
            # Add priority summary
            if priority_indicators:
                summary_parts.append(f"Found {len(priority_indicators)} priority indicators")
            
            # Add temporal summary
            if temporal_data:
                summary_parts.append(f"Identified {len(temporal_data)} time-sensitive items")
            
            # Add action item summary
            action_items = [item for item in text_content if self.is_action_item(item['content'])]
            summary_parts.append(f"Detected {len(action_items)} potential action items")
            
            return ". ".join(summary_parts) + "."
            
        except Exception as e:
            logger.error(f"Context summary creation failed: {str(e)}")
            return "Context analysis completed with errors." 