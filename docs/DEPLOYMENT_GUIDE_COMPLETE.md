# 🚀 VeroctaAI Deployment Guide

**Complete Production Deployment Guide for VeroctaAI Backend**

---

## 📋 Table of Contents

1. [Deployment Overview](#-deployment-overview)
2. [Render.com Deployment](#-rendercom-deployment)
3. [Docker Deployment](#-docker-deployment)
4. [Environment Configuration](#-environment-configuration)
5. [Database Setup](#-database-setup)
6. [Production Checklist](#-production-checklist)
7. [Monitoring & Maintenance](#-monitoring--maintenance)
8. [Troubleshooting](#-troubleshooting)

---

## 🎯 Deployment Overview

VeroctaAI is designed for cloud deployment with the following architecture:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │────│   Application   │────│    Database     │
│  (Render/CDN)   │    │   (Flask API)   │    │  (Supabase)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
   HTTPS Traffic            API Processing          Data Persistence
   SSL Termination         AI-Powered Analysis      PostgreSQL 17.6
   Auto-scaling            File Processing          Connection Pooling
```

### Supported Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| **Render.com** | ✅ Recommended | Easy deployment, auto-scaling |
| **Heroku** | ✅ Supported | Classic PaaS option |
| **Railway** | ✅ Supported | Modern deployment platform |
| **AWS/GCP/Azure** | ✅ Advanced | Requires Docker configuration |
| **DigitalOcean** | ✅ Supported | App Platform or Droplets |
| **Vercel** | ❌ Not suitable | Serverless limitations |

---

## 🌐 Render.com Deployment

### Quick Deploy (5 minutes)

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone
   git clone https://github.com/YOUR_USERNAME/VeroctaAI-Backend.git
   cd VeroctaAI-Backend
   ```

2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Choose `VeroctaAI-Backend`

3. **Configure Deployment**
   ```yaml
   # render.yaml is already configured
   Name: verocta-ai-backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --bind 0.0.0.0:$PORT app:app --workers 4 --timeout 120
   ```

4. **Set Environment Variables**
   ```bash
   FLASK_ENV=production
   DATABASE_URL=your_supabase_database_url
   OPENAI_API_KEY=your_openai_api_key
   SESSION_SECRET=your_random_secret_key
   JWT_SECRET_KEY=your_jwt_secret_key
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Your API will be available at `https://your-app.onrender.com`

### Advanced Render Configuration

```yaml
# render.yaml - Complete Configuration
services:
  - type: web
    name: verocta-ai-backend
    env: python
    plan: starter  # $7/month - upgrade to standard for production
    buildCommand: |
      pip install --upgrade pip
      pip install -r requirements.txt
      python -c "import nltk; nltk.download('punkt')"
    startCommand: |
      gunicorn --bind 0.0.0.0:$PORT app:app \
        --workers 4 \
        --worker-class gevent \
        --worker-connections 1000 \
        --timeout 120 \
        --keep-alive 5 \
        --max-requests 1000 \
        --max-requests-jitter 50 \
        --preload \
        --access-logfile - \
        --error-logfile -
    
    # Environment Variables
    envVars:
      - key: FLASK_ENV
        value: production
      - key: PYTHONPATH
        value: .
      - key: WEB_CONCURRENCY
        value: 4
    
    # Health Check
    healthCheckPath: /api/health
    
    # Scaling
    autoDeploy: true
    
    # Custom Domains (optional)
    # domains:
    #   - api.verocta.ai

# Database (if using Render PostgreSQL)
databases:
  - name: verocta-ai-db
    plan: starter  # $7/month
    postgresMajorVersion: 17
```

---

## 🐳 Docker Deployment

### Production Dockerfile

```dockerfile
# Multi-stage build for production
FROM python:3.13-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.13-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /home/app/.local

# Copy application code
COPY --chown=app:app . .

# Switch to non-root user
USER app

# Set environment variables
ENV PATH=/home/app/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV FLASK_ENV=production
ENV PORT=8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/api/health || exit 1

# Expose port
EXPOSE 8001

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "app:app", "--workers", "4", "--timeout", "120"]
```

### Docker Compose (Development + Production)

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Application
  app:
    build: .
    ports:
      - "8001:8001"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SESSION_SECRET=${SESSION_SECRET}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    depends_on:
      - db
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Database (optional - use if not using Supabase)
  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_DB: verocta_ai
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  # Redis (optional - for caching)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  # Nginx (optional - for reverse proxy)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
```

### Build and Deploy with Docker

```bash
# Build the image
docker build -t verocta-ai:latest .

# Run locally
docker run -p 8001:8001 \
  -e DATABASE_URL="your_database_url" \
  -e OPENAI_API_KEY="your_api_key" \
  -e SESSION_SECRET="your_secret" \
  verocta-ai:latest

# Deploy to production
docker tag verocta-ai:latest your-registry/verocta-ai:v1.0.0
docker push your-registry/verocta-ai:v1.0.0
```

---

## ⚙️ Environment Configuration

### Production Environment Variables

Create a `.env.production` file:

```bash
# Application Configuration
FLASK_ENV=production
PORT=8001
DEBUG=False

# Security
SESSION_SECRET=your-super-secure-random-string-here
JWT_SECRET_KEY=another-super-secure-jwt-key-here
BCRYPT_LOG_ROUNDS=12

# Database
DATABASE_URL=postgresql+psycopg2://user:password@host:port/database
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
DB_POOL_TIMEOUT=30

# AI Services
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_ORG_ID=org-your-openai-org-id (optional)
OPENAI_MODEL=gpt-4o
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7

# Supabase (if using)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_PASSWORD=your-supabase-password

# File Storage
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads
ALLOWED_EXTENSIONS=csv

# Rate Limiting
RATELIMIT_STORAGE_URL=redis://localhost:6379/0
RATELIMIT_DEFAULT=100 per hour

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email (if implementing notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Monitoring
SENTRY_DSN=your-sentry-dsn-here (optional)
```

### Generate Secure Keys

```bash
# Generate secure secrets
python -c "import secrets; print('SESSION_SECRET=' + secrets.token_urlsafe(64))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(64))"

# Or use openssl
openssl rand -base64 64
```

---

## 🗄️ Database Setup

### Supabase Setup (Recommended)

1. **Create Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Choose region (closest to your users)
   - Set strong password

2. **Get Connection Details**
   ```bash
   # Project Settings → Database
   Host: db.your-project-ref.supabase.co
   Database: postgres
   Port: 5432
   User: postgres
   Password: your_password
   ```

3. **Connection String Format**
   ```bash
   # Direct Connection (for Connection Pooler)
   DATABASE_URL=postgresql+psycopg2://postgres:password@db.project.supabase.co:5432/postgres

   # Connection Pooler (recommended for production)
   DATABASE_URL=postgresql+psycopg2://postgres:password@aws-0-region.pooler.supabase.com:6543/postgres?pgbouncer=true
   ```

4. **Initialize Database**
   ```bash
   # The application will automatically create tables
   # Or run manually:
   python setup_supabase_tables.py
   ```

### Self-Hosted PostgreSQL

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE verocta_ai;
CREATE USER verocta_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE verocta_ai TO verocta_user;
\q

# Connection string
DATABASE_URL=postgresql+psycopg2://verocta_user:secure_password@localhost:5432/verocta_ai
```

---

## ✅ Production Checklist

### Pre-Deployment

- [ ] **Environment Variables Set**
  - [ ] `DATABASE_URL` configured
  - [ ] `OPENAI_API_KEY` set
  - [ ] `SESSION_SECRET` generated
  - [ ] `JWT_SECRET_KEY` generated
  - [ ] `FLASK_ENV=production`

- [ ] **Database Ready**
  - [ ] Database created and accessible
  - [ ] Connection string tested
  - [ ] Tables will be auto-created on first run

- [ ] **Dependencies**
  - [ ] `requirements.txt` up to date
  - [ ] All packages installable
  - [ ] Python 3.9+ available

- [ ] **Files & Permissions**
  - [ ] Upload directory created
  - [ ] Proper file permissions set
  - [ ] Logs directory accessible

### Post-Deployment

- [ ] **Health Checks**
  ```bash
  curl https://your-app.onrender.com/api/health
  ```

- [ ] **API Testing**
  ```bash
  # Test registration
  curl -X POST https://your-app.onrender.com/api/auth/register \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"test123"}'
  
  # Test file upload
  curl -X POST https://your-app.onrender.com/api/upload \
    -F "file=@sample.csv"
  ```

- [ ] **Performance**
  - [ ] Response times < 2 seconds
  - [ ] Memory usage stable
  - [ ] No memory leaks

- [ ] **Security**
  - [ ] HTTPS enabled
  - [ ] Secure headers set
  - [ ] Rate limiting active
  - [ ] Input validation working

### Performance Optimization

```bash
# Gunicorn optimized settings
gunicorn --bind 0.0.0.0:$PORT app:app \
  --workers $((2 * $(nproc) + 1)) \
  --worker-class gevent \
  --worker-connections 1000 \
  --timeout 120 \
  --keep-alive 5 \
  --max-requests 1000 \
  --max-requests-jitter 50 \
  --preload
```

---

## 📊 Monitoring & Maintenance

### Health Monitoring

```bash
# Set up monitoring endpoint checks
curl -f https://your-app.onrender.com/api/health

# Expected response
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "services": {
    "database": {"status": "connected"},
    "ai": {"status": "available"}
  }
}
```

### Logging Setup

```python
# Add to your monitoring service
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

if os.getenv('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0
    )

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Performance Metrics

Monitor these key metrics:

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Response Time | < 2s | > 5s |
| Memory Usage | < 512MB | > 1GB |
| CPU Usage | < 70% | > 90% |
| Database Connections | < 50 | > 80 |
| Error Rate | < 1% | > 5% |

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Issues

```bash
# Symptoms
Connection refused / Connection timeout

# Solutions
1. Check DATABASE_URL format
2. Verify database is accessible
3. Check firewall rules
4. Use Connection Pooler for Supabase

# Test connection
python test_db_connection.py
```

#### 2. OpenAI API Issues

```bash
# Symptoms
AI features not working / API key errors

# Solutions
1. Verify OPENAI_API_KEY is set
2. Check API key has sufficient credits
3. Verify model access (gpt-4o)

# Test API
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### 3. File Upload Issues

```bash
# Symptoms
File upload fails / 413 Request Entity Too Large

# Solutions
1. Check MAX_CONTENT_LENGTH setting
2. Verify upload directory exists
3. Check file permissions
4. Ensure CSV format is valid
```

#### 4. Memory Issues

```bash
# Symptoms
Application crashes / Out of memory errors

# Solutions
1. Reduce worker count
2. Implement request timeouts
3. Add garbage collection
4. Upgrade server plan
```

### Debug Commands

```bash
# Check application logs
heroku logs --tail -a your-app-name  # Heroku
render logs --tail your-service-id   # Render

# Test database connection
python -c "from database import test_connection; test_connection()"

# Check environment variables
python -c "import os; print(os.environ.get('DATABASE_URL', 'Not set'))"

# Test API endpoints
python docs/scripts/test_api.sh production
```

### Performance Tuning

```python
# Database connection pooling
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_timeout=30,
    pool_recycle=1800
)

# Request timeout
from werkzeug.middleware.timeout import TimeoutMiddleware
app.wsgi_app = TimeoutMiddleware(app.wsgi_app, timeout=120)

# Compression
from flask_compress import Compress
compress = Compress(app)
```

---

## 📞 Support & Resources

- **GitHub Issues**: [Report Problems](https://github.com/jobayehoque/VeroctaAI-Backend/issues)
- **API Documentation**: `/api/docs`
- **Health Check**: `/api/health`
- **Test Script**: `docs/scripts/test_api.sh`

---

## 🔄 Update Process

```bash
# 1. Backup database (if needed)
pg_dump $DATABASE_URL > backup.sql

# 2. Deploy new version
git push origin main  # Auto-deploys on Render

# 3. Run migrations (if any)
python migrate.py

# 4. Test deployment
python docs/scripts/test_api.sh production

# 5. Monitor for issues
tail -f logs/application.log
```

---

**Successfully deployed? Your VeroctaAI backend is now ready for production! 🚀**

*For additional support, contact the development team or create an issue on GitHub.*