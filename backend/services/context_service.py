"""Context service for handling context entry-related business logic."""

import logging
from typing import Dict, List, Any, Optional, cast
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.exceptions import ValidationError

from .base_service import BaseService
from todo.models import ContextEntry
from todo.serializers import ContextEntrySerializer


class ContextService(BaseService[ContextEntry]):
    """Service for context entry operations."""
    
    def __init__(self):
        super().__init__(ContextEntry, ContextEntrySerializer)
    
    def get_context_by_source_type(self, source_type: str) -> List[Dict[str, Any]]:
        valid_source_types = ['WhatsApp', 'Email', 'Note']
        if source_type not in valid_source_types:
            raise ValidationError(f"Invalid source_type. Must be one of: {valid_source_types}")
        return self.get_all(source_type=source_type)
    
    def get_recent_context(self, days: int = 7) -> List[Dict[str, Any]]:
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_context = self.model.objects.filter(created_at__gte=cutoff_date)  # type: ignore
            serializer = self.serializer_class(recent_context, many=True)
            return cast(List[Dict[str, Any]], serializer.data)
        except Exception as e:
            self.logger.error(f"Failed to retrieve recent context: {str(e)}")
            raise
    
    def search_context(self, query: str) -> List[Dict[str, Any]]:
        try:
            context_entries = self.model.objects.filter(content__icontains=query)  # type: ignore
            serializer = self.serializer_class(context_entries, many=True)
            return cast(List[Dict[str, Any]], serializer.data)
        except Exception as e:
            self.logger.error(f"Failed to search context: {str(e)}")
            raise
    
    def get_context_with_insights(self) -> List[Dict[str, Any]]:
        return self.get_all(processed_insights__isnull=False)
    
    def update_processed_insights(self, context_id: str, insights: str) -> Optional[Dict[str, Any]]:
        return self.update(context_id, {'processed_insights': insights})
    
    def get_context_statistics(self) -> Dict[str, Any]:
        try:
            total_entries = self.model.objects.count()  # type: ignore
            whatsapp_entries = self.model.objects.filter(source_type='WhatsApp').count()  # type: ignore
            email_entries = self.model.objects.filter(source_type='Email').count()  # type: ignore
            note_entries = self.model.objects.filter(source_type='Note').count()  # type: ignore
            entries_with_insights = self.model.objects.filter(processed_insights__isnull=False).count()  # type: ignore
            
            # Get entries from last 30 days
            thirty_days_ago = datetime.now() - timedelta(days=30)
            recent_entries = self.model.objects.filter(created_at__gte=thirty_days_ago).count()  # type: ignore
            
            return {
                'total_entries': total_entries,
                'whatsapp_entries': whatsapp_entries,
                'email_entries': email_entries,
                'note_entries': note_entries,
                'entries_with_insights': entries_with_insights,
                'recent_entries_30_days': recent_entries,
                'insights_rate': (entries_with_insights / total_entries * 100) if total_entries > 0 else 0
            }
        except Exception as e:
            self.logger.error(f"Failed to get context statistics: {str(e)}")
            raise
    
    def cleanup_old_context(self, days: int = 90) -> int:
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            old_entries = self.model.objects.filter(created_at__lt=cutoff_date)  # type: ignore
            count = old_entries.count()  # type: ignore
            old_entries.delete()
            
            self.logger.info(f"Deleted {count} old context entries")
            return count
        except Exception as e:
            self.logger.error(f"Failed to cleanup old context: {str(e)}")
            raise
    
    def get_context_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        try:
            context_entries = self.model.objects.filter(
                created_at__gte=start_date,
                created_at__lte=end_date
            ).order_by('created_at')  # type: ignore
            
            serializer = self.serializer_class(context_entries, many=True)
            return cast(List[Dict[str, Any]], serializer.data)
        except Exception as e:
            self.logger.error(f"Failed to retrieve context by date range: {str(e)}")
            raise 