"""Settings management for the application."""

import os
from typing import Any, Optional, Dict
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / '.env')


def get_setting(key: str, default: Any = None, required: bool = False) -> Any:
    value = os.getenv(key, default)
    
    if required and value is None:
        raise ValueError(f"Required setting '{key}' is not configured")
    
    return value


def get_boolean_setting(key: str, default: bool = False) -> bool:
    value = get_setting(key, str(default))
    return str(value).lower() in ('true', '1', 'yes', 'on')


def get_int_setting(key: str, default: int = 0) -> int:
    value = get_setting(key, str(default))
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def get_float_setting(key: str, default: float = 0.0) -> float:
    value = get_setting(key, str(default))
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def get_list_setting(key: str, default: list = None, separator: str = ',') -> list:  # type: ignore
    if default is None:
        default = []
    
    value = get_setting(key, '')
    if not value:
        return default
    
    return [item.strip() for item in value.split(separator) if item.strip()]


def get_dict_setting(key: str, default: dict = None) -> dict:  # type: ignore
    if default is None:
        default = {}
    
    import json
    value = get_setting(key, '')
    if not value:
        return default
    
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return default


# Environment detection
def is_development() -> bool:
    """Check if running in development environment."""
    return get_boolean_setting('DEBUG', True)


def is_production() -> bool:
    """Check if running in production environment."""
    return get_boolean_setting('PRODUCTION', False)


def is_testing() -> bool:
    """Check if running in testing environment."""
    return get_boolean_setting('TESTING', False)


def is_staging() -> bool:
    """Check if running in staging environment."""
    return get_boolean_setting('STAGING', False)


# Database settings
def get_database_config() -> Dict[str, Any]:
    """Get database configuration."""
    return {
        'ENGINE': get_setting('DB_ENGINE', 'django.db.backends.postgresql_psycopg2'),
        'NAME': get_setting('DB_NAME', 'todo_db'),
        'USER': get_setting('DB_USER', 'postgres'),
        'PASSWORD': get_setting('DB_PASSWORD', ''),
        'HOST': get_setting('DB_HOST', 'localhost'),
        'PORT': get_setting('DB_PORT', '5432'),
        'OPTIONS': {
            'connect_timeout': get_int_setting('DB_CONNECT_TIMEOUT', 20),
        }
    }


# AI settings
def get_ai_config() -> Dict[str, Any]:
    """Get AI configuration."""
    return {
        'api_key': get_setting('GEMINI_API_KEY', required=True),
        'model': get_setting('AI_MODEL', 'gemini-2.5-flash'),
        'max_retries': get_int_setting('AI_MAX_RETRIES', 3),
        'temperature': get_float_setting('AI_TEMPERATURE', 0.7),
        'timeout': get_int_setting('AI_TIMEOUT', 30),
        'batch_size': get_int_setting('AI_BATCH_SIZE', 10),
        'rate_limit_delay': get_float_setting('AI_RATE_LIMIT_DELAY', 1.0),
    }


# Security settings
def get_security_config() -> Dict[str, Any]:
    """Get security configuration."""
    return {
        'secret_key': get_setting('SECRET_KEY', required=True),
        'allowed_hosts': get_list_setting('ALLOWED_HOSTS', ['localhost', '127.0.0.1']),
        'csrf_trusted_origins': get_list_setting('CSRF_TRUSTED_ORIGINS', []),
        'cors_allowed_origins': get_list_setting('CORS_ALLOWED_ORIGINS', ['http://localhost:3000']),
        'cors_allowed_credentials': get_boolean_setting('CORS_ALLOWED_CREDENTIALS', True),
    }


# Logging settings
def get_logging_config() -> Dict[str, Any]:
    """Get logging configuration."""
    return {
        'level': get_setting('LOG_LEVEL', 'INFO'),
        'format': get_setting('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
        'file_path': get_setting('LOG_FILE_PATH', 'logs/app.log'),
        'max_size': get_int_setting('LOG_MAX_SIZE', 10 * 1024 * 1024),  # 10MB
        'backup_count': get_int_setting('LOG_BACKUP_COUNT', 5),
        'console_output': get_boolean_setting('LOG_CONSOLE_OUTPUT', True),
        'file_output': get_boolean_setting('LOG_FILE_OUTPUT', True),
    }


# Cache settings
def get_cache_config() -> Dict[str, Any]:
    """Get cache configuration."""
    cache_backend = get_setting('CACHE_BACKEND', 'default')
    
    if cache_backend == 'redis':
        return {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': get_setting('REDIS_URL', 'redis://localhost:6379/1'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    else:
        return {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }


# Email settings
def get_email_config() -> Dict[str, Any]:
    """Get email configuration."""
    return {
        'backend': get_setting('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend'),
        'host': get_setting('EMAIL_HOST', 'localhost'),
        'port': get_int_setting('EMAIL_PORT', 587),
        'username': get_setting('EMAIL_USERNAME', ''),
        'password': get_setting('EMAIL_PASSWORD', ''),
        'use_tls': get_boolean_setting('EMAIL_USE_TLS', True),
        'use_ssl': get_boolean_setting('EMAIL_USE_SSL', False),
        'default_from_email': get_setting('DEFAULT_FROM_EMAIL', 'noreply@example.com'),
    }


# File upload settings
def get_file_upload_config() -> Dict[str, Any]:
    """Get file upload configuration."""
    return {
        'max_size': get_int_setting('FILE_UPLOAD_MAX_SIZE', 10 * 1024 * 1024),  # 10MB
        'allowed_types': get_list_setting('FILE_UPLOAD_ALLOWED_TYPES', ['txt', 'pdf', 'doc', 'docx']),
        'upload_path': get_setting('FILE_UPLOAD_PATH', 'uploads/'),
        'temp_path': get_setting('FILE_TEMP_PATH', 'temp/'),
    }


# Performance settings
def get_performance_config() -> Dict[str, Any]:
    """Get performance configuration."""
    return {
        'cache_enabled': get_boolean_setting('CACHE_ENABLED', True),
        'compression_enabled': get_boolean_setting('COMPRESSION_ENABLED', True),
        'gzip_level': get_int_setting('GZIP_LEVEL', 6),
        'max_concurrent_requests': get_int_setting('MAX_CONCURRENT_REQUESTS', 100),
        'request_timeout': get_int_setting('REQUEST_TIMEOUT', 30),
        'database_pool_size': get_int_setting('DB_POOL_SIZE', 10),
    }


# Validation function
def validate_settings() -> None:
    required_settings = [
        'SECRET_KEY',
        'GEMINI_API_KEY',
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not get_setting(setting):
            missing_settings.append(setting)
    
    if missing_settings:
        raise ValueError(f"Missing required settings: {', '.join(missing_settings)}")


# Configuration validation on import
try:
    validate_settings()
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please check your environment variables and .env file.") 