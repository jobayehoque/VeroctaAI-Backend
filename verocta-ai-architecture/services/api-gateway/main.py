"""
VeroctaAI Enterprise API Gateway v2.0
FastAPI-based API Gateway with authentication, rate limiting, and routing
"""

import os
import logging
import time
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import redis
import uvicorn
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response as StarletteResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/api-gateway.log')
    ]
)
logger = logging.getLogger(__name__)

# Metrics
REQUEST_COUNT = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('api_request_duration_seconds', 'API request duration', ['method', 'endpoint'])
AUTH_FAILURES = Counter('auth_failures_total', 'Authentication failures', ['reason'])

# Redis connection for rate limiting
try:
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=int(os.getenv('REDIS_DB', 0)),
        password=os.getenv('REDIS_PASSWORD'),
        decode_responses=True
    )
    redis_client.ping()
    logger.info("✅ Redis connection established")
except Exception as e:
    logger.error(f"❌ Redis connection failed: {e}")
    redis_client = None

# Rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}",
    enabled=redis_client is not None
)

# Security
security = HTTPBearer()

# Service URLs
SERVICE_URLS = {
    'auth': os.getenv('AUTH_SERVICE_URL', 'http://auth-service:8001'),
    'analytics': os.getenv('ANALYTICS_SERVICE_URL', 'http://analytics-service:8002'),
    'payment': os.getenv('PAYMENT_SERVICE_URL', 'http://payment-service:8003'),
    'notification': os.getenv('NOTIFICATION_SERVICE_URL', 'http://notification-service:8004'),
    'report': os.getenv('REPORT_SERVICE_URL', 'http://report-service:8005'),
    'integration': os.getenv('INTEGRATION_SERVICE_URL', 'http://integration-service:8006'),
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 Starting VeroctaAI Enterprise API Gateway v2.0")
    yield
    logger.info("🛑 Shutting down API Gateway")

# Create FastAPI app
app = FastAPI(
    title="VeroctaAI Enterprise API Gateway",
    description="Enterprise-grade API Gateway for VeroctaAI Financial Intelligence Platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.verocta.ai", "*.onrender.com"]
)

if redis_client:
    app.add_middleware(SlowAPIMiddleware)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "2.0.0",
        "services": {
            "redis": "connected" if redis_client else "disconnected",
            "rate_limiting": "enabled" if redis_client else "disabled"
        }
    }

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return StarletteResponse(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

# Authentication dependency
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    if not credentials:
        AUTH_FAILURES.labels(reason="no_token").inc()
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # In a real implementation, you would verify the JWT token here
    # For now, we'll do a simple validation
    token = credentials.credentials
    if not token or len(token) < 10:
        AUTH_FAILURES.labels(reason="invalid_token").inc()
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {"user_id": "demo_user", "email": "demo@verocta.ai"}

# Rate limiting decorator
def rate_limit(requests_per_minute: int = 100):
    """Rate limiting decorator"""
    if redis_client:
        return limiter.limit(f"{requests_per_minute}/minute")
    return lambda x: x

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Update metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    # Log request
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {duration:.3f}s"
    )
    
    return response

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "VeroctaAI Enterprise API Gateway v2.0",
        "version": "2.0.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/health"
    }

# Authentication routes
@app.post("/api/v2/auth/login")
@rate_limit(10)  # 10 requests per minute
async def login(request: Request):
    """Login endpoint - proxy to auth service"""
    # This would proxy to the auth service
    return {"message": "Login endpoint - proxy to auth service"}

@app.post("/api/v2/auth/register")
@rate_limit(5)  # 5 requests per minute
async def register(request: Request):
    """Register endpoint - proxy to auth service"""
    return {"message": "Register endpoint - proxy to auth service"}

@app.post("/api/v2/auth/refresh")
async def refresh_token(request: Request):
    """Refresh token endpoint - proxy to auth service"""
    return {"message": "Refresh token endpoint - proxy to auth service"}

# Analytics routes
@app.get("/api/v2/analytics/spend-score")
async def get_spend_score(current_user: dict = Depends(verify_token)):
    """Get spend score - proxy to analytics service"""
    return {"message": "Spend score endpoint - proxy to analytics service"}

@app.post("/api/v2/analytics/analyze")
@rate_limit(20)  # 20 requests per minute
async def analyze_data(request: Request, current_user: dict = Depends(verify_token)):
    """Analyze financial data - proxy to analytics service"""
    return {"message": "Analysis endpoint - proxy to analytics service"}

# Payment routes
@app.get("/api/v2/payments/subscriptions")
async def get_subscriptions(current_user: dict = Depends(verify_token)):
    """Get user subscriptions - proxy to payment service"""
    return {"message": "Subscriptions endpoint - proxy to payment service"}

@app.post("/api/v2/payments/create-subscription")
async def create_subscription(request: Request, current_user: dict = Depends(verify_token)):
    """Create subscription - proxy to payment service"""
    return {"message": "Create subscription endpoint - proxy to payment service"}

# Report routes
@app.get("/api/v2/reports")
async def get_reports(current_user: dict = Depends(verify_token)):
    """Get user reports - proxy to report service"""
    return {"message": "Reports endpoint - proxy to report service"}

@app.post("/api/v2/reports/generate")
@rate_limit(10)  # 10 requests per minute
async def generate_report(request: Request, current_user: dict = Depends(verify_token)):
    """Generate report - proxy to report service"""
    return {"message": "Generate report endpoint - proxy to report service"}

# Integration routes
@app.post("/api/v2/integrations/upload")
@rate_limit(5)  # 5 requests per minute
async def upload_file(request: Request, current_user: dict = Depends(verify_token)):
    """Upload file - proxy to integration service"""
    return {"message": "Upload endpoint - proxy to integration service"}

@app.get("/api/v2/integrations/quickbooks/connect")
async def connect_quickbooks(current_user: dict = Depends(verify_token)):
    """Connect QuickBooks - proxy to integration service"""
    return {"message": "QuickBooks connection endpoint - proxy to integration service"}

# Notification routes
@app.get("/api/v2/notifications")
async def get_notifications(current_user: dict = Depends(verify_token)):
    """Get notifications - proxy to notification service"""
    return {"message": "Notifications endpoint - proxy to notification service"}

@app.post("/api/v2/notifications/mark-read")
async def mark_notification_read(request: Request, current_user: dict = Depends(verify_token)):
    """Mark notification as read - proxy to notification service"""
    return {"message": "Mark notification read endpoint - proxy to notification service"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.time()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": time.time()
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("RELOAD", "false").lower() == "true",
        log_level="info"
    )
