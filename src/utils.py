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
            # For platforms that support /proc/uptime
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                return str(timedelta(seconds=uptime_seconds))
        except:
            # Fallback for other platforms
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
                'percentage': round(memory.percent, 2)
            }
        except ImportError:
            return {'error': 'psutil not available'}
    
    @staticmethod
    def get_cpu_usage() -> Dict[str, Any]:
        """Get CPU usage information"""
        try:
            import psutil
            return {
                'percent': round(psutil.cpu_percent(interval=1), 2),
                'cores': psutil.cpu_count(),
                'load_average': [round(x, 2) for x in os.getloadavg()] if hasattr(os, 'getloadavg') else []
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
            if self.failed_attempts[ip_address]:
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
            del self.failed_attempts[ip_address]
        if ip_address in self.blocked_ips:
            self.blocked_ips.remove(ip_address)
    
    def get_security_events(self) -> List[Dict[str, Any]]:
        """Get recent security events"""
        events = []
        for ip, attempts in self.failed_attempts.items():
            if attempts:
                events.append({
                    'type': 'failed_attempts',
                    'ip_address': ip,
                    'attempts': len(attempts),
                    'last_attempt': max(attempts).isoformat(),
                    'blocked': ip in self.blocked_ips
                })
        return events

class CacheManager:
    """Advanced caching system with TTL support"""
    
    def __init__(self):
        self._cache = {}
        self._lock = threading.RLock()
    
    def get(self, key: str) -> Any:
        """Get value from cache"""
        with self._lock:
            if key in self._cache:
                value, expiry = self._cache[key]
                if expiry is None or expiry > time.time():
                    return value
                else:
                    del self._cache[key]
            return None
    
    def set(self, key: str, value: Any, timeout: int = 300) -> None:
        """Set value in cache with timeout"""
        with self._lock:
            expiry = time.time() + timeout if timeout else None
            self._cache[key] = (value, expiry)
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear all cache"""
        with self._lock:
            self._cache.clear()

class DataProcessor:
    """Advanced data processing and analysis"""
    
    def __init__(self):
        self.cache = CacheManager()
    
    def analyze_text(self, text: str) -> AnalysisResult:
        """Comprehensive text analysis"""
        start_time = time.time()
        
        if not text or not isinstance(text, str):
            return AnalysisResult(
                success=False,
                data={},
                metrics={},
                warnings=['Invalid input text'],
                recommendations=['Provide valid text for analysis'],
                processing_time=0
            )
        
        # Basic text statistics
        words = re.findall(r'\b\w+\b', text.lower())
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        char_count = len(text)
        word_count = len(words)
        sentence_count = len(sentences)
        unique_words = len(set(words))
        
        # Advanced metrics
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Readability score (simplified)
        readability = max(0, min(100, 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (avg_word_length / word_count))) if sentence_count > 0 and word_count > 0 else 0
        
        # Sentiment analysis (basic)
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'positive', 'happy']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointing', 'negative', '
