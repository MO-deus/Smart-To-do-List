"""Base service class providing common functionality for all service classes."""

import logging
from typing import Any, Dict, List, Optional, TypeVar, Generic, cast
from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=models.Model)


class BaseService(Generic[T]):
    """Base service class providing common CRUD operations and error handling."""
    
    def __init__(self, model: type[T], serializer_class: type[serializers.ModelSerializer]):
        self.model = model
        self.serializer_class = serializer_class
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def get_all(self, **filters) -> List[Dict[str, Any]]:
        """Retrieve all objects with optional filtering."""
        try:
            queryset = self.model.objects.filter(**filters)  # type: ignore
            serializer = self.serializer_class(queryset, many=True)
            return cast(List[Dict[str, Any]], serializer.data)
        except Exception as e:
            self.logger.error(f"Failed to retrieve {self.model.__name__} objects: {str(e)}")
            raise
    
    def get_by_id(self, object_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single object by its ID."""
        try:
            obj = self.model.objects.get(id=object_id)  # type: ignore
            serializer = self.serializer_class(obj)
            return cast(Dict[str, Any], serializer.data)
        except ObjectDoesNotExist:
            self.logger.warning(f"{self.model.__name__} with id {object_id} not found")
            return None
        except Exception as e:
            self.logger.error(f"Failed to retrieve {self.model.__name__} with id {object_id}: {str(e)}")
            raise
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new object."""
        try:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                obj = serializer.save()
                self.logger.info(f"Created {self.model.__name__} with id {obj.id}")  # type: ignore
                return cast(Dict[str, Any], serializer.data)
            else:
                self.logger.error(f"Validation failed for {self.model.__name__}: {serializer.errors}")
                raise ValidationError(serializer.errors)
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to create {self.model.__name__}: {str(e)}")
            raise
    
    def update(self, object_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing object."""
        try:
            obj = self.model.objects.get(id=object_id)  # type: ignore
            serializer = self.serializer_class(obj, data=data, partial=True)
            if serializer.is_valid():
                updated_obj = serializer.save()
                self.logger.info(f"Updated {self.model.__name__} with id {object_id}")
                return cast(Dict[str, Any], serializer.data)
            else:
                self.logger.error(f"Validation failed for {self.model.__name__} update: {serializer.errors}")
                raise ValidationError(serializer.errors)
        except ObjectDoesNotExist:
            self.logger.warning(f"{self.model.__name__} with id {object_id} not found for update")
            return None
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to update {self.model.__name__} with id {object_id}: {str(e)}")
            raise
    
    def delete(self, object_id: str) -> bool:
        """Delete an object by its ID."""
        try:
            obj = self.model.objects.get(id=object_id)  # type: ignore
            obj.delete()
            self.logger.info(f"Deleted {self.model.__name__} with id {object_id}")
            return True
        except ObjectDoesNotExist:
            self.logger.warning(f"{self.model.__name__} with id {object_id} not found for deletion")
            return False
        except Exception as e:
            self.logger.error(f"Failed to delete {self.model.__name__} with id {object_id}: {str(e)}")
            raise
    
    def exists(self, object_id: str) -> bool:
        """Check if an object exists by its ID."""
        return self.model.objects.filter(id=object_id).exists()  # type: ignore
    
    def count(self, **filters) -> int:
        """Get the count of objects with optional filtering."""
        try:
            return self.model.objects.filter(**filters).count()  # type: ignore
        except Exception as e:
            self.logger.error(f"Failed to count {self.model.__name__} objects: {str(e)}")
            raise 