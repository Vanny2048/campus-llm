"""
LMU Campus LLM - Source Package
A student-centered AI assistant for Loyola Marymount University
"""

__version__ = "1.0.0"
__author__ = "Vanessa Akaraiwe"
__description__ = "Campus LLM for LMU students, faculty, and staff"

# Import main classes for easy access
from .llm_handler import LLMHandler
from .rag_system import RAGSystem
from .points_system import PointsSystem
from .data_collector import LMUDataCollector

__all__ = [
    "LLMHandler",
    "RAGSystem", 
    "PointsSystem",
    "LMUDataCollector"
]