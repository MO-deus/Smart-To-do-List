"""Category service for handling category-related business logic."""

import logging
from typing import Dict, List, Any, Optional, cast
from django.core.exceptions import ValidationError

from .base_service import BaseService
from todo.models import Category
from todo.serializers import CategorySerializer


class CategoryService(BaseService[Category]):
    """Service class for handling category-related operations."""
    
    def __init__(self):
        super().__init__(Category, CategorySerializer)
    
    def get_categories_by_usage(self, min_usage: int = 0) -> List[Dict[str, Any]]:
        """Retrieve categories filtered by minimum usage frequency."""
        return self.get_all(usage_frequency__gte=min_usage)
    
    def get_most_used_categories(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve the most frequently used categories."""
        try:
            categories = self.model.objects.order_by('-usage_frequency')[:limit]  # type: ignore
            serializer = self.serializer_class(categories, many=True)
            return cast(List[Dict[str, Any]], serializer.data)
        except Exception as e:
            self.logger.error(f"Failed to retrieve most used categories: {str(e)}")
            raise
    
    def increment_usage_frequency(self, category_id: str) -> Optional[Dict[str, Any]]:
        """Increment the usage frequency of a category."""
        try:
            category = self.model.objects.get(id=category_id)  # type: ignore
            category.usage_frequency += 1  # type: ignore
            category.save()
            serializer = self.serializer_class(category)
            return cast(Dict[str, Any], serializer.data)
        except self.model.DoesNotExist:  # type: ignore
            self.logger.warning(f"Category with id {category_id} not found")
            return None
        except Exception as e:
            self.logger.error(f"Failed to increment usage frequency for category {category_id}: {str(e)}")
            raise
    
    def create_category_if_not_exists(self, name: str) -> Dict[str, Any]:
        """Create a category if it doesn't already exist."""
        try:
            category, created = self.model.objects.get_or_create(  # type: ignore
                name=name,
                defaults={'usage_frequency': 1}
            )
            
            if not created:
                category.usage_frequency += 1  # type: ignore
                category.save()
            
            serializer = self.serializer_class(category)
            return cast(Dict[str, Any], serializer.data)
        except Exception as e:
            self.logger.error(f"Failed to create/get category '{name}': {str(e)}")
            raise
    
    def search_categories(self, query: str) -> List[Dict[str, Any]]:
        """Search categories by name."""
        try:
            categories = self.model.objects.filter(name__icontains=query)  # type: ignore
            serializer = self.serializer_class(categories, many=True)
            return cast(List[Dict[str, Any]], serializer.data)
        except Exception as e:
            self.logger.error(f"Failed to search categories: {str(e)}")
            raise
    
    def get_category_statistics(self) -> Dict[str, Any]:
        """Get statistics about categories."""
        try:
            total_categories = self.model.objects.count()  # type: ignore
            used_categories = self.model.objects.filter(usage_frequency__gt=0).count()  # type: ignore
            unused_categories = total_categories - used_categories
            
            top_categories = self.model.objects.order_by('-usage_frequency')[:5]  # type: ignore
            top_categories_data = []
            for category in top_categories:
                top_categories_data.append({
                    'name': category.name,
                    'usage_frequency': category.usage_frequency  # type: ignore
                })
            
            return {
                'total_categories': total_categories,
                'used_categories': used_categories,
                'unused_categories': unused_categories,
                'top_categories': top_categories_data,
                'usage_rate': (used_categories / total_categories * 100) if total_categories > 0 else 0
            }
        except Exception as e:
            self.logger.error(f"Failed to get category statistics: {str(e)}")
            raise
    
    def cleanup_unused_categories(self, min_usage: int = 0) -> int:
        try:
            unused_categories = self.model.objects.filter(usage_frequency__lt=min_usage)  # type: ignore
            count = unused_categories.count()  # type: ignore
            unused_categories.delete()
            
            self.logger.info(f"Deleted {count} unused categories")
            return count
        except Exception as e:
            self.logger.error(f"Failed to cleanup unused categories: {str(e)}")
            raise 