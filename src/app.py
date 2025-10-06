import os
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, Any, List, Optional
import json
import hashlib

from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

from .database import DatabaseManager
from .utils import AdvancedUtils, SecurityManager, CacheManager, DataProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def create_app():
    """Factory function to create and configure the Flask application"""
    
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Configuration
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
        SESSION_TYPE='filesystem',
        SESSION_PERMANENT=False,
        SESSION_USE_SIGNER=True,
        SESSION_KEY_PREFIX='advanced_app_',
        PERMANENT_SESSION_LIFETIME=timedelta(hours=24),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file upload
    )
    
    # Initialize extensions
    Session(app)
    
    # Initialize custom components
    db_manager = DatabaseManager()
    security_manager = SecurityManager()
    cache_manager = CacheManager()
    data_processor = DataProcessor()
    
    # Store components in app context
    app.db_manager = db_manager
    app.security_manager = security_manager
    app.cache_manager = cache_manager
    app.data_processor = data_processor
    
    def require_auth(f):
        """Decorator to require authentication"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    
    def require_role(role: str):
        """Decorator to require specific role"""
        def decorator(f):
            @wraps(f)
            @require_auth
            def decorated_function(*args, **kwargs):
                user_role = session.get('user_role', 'user')
                if user_role != role and user_role != 'admin':
                    flash('Insufficient permissions.', 'danger')
                    return redirect(url_for('dashboard'))
                return f(*args, **kwargs)
            return decorated_function
        return decorator

    # Template context processors
    @app.context_processor
    def utility_processor():
        def format_datetime(value, format='medium'):
            if isinstance(value, str):
                value = datetime.fromisoformat(value)
            if format == 'full':
                format_str = "%Y-%m-%d %H:%M:%S"
            elif format == 'medium':
                format_str = "%Y-%m-%d %H:%M"
            else:
                format_str = "%Y-%m-%d"
            return value.strftime(format_str)
        
        def get_current_year():
            return datetime.now().year
        
        return dict(
            format_datetime=format_datetime,
            current_year=get_current_year
        )

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Server Error: {error}")
        return render_template('500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403

    # Routes
    @app.route('/')
    def index():
        """Home page with system overview"""
        system_stats = cache_manager.get('system_stats')
        if not system_stats:
            system_stats = {
                'total_users': db_manager.get_user_count(),
                'active_sessions': 0,  # Simplified for now
                'system_uptime': AdvancedUtils.get_system_uptime(),
                'memory_usage': AdvancedUtils.get_memory_usage(),
                'cpu_usage': AdvancedUtils.get_cpu_usage(),
                'timestamp': datetime.now().isoformat()
            }
            cache_manager.set('system_stats', system_stats, timeout=300)
        
        return render_template('index.html', stats=system_stats)
    
    @app.route('/dashboard')
    @require_auth
    def dashboard():
        """User dashboard with personalized data"""
        user_id = session['user_id']
        user_data = cache_manager.get(f'user_{user_id}_dashboard')
        
        if not user_data:
            user_data = {
                'profile': db_manager.get_user_profile(user_id),
                'recent_activity': db_manager.get_user_activity(user_id, limit=10),
                'analytics': data_processor.analyze_user_behavior(user_id),
                'notifications': db_manager.get_user_notifications(user_id)
            }
            cache_manager.set(f'user_{user_id}_dashboard', user_data, timeout=60)
        
        return render_template('dashboard.html', data=user_data)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Advanced login system with security features"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            remember_me = bool(request.form.get('remember_me'))
            
            # Security checks
            if security_manager.is_ip_blocked(request.remote_addr):
                flash('Too many failed attempts. Please try again later.', 'danger')
                return render_template('login.html')
            
            user = db_manager.authenticate_user(username, password)
            if user:
                # Successful login
                security_manager.clear_failed_attempts(request.remote_addr)
                
                session.permanent = remember_me
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['user_role'] = user['role']
                session['login_time'] = datetime.now().isoformat()
                
                # Log login activity
                db_manager.log_activity(
                    user['id'], 
                    'login', 
                    f'Successful login from {request.remote_addr}'
                )
                
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                # Failed login
                security_manager.record_failed_attempt(request.remote_addr)
                flash('Invalid credentials. Please try again.', 'danger')
        
        return render_template('login.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Advanced user registration with validation"""
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Validation
            errors = []
            if not security_manager.is_valid_username(username):
                errors.append('Invalid username format.')
            if not security_manager.is_valid_email(email):
                errors.append('Invalid email format.')
            if not security_manager.is_strong_password(password):
                errors.append('Password does not meet security requirements.')
            if password != confirm_password:
                errors.append('Passwords do not match.')
            if db_manager.username_exists(username):
                errors.append('Username already exists.')
            if db_manager.email_exists(email):
                errors.append('Email already registered.')
            
            if not errors:
                user_id = db_manager.create_user(username, email, password)
                if user_id:
                    flash('Registration successful! Please log in.', 'success')
                    return redirect(url_for('login'))
                else:
                    errors.append('Registration failed. Please try again.')
            
            for error in errors:
                flash(error, 'danger')
        
        return render_template('register.html')
    
    @app.route('/admin')
    @require_role('admin')
    def admin_panel():
        """Administrative panel with system management"""
        admin_data = {
            'users': db_manager.get_all_users(),
            'system_logs': db_manager.get_system_logs(limit=50),
            'performance_metrics': AdvancedUtils.get_performance_metrics(),
            'security_events': security_manager.get_security_events()
        }
        
        return render_template('admin.html', data=admin_data)
    
    @app.route('/api/v1/analyze', methods=['POST'])
    @require_auth
    def analyze_data():
        """Advanced data analysis endpoint"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            analysis_type = data.get('type', 'general')
            input_data = data.get('data')
            
            if analysis_type == 'text':
                result = data_processor.analyze_text(input_data)
            elif analysis_type == 'numeric':
                result = data_processor.analyze_numeric_data(input_data)
            elif analysis_type == 'pattern':
                result = data_processor.detect_patterns(input_data)
            else:
                result = data_processor.comprehensive_analysis(input_data)
            
            # Log analysis activity
            db_manager.log_activity(
                session['user_id'],
                'data_analysis',
                f'Analysis performed: {analysis_type}'
            )
            
            return jsonify({
                'success': True,
                'analysis_type': analysis_type,
                'result': result,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return jsonify({'error': 'Analysis failed'}), 500
    
    @app.route('/api/v1/process-file', methods=['POST'])
    @require_auth
    def process_file():
        """File processing endpoint with multiple formats support"""
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        try:
            # Process file based on type
            file_type = file.filename.split('.')[-1].lower()
            processor = data_processor.get_file_processor(file_type)
            
            if not processor:
                return jsonify({'error': 'Unsupported file type'}), 400
            
            result = processor.process(file.stream)
            
            # Store processing result
            db_manager.save_processing_result(
                session['user_id'],
                file.filename,
                file_type,
                result
            )
            
            return jsonify({
                'success': True,
                'filename': file.filename,
                'file_type': file_type,
                'result': result
            })
            
        except Exception as e:
            logger.error(f"File processing error: {str(e)}")
            return jsonify({'error': 'File processing failed'}), 500
    
    @app.route('/profile')
    @require_auth
    def profile():
        """User profile management"""
        user_profile = db_manager.get_user_profile(session['user_id'])
        return render_template('profile.html', profile=user_profile)
    
    @app.route('/logout')
    def logout():
        """Logout with session cleanup"""
        if 'user_id' in session:
            db_manager.log_activity(
                session['user_id'],
                'logout',
                'User logged out'
            )
        
        session.clear()
        flash('You have been logged out successfully.', 'info')
        return redirect(url_for('index'))
    
    logger.info("Application initialized successfully")
    return app

# For direct execution
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
