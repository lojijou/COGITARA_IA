"""
Advanced Python Application Package
A comprehensive web application with advanced features
"""

__version__ = "2.0.0"
__author__ = "Advanced Development Team"
__description__ = "A sophisticated web application with AI capabilities"

from .app import create_app
from .database import DatabaseManager
from .utils import AdvancedUtils, SecurityManager, CacheManager

__all__ = [
    'create_app',
    'DatabaseManager', 
    'AdvancedUtils',
    'SecurityManager',
    'CacheManager'
]
