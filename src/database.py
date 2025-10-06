import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import json
import threading
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Advanced database management with connection pooling"""
    
    def __init__(self, db_path: str = "app_database.db"):
        self.db_path = db_path
        self._local = threading.local()
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get thread-local database connection"""
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(
                self.db_path, 
                check_same_thread=False
            )
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection
    
    @contextmanager
    def transaction(self):
        """Context manager for database transactions"""
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction failed: {e}")
            raise
    
    def init_database(self):
        """Initialize database with all required tables"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'user',
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                profile_data TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                activity_type VARCHAR(50),
                description TEXT,
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS processing_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                filename VARCHAR(255),
                file_type VARCHAR(20),
                result_data TEXT,
                processing_time INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level VARCHAR(20),
                module VARCHAR(100),
                message TEXT,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS user_notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title VARCHAR(255),
                message TEXT,
                notification_type VARCHAR(50),
                is_read BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
        ]
        
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
            "CREATE INDEX IF NOT EXISTS idx_activity_user_time ON activity_logs(user_id, created_at)",
            "CREATE INDEX IF NOT EXISTS idx_notifications_user ON user_notifications(user_id, is_read)"
        ]
        
        with self.transaction() as conn:
            for table_sql in tables:
                conn.execute(table_sql)
            for index_sql in indexes:
                conn.execute(index_sql)
            
            # Create default admin user if not exists
            from werkzeug.security import generate_password_hash
            admin_hash = generate_password_hash('admin123')
            try:
                conn.execute(
                    "INSERT OR IGNORE INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                    ('admin', 'admin@cogitara.com', admin_hash, 'admin')
                )
            except:
                pass
    
    def create_user(self, username: str, email: str, password: str) -> Optional[int]:
        """Create a new user with hashed password"""
        from werkzeug.security import generate_password_hash
        
        password_hash = generate_password_hash(password)
        profile_data = json.dumps({
            'registration_ip': '127.0.0.1',
            'preferences': {},
            'statistics': {'logins': 0, 'files_processed': 0}
        })
        
        try:
            with self.transaction() as conn:
                cursor = conn.execute("""
                    INSERT INTO users (username, email, password_hash, profile_data)
                    VALUES (?, ?, ?, ?)
                """, (username, email, password_hash, profile_data))
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            logger.warning(f"User creation failed - username or email exists: {username}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return user data if successful"""
        from werkzeug.security import check_password_hash
        
        try:
            with self.transaction() as conn:
                user = conn.execute("""
                    SELECT id, username, email, password_hash, role, is_active, 
                           last_login, profile_data
                    FROM users 
                    WHERE username = ? AND is_active = 1
                """, (username,)).fetchone()
                
                if user and check_password_hash(user['password_hash'], password):
                    # Update last login
                    conn.execute(
                        "UPDATE users SET last_login = ? WHERE id = ?",
                        (datetime.now(), user['id'])
                    )
                    
                    # Update login count in profile
                    profile = json.loads(user['profile_data'])
                    profile['statistics']['logins'] = profile['statistics'].get('logins', 0) + 1
                    
                    conn.execute(
                        "UPDATE users SET profile_data = ? WHERE id = ?",
                        (json.dumps(profile), user['id'])
                    )
                    
                    return dict(user)
                return None
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None
    
    def username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        with self.transaction() as conn:
            result = conn.execute(
                "SELECT 1 FROM users WHERE username = ?", 
                (username,)
            ).fetchone()
            return result is not None
    
    def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        with self.transaction() as conn:
            result = conn.execute(
                "SELECT 1 FROM users WHERE email = ?", 
                (email,)
            ).fetchone()
            return result is not None
    
    def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive user profile"""
        with self.transaction() as conn:
            user = conn.execute("""
                SELECT id, username, email, role, created_at, last_login, profile_data
                FROM users WHERE id = ?
            """, (user_id,)).fetchone()
            
            if user:
                profile = dict(user)
                try:
                    profile['profile_data'] = json.loads(user['profile_data'])
                except:
                    profile['profile_data'] = {}
                return profile
            return {}
    
    def log_activity(self, user_id: int, activity_type: str, description: str, 
                    ip_address: str = None, user_agent: str = None, metadata: Dict = None):
        """Log user activity"""
        with self.transaction() as conn:
            conn.execute("""
                INSERT INTO activity_logs 
                (user_id, activity_type, description, ip_address, user_agent, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, activity_type, description, ip_address, user_agent, 
                 json.dumps(metadata or {})))
    
    def get_user_activity(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent user activity"""
        with self.transaction() as conn:
            activities = conn.execute("""
                SELECT activity_type, description, created_at, metadata
                FROM activity_logs 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (user_id, limit)).fetchall()
            
            return [dict(activity) for activity in activities]
    
    def save_processing_result(self, user_id: int, filename: str, file_type: str, 
                             result_data: Dict[str, Any]):
        """Save file processing results"""
        with self.transaction() as conn:
            conn.execute("""
                INSERT INTO processing_results 
                (user_id, filename, file_type, result_data, processing_time)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, filename, file_type, json.dumps(result_data), 0))
    
    def get_user_count(self) -> int:
        """Get total number of users"""
        with self.transaction() as conn:
            result = conn.execute("SELECT COUNT(*) as count FROM users").fetchone()
            return result['count'] if result else 0
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users (admin function)"""
        with self.transaction() as conn:
            users = conn.execute("""
                SELECT id, username, email, role, created_at, last_login, is_active
                FROM users ORDER BY created_at DESC
            """).fetchall()
            return [dict(user) for user in users]
    
    def get_system_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get system logs"""
        with self.transaction() as conn:
            logs = conn.execute("""
                SELECT level, module, message, created_at
                FROM system_logs 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,)).fetchall()
            return [dict(log) for log in logs]
    
    def get_user_notifications(self, user_id: int, unread_only: bool = True) -> List[Dict[str, Any]]:
        """Get user notifications"""
        with self.transaction() as conn:
            query = """
                SELECT id, title, message, notification_type, created_at, is_read
                FROM user_notifications 
                WHERE user_id = ? AND (expires_at IS NULL OR expires_at > ?)
            """
            params = [user_id, datetime.now()]
            
            if unread_only:
                query += " AND is_read = 0"
            
            query += " ORDER BY created_at DESC LIMIT 20"
            
            notifications = conn.execute(query, params).fetchall()
            return [dict(notif) for notif in notifications]
    
    def create_notification(self, user_id: int, title: str, message: str, 
                          notification_type: str = 'info', expires_hours: int = 24):
        """Create a new notification for user"""
        expires_at = datetime.now() + timedelta(hours=expires_hours)
        
        with self.transaction() as conn:
            conn.execute("""
                INSERT INTO user_notifications 
                (user_id, title, message, notification_type, expires_at)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, title, message, notification_type, expires_at))
