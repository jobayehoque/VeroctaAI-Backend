# 🚀 VeroctaAI Backend - Production Deployment Guide

## 📋 Quick Start

The VeroctaAI backend is **production-ready** and optimized for **Render** deployment with Docker containerization.

### ⚡ One-Click Deployment

1. **Deploy to Render**: [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)
2. **Connect GitHub**: Link your repository
3. **Auto-Configuration**: Uses `render.yaml` for automatic setup
4. **Set Environment Variables**: Add your API keys
5. **Deploy**: Click deploy and you're live!

---

## 🏗️ Architecture Overview

```
VeroctaAI Backend
├── 🐍 Python Flask Application
├── 🐳 Docker Containerized
├── 🔒 JWT Authentication
├── 🧠 OpenAI GPT-4o Integration
├── 🗄️ Supabase PostgreSQL Database
├── 📊 Advanced SpendScore™ Engine
├── 📄 PDF Report Generation
├── 🔄 File Processing (CSV)
└── 🌐 RESTful API (25+ endpoints)
```

---

## 🚀 Deployment Options

### Option 1: Render (Recommended)

**Automatic deployment with render.yaml:**

```bash
# 1. Push to GitHub
git add .
git commit -m "Production ready"
git push origin main

# 2. Go to render.com
# 3. Create Web Service
# 4. Connect repository
# 5. Uses render.yaml automatically
# 6. Set environment variables
# 7. Deploy!
```

### Option 2: Manual Docker Deployment

```bash
# Build and test locally
./deploy.sh test

# Build for production
./deploy.sh production

# Deploy to any Docker-compatible platform
docker run -p 10000:10000 --env-file .env veroctai-backend:latest
```

---

## ⚙️ Environment Configuration

### Required Environment Variables

```bash
# Core Application
SESSION_SECRET=your-secure-secret-here
JWT_SECRET_KEY=your-jwt-secret-here
FLASK_ENV=production
PORT=10000

# AI Services (Required)
OPENAI_API_KEY=sk-your-openai-api-key

# Database (Recommended)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_PASSWORD=your-db-password

# Optional Services
STRIPE_SECRET_KEY=sk-your-stripe-key
RESEND_API_KEY=re-your-resend-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 📁 Environment Files

- `.env.production` - Production template with documentation
- `.env.example` - Development template
- Create `.env` with your actual values

---

## 🔧 Production Features

### ✅ Performance Optimizations

- **Gunicorn WSGI Server** with 4 workers
- **Request timeout**: 120 seconds
- **Keep-alive connections**: Optimized
- **Max requests per worker**: 1000 with jitter
- **Preload application**: Faster startup
- **Health checks**: Built-in monitoring

### ✅ Security Features

- **Non-root user**: Container runs as `appuser`
- **JWT Authentication**: Secure token-based auth
- **CORS Configuration**: Properly configured origins
- **Environment isolation**: Secure secret management
- **Input validation**: All endpoints validated

### ✅ Monitoring & Logging

- **Health endpoint**: `/api/health`
- **Structured logging**: JSON format in production
- **Error tracking**: Comprehensive error handling
- **Request logging**: All API calls logged
- **Performance metrics**: Response time tracking

---

## 📊 API Endpoints

### 🏥 System Health
- `GET /api/health` - Health check

### 🔐 Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/refresh` - Refresh token

### 📁 File Processing
- `POST /api/upload` - Upload CSV for analysis
- `GET /api/upload/formats` - Supported formats

### 📊 Reports & Analytics
- `GET /api/reports` - List user reports
- `GET /api/reports/{id}` - Get report details
- `GET /api/reports/{id}/pdf` - Download PDF
- `GET /api/spend-score` - Get SpendScore analysis
- `GET /api/dashboard/stats` - Dashboard statistics

### 🏢 SaaS Platform
- `GET /api/v2/analytics/overview` - Platform analytics
- `GET /api/v2/billing/current` - Billing information
- `GET /api/v2/notifications` - System notifications

**Total: 25+ production-ready endpoints**

---

## 🧪 Testing

### Local Testing

```bash
# Test Docker build
./deploy.sh test

# Health check
curl http://localhost:8000/api/health

# Full API testing
cd docs/scripts
./test_api.sh
```

### Production Testing

```bash
# Health check
curl https://your-app.onrender.com/api/health

# API documentation
https://your-app.onrender.com/api/docs
```

---

## 📦 What's Included

### 🔧 Infrastructure Files
- `Dockerfile` - Optimized multi-stage build
- `render.yaml` - Render deployment configuration
- `deploy.sh` - Production deployment script
- `requirements.txt` - Python dependencies
- `gunicorn.conf.py` - WSGI server configuration

### 📚 Documentation
- `docs/API_DOCUMENTATION_COMPLETE.md` - Complete API docs
- `docs/DEPLOYMENT_GUIDE_COMPLETE.md` - Deployment guide
- `docs/postman/` - Postman collections
- `docs/scripts/` - Testing scripts

### 🧠 Core Features
- Advanced SpendScore™ analytics engine
- AI-powered financial insights
- CSV processing for multiple formats
- PDF report generation
- Real-time dashboard statistics
- Comprehensive user management

---

## 🚨 Troubleshooting

### Common Issues

**1. Docker Build Fails**
```bash
# Clean Docker cache
docker system prune -a
./deploy.sh production
```

**2. Health Check Fails**
```bash
# Check logs
docker logs your-container-name

# Verify environment variables
docker exec -it your-container env
```

**3. Database Connection Issues**
```bash
# Verify Supabase credentials
echo $SUPABASE_URL
echo $SUPABASE_ANON_KEY

# Test connection
python -c "from database import db_service; print(db_service.test_connection())"
```

**4. OpenAI API Issues**
```bash
# Verify API key
echo $OPENAI_API_KEY

# Test API
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

---

## 📈 Performance Metrics

### Expected Performance
- **Response Time**: < 2 seconds (typical)
- **Throughput**: 100+ requests/second
- **Memory Usage**: ~512MB base
- **CPU Usage**: Low to moderate
- **Startup Time**: ~30 seconds

### Scaling Options
- **Horizontal**: Multiple Render instances
- **Vertical**: Upgrade Render plan
- **Database**: Supabase auto-scaling
- **CDN**: Render global CDN

---

## 🌟 Production Checklist

### ✅ Pre-Deployment
- [ ] Environment variables configured
- [ ] OpenAI API key valid
- [ ] Database connection tested
- [ ] Docker build successful
- [ ] Health check passing

### ✅ Post-Deployment
- [ ] Health endpoint responding
- [ ] API authentication working
- [ ] File upload processing
- [ ] PDF generation working
- [ ] Database persistence verified

### ✅ Monitoring
- [ ] Health checks configured
- [ ] Error logging active
- [ ] Performance monitoring
- [ ] Backup strategy in place

---

## 🎯 Quick Commands

```bash
# Build and test
./deploy.sh test

# Production build
./deploy.sh production

# Health check
curl http://localhost:8000/api/health

# View logs
docker logs -f veroctai-backend

# Stop test server
docker stop veroctai-test
```

---

## 🆘 Support

### 📞 Contact
- **Email**: support@verocta.ai
- **GitHub**: Issues tab
- **Documentation**: Complete API docs included

### 🔗 Resources
- **API Documentation**: `/docs/API_DOCUMENTATION_COMPLETE.md`
- **Postman Collection**: `/docs/postman/VeroctaAI-DragDrop-Collection.json`
- **Testing Scripts**: `/docs/scripts/test_api.sh`

---

## 🎉 You're Ready!

Your VeroctaAI backend is **production-ready** with:
- ✅ Complete API suite (25+ endpoints)
- ✅ AI-powered financial analytics
- ✅ Secure authentication system
- ✅ Advanced reporting capabilities
- ✅ Production-optimized deployment
- ✅ Comprehensive documentation
- ✅ Full testing suite

**Deploy to Render in under 5 minutes!** 🚀