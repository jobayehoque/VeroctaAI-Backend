import os
import logging
from flask import Flask, send_from_directory, send_file, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Configure logging for production
log_level = logging.INFO if os.environ.get('FLASK_ENV') == 'production' else logging.DEBUG
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('verocta.log') if os.environ.get('FLASK_ENV') == 'production' else logging.NullHandler()
    ]
)

# Get the directory of this script
basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
    logging.info("Environment variables loaded from .env file")
except ImportError:
    logging.warning("python-dotenv not installed. Install with: pip install python-dotenv")
except Exception as e:
    logging.error(f"Error loading .env file: {e}")

# Debug: Log all environment variables that start with common prefixes
logging.info("=== Environment Variables Debug ===")
for key, value in os.environ.items():
    if any(key.startswith(prefix) for prefix in ['SESSION', 'FLASK', 'PYTHON', 'SUPABASE', 'OPENAI']):
        logging.info(f"{key}: {'SET' if value else 'EMPTY'}")
logging.info("=== End Environment Variables Debug ===")

# Create the Flask app for API-only service
app = Flask(__name__,
            template_folder=os.path.join(basedir, 'templates'))
# Set secret key with fallback for deployment
session_secret = os.environ.get("SESSION_SECRET")
logging.info(f"SESSION_SECRET environment variable: {'SET' if session_secret else 'NOT SET'}")
if not session_secret:
    # Generate a fallback secret for production deployment
    import secrets
    session_secret = secrets.token_hex(32)
    logging.warning("SESSION_SECRET not found, using generated fallback secret")

app.secret_key = session_secret
logging.info("Flask app secret key configured successfully")

# Import and configure enhanced database service
try:
    from database_enhanced import enhanced_db
    if enhanced_db.connected:
        app.config["DATABASE_URL"] = "configured"  # Flag that database is available
        app.config["ENHANCED_DB"] = enhanced_db  # Store enhanced DB instance
        logging.info("✅ Enhanced database connection established via SQLAlchemy")
        logging.info("✅ Enhanced database tables initialized")
    else:
        app.config["DATABASE_URL"] = None
        logging.warning("⚠️ Enhanced database connection failed - falling back to legacy database")
        # Fallback to legacy database
        from database import db_service
        if db_service.connected:
            app.config["DATABASE_URL"] = "configured"
            logging.info("✅ Legacy database connection established")
        else:
            app.config["DATABASE_URL"] = None
            logging.warning("⚠️ All database connections failed - using in-memory storage only")
except Exception as e:
    logging.error(f"⚠️ Enhanced database service import failed: {str(e)} - falling back to legacy")
    try:
        from database import db_service
        if db_service.connected:
            app.config["DATABASE_URL"] = "configured"
            logging.info("✅ Legacy database connection established")
        else:
            app.config["DATABASE_URL"] = None
    except:
        app.config["DATABASE_URL"] = None

# Enable CORS for development and production
allowed_origins = [
    "http://localhost:5000", 
    "http://127.0.0.1:5000",
    "http://localhost:3000",  # React dev server
    "https://verocta-ai.onrender.com",  # Production URL
    "https://*.onrender.com",  # Render subdomains
    "https://*.vercel.app",  # Vercel deployments
    "https://*.netlify.app"  # Netlify deployments
]

# Add custom domain if provided
custom_domain = os.environ.get("CUSTOM_DOMAIN")
if custom_domain:
    allowed_origins.append(f"https://{custom_domain}")
    allowed_origins.append(f"http://{custom_domain}")

# Remove empty strings and duplicates
allowed_origins = list(set([origin for origin in allowed_origins if origin]))

CORS(app, resources={
    r"/api/*": {
        "origins": allowed_origins,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"]
    }
})

# Initialize authentication
try:
    from auth import init_auth
    jwt = init_auth(app)
except ImportError:
    logging.warning("Auth module not found - running without authentication")
    jwt = None

# Import routes after app creation to avoid circular imports
try:
    from routes import *
except ImportError:
    logging.warning("Routes module not found - creating basic routes")
    
    # Routes are imported from routes.py module
    pass

if __name__ == '__main__':
    # Production configuration
    is_production = os.environ.get('FLASK_ENV') == 'production'
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'  # Always use 0.0.0.0 for Render compatibility
    debug = not is_production
    
    logging.info('🚀 Starting VeroctaAI API Service...')
    logging.info(f'📍 URL: http://{host}:{port}')
    logging.info('📊 Platform: AI-Powered Financial Intelligence & Analytics API')
    logging.info(f'🔧 Environment: {"Production" if is_production else "Development"}')
    logging.info('🌐 Service Type: Backend API Only')

    # Check OpenAI API key
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        logging.info('🤖 AI: GPT-4o Integration Ready ✅')
    else:
        logging.warning('⚠️  WARNING: OPENAI_API_KEY not set! AI features will not work.')
        logging.info('💡 Fix: Set environment variable or create .env file with your API key')

    # Check database connection
    if app.config.get("DATABASE_URL"):
        logging.info('🗄️  Database: PostgreSQL Connected ✅')
    else:
        logging.warning('🗄️  Database: In-memory storage (no persistence)')

    logging.info('📁 CSV Support: QuickBooks, Wave, Revolut, Xero')
    logging.info('✅ Server starting...')
    
    if is_production:
        # Use Gunicorn for production
        logging.info('🚀 Production mode: Use Gunicorn for deployment')
        logging.info('Command: gunicorn --bind 0.0.0.0:{} --workers 4 app:app'.format(port))
    else:
        app.run(host=host, port=port, debug=debug)
