"""
Cogitara IA - Advanced AI Application
"""

__version__ = "2.0.0"
__author__ = "Cogitara Development Team"

# Importações principais para facilitar o acesso
from .app import create_app
from .database import DatabaseManager
from .utils import AdvancedUtils, SecurityManager, CacheManager, DataProcessor

__all__ = ['create_app', 'DatabaseManager', 'AdvancedUtils', 'SecurityManager', 'CacheManager', 'DataProcessor']
