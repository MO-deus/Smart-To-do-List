"""
Configuration package for centralized application settings.

This package provides a centralized way to manage all application
configuration, including environment variables, settings, and constants.
"""

from .settings import *
from .constants import *

__all__ = [
    'get_setting',
    'is_development',
    'is_production',
    'is_testing',
    'AI_CONFIG',
    'DATABASE_CONFIG',
    'LOGGING_CONFIG'
] 