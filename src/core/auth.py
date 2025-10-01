import os
import bcrypt
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt
)
from functools import wraps
import logging

try:
    # Attempt to import the database service, assuming it handles Supabase connection
    from .database import db_service
except ImportError:
    db_service = None
    logging.warning("Database service not found. Supabase integration may not be available.")

# Simple in-memory user store (replace with database in production)
# Pre-computed password hashes for consistent authentication
admin_password_hash = b'$2b$12$ZKOiYm4737YUelAqY2xLD.lx7PI8oTUFKZjjfZlmEK3Tzx.q0ZCpm'  # admin123
demo_password_hash = b'$2b$12$z2zF.Wlh3rF.rSqkaw2Bn.7rG/EbXsuChM/xSdneDmQlVDV6YqtSu'   # demo123

users_db = {
    "admin@verocta.ai": {
        "id": 1,
        "email": "admin@verocta.ai",
        "password": admin_password_hash,
        "role": "admin",
        "created_at": datetime.now(),
        "company": "VeroctaAI",
        "is_active": True
    },
    "demo@verocta.ai": {
        "id": 2,
        "email": "demo@verocta.ai",
        "password": demo_password_hash,
        "role": "user",
        "created_at": datetime.now(),
        "company": "VeroctaAI Demo",
        "is_active": True
    },
    "user@verocta.ai": {
        "id": 3,
        "email": "user@verocta.ai",
        "password": demo_password_hash,  # Same password for simplicity
        "role": "user",
        "created_at": datetime.now(),
        "company": "VeroctaAI",
        "is_active": True
    },
    "test@example.com": {
        "id": 4,
        "email": "test@example.com",
        "password": demo_password_hash,  # Same password for simplicity
        "role": "user",
        "created_at": datetime.now(),
        "company": "Test Company",
        "is_active": True
    },
    "test@verocta.ai": {
        "id": 5,
        "email": "test@verocta.ai",
        "password": b'$2b$12$nX3lVDsx9eBsoJBkF3zKRujkOyzUCmyA2CoJEBzLjXpU6VdexNie.',  # testpass123
        "role": "user",
        "created_at": datetime.now(),
        "company": "Test Company LLC",
        "is_active": True
    }
}

# Simple token revocation store. Uses Redis if available, otherwise in-memory set.
token_blocklist = None
try:
    import redis
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    redis_client.ping()
    token_blocklist = redis_client
    logging.info("Redis connected for token management")
except:
    token_blocklist = set()
    logging.info("Using in-memory token store (Redis not available)")

def init_auth(app):
    """Initialize JWT authentication with Flask app"""
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', app.secret_key)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    
    jwt = JWTManager(app)
    
    # Token blocklist check
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        if isinstance(token_blocklist, set):
            return jti in token_blocklist
        try:
            return token_blocklist.get(jti) is not None
        except:
            return False
    
    return jwt

def revoke_token(jti):
    """Revoke a token by adding it to blocklist"""
    if isinstance(token_blocklist, set):
        token_blocklist.add(jti)
    else:
        try:
            token_blocklist.setex(jti, 86400 * 30, "revoked")  # 30 days expiry
        except:
            pass

def validate_user(email, password):
    """Validate user credentials"""
    try:
        # Try database first
        if db_service:
            db_user = db_service.get_user_by_email(email)
            if db_user and db_user.get('is_active'):
                stored_password = db_user['password_hash']
                if isinstance(stored_password, str):
                    stored_password = stored_password.encode('utf-8')
                
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    return {
                        'id': db_user['id'],
                        'email': db_user['email'],
                        'role': db_user.get('role', 'user'),
                        'company': db_user.get('company', 'Default Company')
                    }
        
        # Fallback to in-memory users
        if email in users_db:
            user = users_db[email]
            if user.get('is_active') and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                return {
                    'id': user['id'],
                    'email': user['email'],
                    'role': user.get('role', 'user'),
                    'company': user.get('company', 'Default Company')
                }
        
        return None
        
    except Exception as e:
        logging.error(f"User validation error: {str(e)}")
        return None

def create_user(email, password, company=None, role="user"):
    """Create a new user"""
    try:
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Try database first
        if db_service:
            db_user = db_service.create_user(email, password_hash.decode('utf-8'), company, role)
            if db_user:
                return {
                    'id': db_user['id'],
                    'email': db_user['email'],
                    'role': db_user.get('role', 'user'),
                    'company': db_user.get('company', company or 'Default Company')
                }
        
        # Fallback to in-memory storage
        if email in users_db:
            return None  # User already exists
        
        new_user_id = max([user['id'] for user in users_db.values()], default=0) + 1
        users_db[email] = {
            'id': new_user_id,
            'email': email,
            'password': password_hash,
            'role': role,
            'company': company or 'Default Company',
            'created_at': datetime.now(),
            'is_active': True
        }
        
        return {
            'id': new_user_id,
            'email': email,
            'role': role,
            'company': company or 'Default Company'
        }
        
    except Exception as e:
        logging.error(f"User creation error: {str(e)}")
        return None

def get_current_user():
    """Get current user from JWT token"""
    try:
        email = get_jwt_identity()
        if not email:
            return None
        
        # Try database first
        if db_service:
            db_user = db_service.get_user_by_email(email)
            if db_user and db_user.get('is_active'):
                return {
                    'id': db_user['id'],
                    'email': db_user['email'],
                    'role': db_user.get('role', 'user'),
                    'company': db_user.get('company', 'Default Company'),
                    'created_at': db_user.get('created_at')
                }
        
        # Fallback to in-memory users
        if email in users_db:
            user = users_db[email]
            if user.get('is_active'):
                return {
                    'id': user['id'],
                    'email': user['email'],
                    'role': user.get('role', 'user'),
                    'company': user.get('company', 'Default Company'),
                    'created_at': user.get('created_at')
                }
        
        return None
        
    except Exception as e:
        logging.error(f"Get current user error: {str(e)}")
        return None

def require_admin(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def require_role(role):
    """Decorator factory to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user or user.get('role') != role:
                return jsonify({'error': f'{role} access required'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Initialize mock users for development
def init_mock_users():
    """Initialize additional mock users for testing"""
    mock_users = [
        ("alice@company.com", "password123", "Alice Corp", "user"),
        ("bob@startup.io", "password123", "Bob's Startup", "user"), 
        ("charlie@enterprise.com", "password123", "Enterprise Corp", "admin")
    ]
    
    for email, password, company, role in mock_users:
        if email not in users_db:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_id = max([user['id'] for user in users_db.values()], default=4) + 1
            users_db[email] = {
                'id': new_id,
                'email': email,
                'password': password_hash,
                'role': role,
                'company': company,
                'created_at': datetime.now(),
                'is_active': True
            }

# Initialize mock users
init_mock_users()