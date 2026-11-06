from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Configure CORS with proper headers
    CORS(app, 
         origins=Config.CORS_ORIGINS, 
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         expose_headers=['Content-Type', 'Authorization'])
    
    jwt = JWTManager(app)
    
    # JWT error handlers
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return jsonify({
            'error': 'Missing Authorization Header',
            'message': 'Request does not contain an access token'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return jsonify({
            'error': 'Invalid token',
            'message': 'Signature verification failed'
        }), 401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token has expired',
            'message': 'The token has expired'
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token has been revoked',
            'message': 'The token has been revoked'
        }), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Fresh token required',
            'message': 'Fresh token required'
        }), 401
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.hospitals import hospitals_bp
    from routes.appointments import appointments_bp
    from routes.admin import admin_bp
    from routes.constraints import constraints_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(hospitals_bp, url_prefix='/api/hospitals')
    app.register_blueprint(appointments_bp, url_prefix='/api/appointments')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(constraints_bp, url_prefix='/api/constraints')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'The Missing Link API is running'}), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
