"""
Health check module for VeroctaAI
Provides system health monitoring for Render deployment
"""

import os
import logging
from datetime import datetime

def check_health():
    """
    Comprehensive health check for the VeroctaAI system
    Returns status information for monitoring
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": os.environ.get('FLASK_ENV', 'development'),
        "checks": {}
    }
    
    # Check environment variables
    required_env_vars = ['SESSION_SECRET']
    optional_env_vars = ['OPENAI_API_KEY', 'SUPABASE_URL', 'SUPABASE_PASSWORD', 'SUPABASE_ANON_KEY']
    
    env_check = {"status": "pass", "details": {}}
    
    # Check required variables
    for var in required_env_vars:
        if os.environ.get(var):
            env_check["details"][var] = "✅ Set"
        else:
            env_check["details"][var] = "❌ Missing"
            env_check["status"] = "fail"
            health_status["status"] = "unhealthy"
    
    # Check optional variables
    for var in optional_env_vars:
        if os.environ.get(var):
            env_check["details"][var] = "✅ Set"
        else:
            env_check["details"][var] = "⚠️ Not set (optional)"
    
    health_status["checks"]["environment"] = env_check
    
    # Check database connection (non-blocking)
    db_check = {"status": "pass", "details": "Database not configured"}
    if os.environ.get('SUPABASE_URL') and os.environ.get('SUPABASE_PASSWORD'):
        db_check = {"status": "pass", "details": "✅ Database URL configured (connection not tested in health check)"}
    else:
        db_check = {"status": "pass", "details": "⚠️ Database not configured (using in-memory storage)"}
    
    health_status["checks"]["database"] = db_check
    
    # Check AI integration
    ai_check = {"status": "pass", "details": "AI not configured"}
    if os.environ.get('OPENAI_API_KEY'):
        try:
            import openai
            ai_check = {"status": "pass", "details": "✅ OpenAI API configured"}
        except Exception as e:
            ai_check = {"status": "fail", "details": f"❌ OpenAI error: {str(e)}"}
            health_status["status"] = "unhealthy"
    else:
        ai_check = {"status": "pass", "details": "⚠️ OpenAI API not configured (optional)"}
    
    health_status["checks"]["ai"] = ai_check
    
    # Frontend removed in backend-only repository
    health_status["checks"]["frontend"] = {
        "status": "removed",
        "details": "Frontend files have been removed; this is a backend-only repository"
    }
    
    return health_status

def get_system_info():
    """
    Get system information for debugging
    """
    import platform
    import sys
    
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "architecture": platform.architecture(),
        "processor": platform.processor(),
        "working_directory": os.getcwd(),
        "environment_variables": {
            key: "***" if "key" in key.lower() or "secret" in key.lower() or "password" in key.lower() 
            else value for key, value in os.environ.items()
        }
    }
