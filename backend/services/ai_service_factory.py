"""Optimized AI Service Factory for managing consolidated AI service instances."""

import logging
from typing import Optional, Dict, Any
from django.conf import settings

from ai_service import (
    GeminiAIService,
    AIPipelineController
)
from ai_service.consolidated_ai_service import ConsolidatedAIService

logger = logging.getLogger(__name__)


class AIServiceFactory:
    """Optimized factory class for managing consolidated AI service instances."""
    
    _instance = None
    _gemini_client: Optional[GeminiAIService] = None
    _ai_pipeline: Optional[AIPipelineController] = None
    _consolidated_ai: Optional[ConsolidatedAIService] = None
    _services_available: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIServiceFactory, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialize_services()
            self._initialized = True
    
    def _initialize_services(self) -> None:
        """Initialize consolidated AI services."""
        try:
            if not getattr(settings, 'GEMINI_API_KEY', None):
                logger.warning("GEMINI_API_KEY not configured. AI services will be unavailable.")
                self._services_available = False
                return
            
            self._gemini_client = GeminiAIService()
            self._consolidated_ai = ConsolidatedAIService(self._gemini_client)
            self._ai_pipeline = AIPipelineController(self._gemini_client)
            
            self._services_available = True
            logger.info("Optimized AI services initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI services: {str(e)}")
            self._services_available = False
            self._gemini_client = None
            self._ai_pipeline = None
            self._consolidated_ai = None
    
    @property
    def services_available(self) -> bool:
        """Check if AI services are available."""
        return self._services_available
    
    def get_gemini_client(self) -> Optional[GeminiAIService]:
        """Get the Gemini AI client instance."""
        return self._gemini_client
    
    def get_ai_pipeline(self) -> Optional[AIPipelineController]:
        """Get the optimized AI pipeline controller instance."""
        return self._ai_pipeline
    
    def get_consolidated_ai(self) -> Optional[ConsolidatedAIService]:
        """Get the consolidated AI service instance."""
        return self._consolidated_ai
    
    def health_check(self) -> Dict[str, Any]:
        """Perform a health check on all AI services."""
        health_status = {
            'services_available': self._services_available,
            'gemini_client': self._gemini_client is not None,
            'ai_pipeline': self._ai_pipeline is not None,
            'consolidated_ai': self._consolidated_ai is not None
        }
        
        if self._consolidated_ai:
            try:
                health_status['consolidated_ai_health'] = True
            except Exception as e:
                logger.error(f"Consolidated AI health check failed: {str(e)}")
                health_status['consolidated_ai_health'] = False
        
        return health_status
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current AI model and available options."""
        if self._gemini_client:
            return self._gemini_client.get_model_info()
        else:
            return {
                "error": "AI services not available",
                "current_model": "unknown",
                "available_models": {}
            }
    
    def reset_services(self) -> None:
        """Reset all AI services and reinitialize them."""
        logger.info("Resetting AI services")
        self._gemini_client = None
        self._ai_pipeline = None
        self._consolidated_ai = None
        self._services_available = False
        
        self._initialize_services() 