"""
Application constants and configuration.

This module defines application-wide constants, configuration values,
and enums that are used throughout the application.
"""

from enum import Enum
from typing import Dict, Any


class TaskPriority(Enum):
    """Enumeration for task priority levels."""
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    
    @classmethod
    def choices(cls) -> list:
        """Get choices for Django model field."""
        return [(member.value, member.name.title()) for member in cls]
    
    @classmethod
    def get_label(cls, value: int) -> str:
        """Get human-readable label for priority value."""
        for member in cls:
            if member.value == value:
                return member.name.title()
        return "Unknown"


class TaskStatus(Enum):
    """Enumeration for task status values."""
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    
    @classmethod
    def choices(cls) -> list:
        """Get choices for Django model field."""
        return [(member.value, member.value) for member in cls]
    
    @classmethod
    def values(cls) -> list:
        """Get all status values."""
        return [member.value for member in cls]


class ContextSourceType(Enum):
    """Enumeration for context source types."""
    WHATSAPP = "WhatsApp"
    EMAIL = "Email"
    NOTE = "Note"
    
    @classmethod
    def choices(cls) -> list:
        """Get choices for Django model field."""
        return [(member.value, member.value) for member in cls]
    
    @classmethod
    def values(cls) -> list:
        """Get all source type values."""
        return [member.value for member in cls]


# AI Configuration
AI_CONFIG: Dict[str, Any] = {
    'model': 'gemini-2.5-flash',
    'max_retries': 3,
    'temperature': 0.7,
    'max_tokens': 1000,
    'timeout': 30,
    'batch_size': 10,
    'rate_limit_delay': 1.0,
}

# Database Configuration
DATABASE_CONFIG: Dict[str, Any] = {
    'connection_timeout': 20,
    'pool_size': 10,
    'max_overflow': 20,
    'echo': False,
}

# Logging Configuration
LOGGING_CONFIG: Dict[str, Any] = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S',
    'file_path': 'logs/app.log',
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5,
}

# API Configuration
API_CONFIG: Dict[str, Any] = {
    'default_page_size': 20,
    'max_page_size': 100,
    'rate_limit': 1000,  # requests per hour
    'timeout': 30,
}

# Task Configuration
TASK_CONFIG: Dict[str, Any] = {
    'max_title_length': 200,
    'max_description_length': 2000,
    'default_priority': TaskPriority.MEDIUM.value,
    'default_status': TaskStatus.PENDING.value,
    'overdue_threshold_days': 1,
    'due_soon_threshold_days': 7,
}

# Category Configuration
CATEGORY_CONFIG: Dict[str, Any] = {
    'max_name_length': 100,
    'min_usage_for_popular': 5,
    'cleanup_threshold_days': 30,
    'max_categories_per_task': 1,
}

# Context Configuration
CONTEXT_CONFIG: Dict[str, Any] = {
    'max_content_length': 10000,
    'retention_days': 90,
    'batch_processing_size': 50,
    'insight_processing_delay': 5,  # seconds
}

# Validation Messages
VALIDATION_MESSAGES: Dict[str, str] = {
    'required_field': 'This field is required.',
    'invalid_email': 'Enter a valid email address.',
    'invalid_uuid': 'Enter a valid UUID.',
    'invalid_priority': 'Priority must be 1 (High), 2 (Medium), or 3 (Low).',
    'invalid_status': 'Status must be one of: Pending, In Progress, Completed.',
    'invalid_source_type': 'Source type must be one of: WhatsApp, Email, Note.',
    'past_deadline': 'Deadline cannot be in the past.',
    'invalid_priority_score': 'Priority score must be between 0.0 and 1.0.',
    'duplicate_category': 'A category with this name already exists.',
    'category_not_found': 'Category not found.',
    'task_not_found': 'Task not found.',
    'context_not_found': 'Context entry not found.',
}

# Error Messages
ERROR_MESSAGES: Dict[str, str] = {
    'ai_service_unavailable': 'AI services are not available. Please check configuration.',
    'ai_processing_failed': 'AI processing failed. Please try again.',
    'database_connection_failed': 'Database connection failed.',
    'validation_error': 'Validation error occurred.',
    'permission_denied': 'Permission denied.',
    'resource_not_found': 'Resource not found.',
    'internal_server_error': 'Internal server error occurred.',
    'rate_limit_exceeded': 'Rate limit exceeded. Please try again later.',
    'timeout_error': 'Request timed out.',
}

# Success Messages
SUCCESS_MESSAGES: Dict[str, str] = {
    'task_created': 'Task created successfully.',
    'task_updated': 'Task updated successfully.',
    'task_deleted': 'Task deleted successfully.',
    'category_created': 'Category created successfully.',
    'category_updated': 'Category updated successfully.',
    'category_deleted': 'Category deleted successfully.',
    'context_created': 'Context entry created successfully.',
    'context_updated': 'Context entry updated successfully.',
    'context_deleted': 'Context entry deleted successfully.',
    'ai_processing_completed': 'AI processing completed successfully.',
}

# HTTP Status Codes
HTTP_STATUS: Dict[str, int] = {
    'OK': 200,
    'CREATED': 201,
    'NO_CONTENT': 204,
    'BAD_REQUEST': 400,
    'UNAUTHORIZED': 401,
    'FORBIDDEN': 403,
    'NOT_FOUND': 404,
    'METHOD_NOT_ALLOWED': 405,
    'CONFLICT': 409,
    'UNPROCESSABLE_ENTITY': 422,
    'INTERNAL_SERVER_ERROR': 500,
    'SERVICE_UNAVAILABLE': 503,
}

# Cache Keys
CACHE_KEYS: Dict[str, str] = {
    'task_list': 'tasks:list',
    'task_detail': 'tasks:detail:{id}',
    'category_list': 'categories:list',
    'category_detail': 'categories:detail:{id}',
    'context_list': 'context:list',
    'context_detail': 'context:detail:{id}',
    'ai_health': 'ai:health',
    'statistics': 'stats:all',
}

# Cache Timeouts (in seconds)
CACHE_TIMEOUTS: Dict[str, int] = {
    'short': 300,      # 5 minutes
    'medium': 1800,    # 30 minutes
    'long': 3600,      # 1 hour
    'very_long': 86400, # 24 hours
}

# File Upload Configuration
FILE_UPLOAD_CONFIG: Dict[str, Any] = {
    'max_size': 10 * 1024 * 1024,  # 10MB
    'allowed_types': ['txt', 'pdf', 'doc', 'docx'],
    'upload_path': 'uploads/',
    'temp_path': 'temp/',
}

# Security Configuration
SECURITY_CONFIG: Dict[str, Any] = {
    'password_min_length': 8,
    'password_require_special': True,
    'session_timeout': 3600,  # 1 hour
    'max_login_attempts': 5,
    'lockout_duration': 900,  # 15 minutes
    'csrf_timeout': 31449600,  # 1 year
}

# Performance Configuration
PERFORMANCE_CONFIG: Dict[str, Any] = {
    'database_pool_size': 10,
    'cache_enabled': True,
    'compression_enabled': True,
    'gzip_level': 6,
    'max_concurrent_requests': 100,
    'request_timeout': 30,
} 