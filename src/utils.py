import os
import logging
import hashlib
import json
import time
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Union
from collections import defaultdict, Counter
import statistics
import math
from functools import wraps
from dataclasses import dataclass
from enum import Enum
import threading
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class AnalysisResult:
    """Comprehensive analysis result container"""
    success: bool
    data: Dict[str, Any]
    metrics: Dict[str, float]
    warnings: List[str]
    recommendations: List[str]
    processing_time: float

class AdvancedUtils:
    """Advanced utility functions for various operations"""
    
    @staticmethod
    def generate_hash(data: str, algorithm: str = 'sha256') -> str:
        """Generate hash for given data"""
        hash_func = getattr(hashlib, algorithm, hashlib.sha256)
        return hash_func(data.encode()).hexdigest()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Comprehensive email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """International phone number validation"""
        pattern = r'^\+?[1-9]\d{1,14}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human-readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
    
    @staticmethod
    def get_system_uptime() -> str:
        """Get system uptime information"""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                return str(timedelta(seconds=uptime_seconds))
        except:
            return "Unknown"
    
    @staticmethod
    def get_memory_usage() -> Dict[str, Any]:
        """Get system memory usage"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return {
                'total': AdvancedUtils.format_file_size(memory.total),
                'available': AdvancedUtils.format_file_size(memory.available),
                'used': AdvancedUtils.format_file_size(memory.used),
                'percentage': memory.percent
            }
        except ImportError:
            return {'error': 'psutil not available'}
    
    @staticmethod
    def get_cpu_usage() -> Dict[str, Any]:
        """Get CPU usage information"""
        try:
            import psutil
            return {
                'percent': psutil.cpu_percent(interval=1),
                'cores': psutil.cpu_count(),
                'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else []
            }
        except ImportError:
            return {'error': 'psutil not available'}
    
    @staticmethod
    def get_performance_metrics() -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        return {
            'timestamp': datetime.now().isoformat(),
            'memory': AdvancedUtils.get_memory_usage(),
            'cpu': AdvancedUtils.get_cpu_usage(),
            'uptime': AdvancedUtils.get_system_uptime(),
            'active_threads': threading.active_count(),
            'python_version': os.sys.version
        }
    
    @staticmethod
    def compress_data(data: str) -> bytes:
        """Compress string data"""
        import zlib
        return zlib.compress(data.encode())
    
    @staticmethod
    def decompress_data(compressed_data: bytes) -> str:
        """Decompress data to string"""
        import zlib
        return zlib.decompress(compressed_data).decode()
    
    @staticmethod
    def create_backup(file_path: str, backup_dir: str = "backups") -> str:
        """Create backup of a file with timestamp"""
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(
            backup_dir, 
            f"{os.path.basename(file_path)}_{timestamp}.bak"
        )
        
        import shutil
        shutil.copy2(file_path, backup_file)
        return backup_file

class SecurityManager:
    """Advanced security management with threat detection"""
    
    def __init__(self):
        self.failed_attempts = defaultdict(list)
        self.blocked_ips = set()
        self.suspicious_patterns = [
            r".*(\bselect\b|\binsert\b|\bupdate\b|\bdelete\b|\bdrop\b).*",
            r".*(<script>|javascript:).*",
            r".*(\.\./|\.\.\\).*",
            r".*(union.*select).*",
        ]
    
    def is_valid_username(self, username: str) -> bool:
        """Validate username against security rules"""
        if len(username) < 3 or len(username) > 50:
            return False
        
        # Only allow alphanumeric and some special characters
        if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
            return False
        
        # Prevent common vulnerable usernames
        blocked_usernames = ['admin', 'root', 'system', 'administrator']
        if username.lower() in blocked_usernames:
            return False
        
        return True
    
    def is_valid_email(self, email: str) -> bool:
        """Enhanced email validation"""
        return AdvancedUtils.validate_email(email)
    
    def is_strong_password(self, password: str) -> bool:
        """Check password strength"""
        if len(password) < 8:
            return False
        
        checks = [
            any(c.islower() for c in password),  # lowercase
            any(c.isupper() for c in password),  # uppercase  
            any(c.isdigit() for c in password),  # digit
            any(not c.isalnum() for c in password)  # special char
        ]
        
        return all(checks)
    
    def detect_sql_injection(self, input_string: str) -> bool:
        """Detect potential SQL injection attempts"""
        input_lower = input_string.lower()
        for pattern in self.suspicious_patterns:
            if re.match(pattern, input_lower, re.IGNORECASE):
                return True
        return False
    
    def detect_xss(self, input_string: str) -> bool:
        """Detect potential XSS attempts"""
        xss_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe.*?>',
            r'<object.*?>'
        ]
        
        for pattern in xss_patterns:
            if re.search(pattern, input_string, re.IGNORECASE):
                return True
        return False
    
    def record_failed_attempt(self, ip_address: str, max_attempts: int = 5, 
                            window_minutes: int = 15):
        """Record failed login attempt and block if threshold exceeded"""
        now = datetime.now()
        self.failed_attempts[ip_address].append(now)
        
        # Remove attempts outside the time window
        cutoff = now - timedelta(minutes=window_minutes)
        self.failed_attempts[ip_address] = [
            attempt for attempt in self.failed_attempts[ip_address] 
            if attempt > cutoff
        ]
        
        # Block IP if too many attempts
        if len(self.failed_attempts[ip_address]) >= max_attempts:
            self.blocked_ips.add(ip_address)
            logger.warning(f"IP address blocked: {ip_address}")
    
    def is_ip_blocked(self, ip_address: str) -> bool:
        """Check if IP address is currently blocked"""
        if ip_address in self.blocked_ips:
            # Check if block should be lifted (1 hour block)
            block_time = min(self.failed_attempts[ip_address])
            if datetime.now() - block_time > timedelta(hours=1):
                self.blocked_ips.remove(ip_address)
                self.failed_attempts[ip_address].clear()
                return False
            return True
        return False
    
    def clear_failed_attempts(self, ip_address: str):
        """Clear failed attempts for IP address (successful login)"""
        if ip_address in self.failed_attempts:
            del self.failed_attempts[ip
