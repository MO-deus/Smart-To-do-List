import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from .gemini_client import GeminiAIService

logger = logging.getLogger(__name__)

class CategorySuggester:
    """
    AI-powered category suggestion system
    Analyzes task content to suggest appropriate categories
    """
    
    def __init__(self, gemini_client: GeminiAIService):
        self.gemini = gemini_client
    
    async def suggest_category(self, task: Dict[str, Any], existing_categories: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        AI-powered category suggestion
        
        Args:
            task: Task data including title, description
            existing_categories: List of existing category names
            
        Returns:
            Category suggestions with confidence scores
        """
        try:
            # Step 1: Analyze task content
            content_analysis = await self.analyze_task_content(task)
            
            # Step 2: Generate category suggestions
            category_suggestions = await self.generate_category_suggestions(task, content_analysis, existing_categories)
            
            # Step 3: Rank suggestions by relevance
            ranked_suggestions = await self.rank_category_suggestions(category_suggestions, task)
            
            # Step 4: Generate reasoning
            reasoning = await self.generate_category_reasoning(task, ranked_suggestions)
            
            return {
                'suggested_categories': ranked_suggestions,
                'primary_suggestion': ranked_suggestions[0] if ranked_suggestions else None,
                'reasoning': reasoning,
                'confidence_score': self.calculate_category_confidence(ranked_suggestions),
                'content_analysis': content_analysis,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Category suggestion failed: {str(e)}")
            return {
                'suggested_categories': [],
                'primary_suggestion': None,
                'reasoning': f"Category suggestion failed: {str(e)}",
                'confidence_score': 0.0,
                'error': str(e)
            }
    
    async def analyze_task_content(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze task content for categorization
        """
        try:
            task_text = f"Title: {task.get('title', '')}\nDescription: {task.get('description', '')}"
            
            prompt = f"""
            Analyze this task for categorization:
            
            {task_text}
            
            Identify:
            1. Primary domain/area
            2. Task type (creative, administrative, technical, etc.)
            3. Key themes and topics
            4. Skill areas involved
            5. Context indicators
            
            Return as JSON:
            {{
                "primary_domain": "work/personal/health/education",
                "task_type": "creative/administrative/technical/planning",
                "themes": ["theme1", "theme2"],
                "skill_areas": ["skill1", "skill2"],
                "context_indicators": ["indicator1", "indicator2"],
                "complexity_level": "simple/medium/complex"
            }}
            """
            
            result = await self.gemini.generate_structured_response(prompt)
            return result if 'error' not in result else {}
            
        except Exception as e:
            logger.error(f"Task content analysis failed: {str(e)}")
            return {}
    
    async def generate_category_suggestions(self, task: Dict[str, Any], content_analysis: Dict[str, Any], 
                                          existing_categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Generate category suggestions using AI
        """
        try:
            task_text = f"Title: {task.get('title', '')}\nDescription: {task.get('description', '')}"
            content_summary = str(content_analysis)
            
            existing_cats = existing_categories or []
            existing_cats_text = ", ".join(existing_cats) if existing_cats else "None"
            
            prompt = f"""
            Suggest categories for this task:
            
            Task: {task_text}
            Content Analysis: {content_summary}
            Existing Categories: {existing_cats_text}
            
            Please suggest:
            1. Best matching existing category (if any)
            2. New category suggestions
            3. Subcategory suggestions
            
            Consider:
            - Task content and themes
            - Existing category structure
            - Logical grouping
            - User preferences
            
            Return as JSON:
            {{
                "existing_category_match": "category_name or null",
                "new_category_suggestions": [
                    {{
                        "name": "Category Name",
                        "description": "Brief description",
                        "confidence": 0.85,
                        "reasoning": "Why this category fits"
                    }}
                ],
                "subcategory_suggestions": [
                    {{
                        "parent_category": "Main Category",
                        "subcategory": "Subcategory Name",
                        "confidence": 0.8
                    }}
                ]
            }}
            """
            
            result = await self.gemini.generate_structured_response(prompt)
            
            if 'error' in result:
                return []
            
            suggestions = []
            
            # Add existing category match
            if result.get('existing_category_match'):
                suggestions.append({
                    'name': result['existing_category_match'],
                    'type': 'existing',
                    'confidence': 0.9,
                    'reasoning': 'Matches existing category'
                })
            
            # Add new category suggestions
            for new_cat in result.get('new_category_suggestions', []):
                suggestions.append({
                    'name': new_cat.get('name', ''),
                    'type': 'new',
                    'description': new_cat.get('description', ''),
                    'confidence': new_cat.get('confidence', 0.7),
                    'reasoning': new_cat.get('reasoning', 'AI suggested category')
                })
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Category suggestion generation failed: {str(e)}")
            return []
    
    async def rank_category_suggestions(self, suggestions: List[Dict[str, Any]], task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Rank category suggestions by relevance
        """
        try:
            if not suggestions:
                return []
            
            # Sort by confidence score (highest first)
            ranked = sorted(suggestions, key=lambda x: x.get('confidence', 0), reverse=True)
            
            # Add ranking metadata
            for i, suggestion in enumerate(ranked):
                suggestion['rank'] = i + 1
                suggestion['score'] = suggestion.get('confidence', 0)
            
            return ranked
            
        except Exception as e:
            logger.error(f"Category ranking failed: {str(e)}")
            return suggestions
    
    async def generate_category_reasoning(self, task: Dict[str, Any], suggestions: List[Dict[str, Any]]) -> str:
        """
        Generate human-readable reasoning for category suggestions
        """
        try:
            if not suggestions:
                return "No category suggestions available."
            
            primary_suggestion = suggestions[0]
            
            prompt = f"""
            Generate a brief explanation for this category suggestion:
            
            Task: {task.get('title', '')}
            Suggested Category: {primary_suggestion.get('name', '')}
            Confidence: {primary_suggestion.get('confidence', 0)}
            Reasoning: {primary_suggestion.get('reasoning', '')}
            
            Provide a 2-3 sentence explanation of why this category is suggested.
            Focus on the key factors that make this category appropriate.
            """
            
            response = await self.gemini.generate_content(prompt, temperature=0.3)
            return response if response else primary_suggestion.get('reasoning', 'Category suggested based on task analysis.')
            
        except Exception as e:
            logger.error(f"Category reasoning generation failed: {str(e)}")
            return "Category suggestion based on task analysis."
    
    def calculate_category_confidence(self, suggestions: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence score for category suggestions
        """
        try:
            if not suggestions:
                return 0.0
            
            # Use the highest confidence score
            max_confidence = max(s.get('confidence', 0) for s in suggestions)
            
            # Adjust based on number of suggestions
            if len(suggestions) >= 3:
                max_confidence += 0.1
            
            # Adjust based on suggestion types
            has_existing = any(s.get('type') == 'existing' for s in suggestions)
            if has_existing:
                max_confidence += 0.1
            
            return min(1.0, max_confidence)
            
        except Exception as e:
            logger.error(f"Category confidence calculation failed: {str(e)}")
            return 0.5
    
    async def batch_suggest_categories(self, tasks: List[Dict[str, Any]], existing_categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Suggest categories for multiple tasks
        """
        try:
            results = []
            
            for task in tasks:
                suggestion_result = await self.suggest_category(task, existing_categories)
                results.append({
                    'task_id': task.get('id'),
                    'task_title': task.get('title'),
                    'suggestions': suggestion_result
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Batch category suggestion failed: {str(e)}")
            return []
    
    async def validate_category_suggestion(self, task: Dict[str, Any], suggested_category: str) -> Dict[str, Any]:
        """
        Validate a category suggestion for a task
        """
        try:
            task_text = f"Title: {task.get('title', '')}\nDescription: {task.get('description', '')}"
            
            prompt = f"""
            Validate if this category is appropriate for the task:
            
            Task: {task_text}
            Suggested Category: {suggested_category}
            
            Evaluate:
            1. How well does the category fit the task?
            2. Are there better alternatives?
            3. What are the pros and cons?
            
            Return as JSON:
            {{
                "is_appropriate": true,
                "fit_score": 0.85,
                "pros": ["pro1", "pro2"],
                "cons": ["con1", "con2"],
                "better_alternatives": ["alt1", "alt2"],
                "recommendation": "use/consider_alternatives/reject"
            }}
            """
            
            result = await self.gemini.generate_structured_response(prompt)
            
            if 'error' in result:
                return {
                    'is_appropriate': True,
                    'fit_score': 0.7,
                    'recommendation': 'use',
                    'error': result['error']
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Category validation failed: {str(e)}")
            return {
                'is_appropriate': True,
                'fit_score': 0.7,
                'recommendation': 'use',
                'error': str(e)
            } 