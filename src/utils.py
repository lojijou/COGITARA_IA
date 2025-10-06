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
    
    def cleanup_expired(self) -> None:
        """Clean up expired cache entries"""
        with self._lock:
            current_time = time.time()
            expired_keys = [
                key for key, (_, expiry) in self._cache.items()
                if expiry and expiry <= current_time
            ]
            for key in expired_keys:
                del self._cache[key]

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
        words = text.split()
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
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointing']
        
        positive_count = sum(1 for word in words if word.lower() in positive_words)
        negative_count = sum(1 for word in words if word.lower() in negative_words)
        
        sentiment_score = (positive_count - negative_count) / word_count if word_count > 0 else 0
        
        processing_time = time.time() - start_time
        
        return AnalysisResult(
            success=True,
            data={
                'basic_stats': {
                    'characters': char_count,
                    'words': word_count,
                    'sentences': sentence_count,
                    'unique_words': unique_words
                },
                'advanced_metrics': {
                    'average_word_length': round(avg_word_length, 2),
                    'average_sentence_length': round(avg_sentence_length, 2),
                    'readability_score': round(readability, 2),
                    'sentiment_score': round(sentiment_score, 4)
                },
                'word_frequency': dict(Counter(words).most_common(10))
            },
            metrics={
                'processing_time': processing_time,
                'complexity_score': (unique_words / word_count) if word_count > 0 else 0
            },
            warnings=[] if word_count > 10 else ['Text is very short for meaningful analysis'],
            recommendations=[
                'Consider longer text for more accurate analysis',
                'Review word frequency for key themes'
            ],
            processing_time=processing_time
        )
    
    def analyze_numeric_data(self, data: List[float]) -> AnalysisResult:
        """Comprehensive numeric data analysis"""
        start_time = time.time()
        
        if not data or not isinstance(data, list):
            return AnalysisResult(
                success=False,
                data={},
                metrics={},
                warnings=['Invalid numeric data'],
                recommendations=['Provide valid numeric list for analysis'],
                processing_time=0
            )
        
        try:
            # Basic statistics
            data_clean = [float(x) for x in data if x is not None]
            
            if not data_clean:
                return AnalysisResult(
                    success=False,
                    data={},
                    metrics={},
                    warnings=['No valid numeric data found'],
                    recommendations=['Check data quality'],
                    processing_time=0
                )
            
            n = len(data_clean)
            mean = statistics.mean(data_clean)
            median = statistics.median(data_clean)
            stdev = statistics.stdev(data_clean) if n > 1 else 0
            variance = statistics.variance(data_clean) if n > 1 else 0
            data_min = min(data_clean)
            data_max = max(data_clean)
            data_range = data_max - data_min
            
            # Advanced statistics
            try:
                mode = statistics.mode(data_clean)
            except:
                mode = None
            
            q1 = statistics.quantiles(data_clean, n=4)[0] if n >= 4 else median
            q3 = statistics.quantiles(data_clean, n=4)[2] if n >= 4 else median
            iqr = q3 - q1
            
            # Detect outliers
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = [x for x in data_clean if x < lower_bound or x > upper_bound]
            
            processing_time = time.time() - start_time
            
            return AnalysisResult(
                success=True,
                data={
                    'descriptive_stats': {
                        'count': n,
                        'mean': round(mean, 4),
                        'median': round(median, 4),
                        'mode': mode,
                        'standard_deviation': round(stdev, 4),
                        'variance': round(variance, 4),
                        'range': round(data_range, 4),
                        'min': round(data_min, 4),
                        'max': round(data_max, 4)
                    },
                    'distribution': {
                        'q1': round(q1, 4),
                        'q3': round(q3, 4),
                        'iqr': round(iqr, 4),
                        'outliers_count': len(outliers),
                        'outliers': [round(x, 4) for x in outliers]
                    }
                },
                metrics={
                    'processing_time': processing_time,
                    'data_quality_score': 1.0 - (len(outliers) / n) if n > 0 else 0,
                    'variability_coefficient': stdev / mean if mean != 0 else 0
                },
                warnings=['Outliers detected'] if outliers else [],
                recommendations=[
                    'Consider removing outliers for certain analyses',
                    'Check data distribution for normality'
                ],
                processing_time=processing_time
            )
            
        except Exception as e:
            return AnalysisResult(
                success=False,
                data={},
                metrics={},
                warnings=[f'Analysis error: {str(e)}'],
                recommendations=['Verify data format and quality'],
                processing_time=time.time() - start_time
            )
    
    def detect_patterns(self, data: Any) -> AnalysisResult:
        """Pattern detection in various data types"""
        start_time = time.time()
        
        if isinstance(data, str):
            # Text pattern detection
            patterns = {
                'emails': re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data),
                'urls': re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data),
                'phone_numbers': re.findall(r'\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}', data),
                'dates': re.findall(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b', data)
            }
            
            result_data = {
                'pattern_type': 'text',
                'detected_patterns': {k: len(v) for k, v in patterns.items()},
                'details': patterns
            }
            
        elif isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
            # Numeric pattern detection
            if len(data) < 3:
                return AnalysisResult(
                    success=False,
                    data={},
                    metrics={},
                    warnings=['Insufficient data for pattern detection'],
                    recommendations=['Provide at least 3 data points'],
                    processing_time=time.time() - start_time
                )
            
            # Check for trends
            differences = [data[i] - data[i-1] for i in range(1, len(data))]
            is_increasing = all(diff >= 0 for diff in differences)
            is_decreasing = all(diff <= 0 for diff in differences)
            
            # Check for periodicity (simple)
            autocorr = self._calculate_autocorrelation(data)
            
            result_data = {
                'pattern_type': 'numeric',
                'trend': 'increasing' if is_increasing else 'decreasing' if is_decreasing else 'mixed',
                'volatility': statistics.stdev(data) if len(data) > 1 else 0,
                'autocorrelation': autocorr,
                'seasonality_detected': any(abs(corr) > 0.5 for corr in autocorr[:min(5, len(autocorr))])
            }
            
        else:
            return AnalysisResult(
                success=False,
                data={},
                metrics={},
                warnings=['Unsupported data type for pattern detection'],
                recommendations=['Provide text or numeric data'],
                processing_time=time.time() - start_time
            )
        
        processing_time = time.time() - start_time
        
        return AnalysisResult(
            success=True,
            data=result_data,
            metrics={'processing_time': processing_time},
            warnings=[],
            recommendations=['Review detected patterns for insights'],
            processing_time=processing_time
        )
    
    def _calculate_autocorrelation(self, data: List[float], max_lag: int = 5) -> List[float]:
        """Calculate autocorrelation for time series data"""
        n = len(data)
        if n <= 1:
            return []
        
        mean = statistics.mean(data)
        variance = statistics.variance(data) if n > 1 else 0
        
        autocorrs = []
        for lag in range(1, min(max_lag + 1, n)):
            covariance = sum(
                (data[i] - mean) * (data[i - lag] - mean) 
                for i in range(lag, n)
            ) / n
            
            autocorr = covariance / variance if variance != 0 else 0
            autocorrs.append(autocorr)
        
        return autocorrs
    
    def comprehensive_analysis(self, data: Any) -> AnalysisResult:
        """Comprehensive analysis combining multiple techniques"""
        start_time = time.time()
        
        analyses = []
        
        if isinstance(data, str):
            analyses.append(self.analyze_text(data))
            analyses.append(self.detect_patterns(data))
        elif isinstance(data, list):
            if all(isinstance(x, (int, float)) for x in data):
                analyses.append(self.analyze_numeric_data(data))
                analyses.append(self.detect_patterns(data))
            elif all(isinstance(x, str) for x in data):
                combined_text = ' '.join(data)
                analyses.append(self.analyze_text(combined_text))
        
        if not analyses:
            return AnalysisResult(
                success=False,
                data={},
                metrics={},
                warnings=['No suitable analysis method found for data type'],
                recommendations=['Provide text, numeric data, or list of strings'],
                processing_time=time.time() - start_time
            )
        
        # Combine results
        combined_data = {}
        combined_metrics = {'total_processing_time': time.time() - start_time}
        all_warnings = []
        all_recommendations = []
        
        for i, analysis in enumerate(analyses):
            if analysis.success:
                combined_data[f'analysis_{i+1}'] = analysis.data
                combined_metrics.update(analysis.metrics)
                all_warnings.extend(analysis.warnings)
                all_recommendations.extend(analysis.recommendations)
        
        return AnalysisResult(
            success=True,
            data=combined_data,
            metrics=combined_metrics,
            warnings=list(set(all_warnings)),
            recommendations=list(set(all_recommendations)),
            processing_time=time.time() - start_time
        )
    
    def analyze_user_behavior(self, user_id: int) -> Dict[str, Any]:
        """Analyze user behavior patterns"""
        # This would typically integrate with database
        # For now, return mock analysis
        return {
            'activity_level': 'high',
            'preferred_analysis_type': 'text',
            'productivity_score': 85,
            'engagement_trend': 'increasing',
            'recommendations': [
                'Try numeric analysis for varied insights',
                'Explore pattern detection features'
            ]
        }
    
    def get_file_processor(self, file_type: str):
        """Get appropriate file processor"""
        processors = {
            'txt': TextFileProcessor(),
            'csv': CSVFileProcessor(),
            'json': JSONFileProcessor()
        }
        return processors.get(file_type)

class TextFileProcessor:
    """Processor for text files"""
    
    def process(self, file_stream)
