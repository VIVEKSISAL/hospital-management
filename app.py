"""
Hospital Management System - Main Application
Flask application with role-based access control
"""
import os
from flask import Flask, render_template
from flask_login import LoginManager, current_user
from config import config
from models import db, User
from routes import auth_bp, dashboard_bp, patient_bp, doctor_bp, appointment_bp, billing_bp, room_bp, lab_report_bp

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID"""
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(lab_report_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 errors"""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden(e):
        """Handle 403 errors"""
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def server_error(e):
        """Handle 500 errors"""
        return render_template('errors/500.html'), 500
    
    # Context processors
    @app.context_processor
    def inject_user():
        """Inject user into template context"""
        return dict(current_user=current_user)
    
    # Application initialization
    with app.app_context():
        db.create_all()
    
    # Home route
    @app.route('/')
    def index():
        """Home page"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return render_template('index.html')
    
    # Health check route
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return {'status': 'ok', 'message': 'Hospital Management System is running'}, 200
    
    return app

if __name__ == '__main__':
    # Create application
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    # Run application
    debug_mode = os.getenv('DEBUG', 'True') == 'True'
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=debug_mode
    )
