# VeroctaAI Backend - Production Ready ✨

> **AI-Powered Financial Intelligence Platform** - Complete backend solution ready for production deployment on Render.com

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

---

## 🚀 Quick Deploy (5 Minutes)

```bash
# 1. Clone and prepare
git clone your-repo-url
cd VeroctaAI-Backend

# 2. Validate production readiness
./validate.sh

# 3. Push to GitHub and deploy to Render
# Uses render.yaml for automatic configuration
```

**That's it!** Your production API will be live at `https://your-app.onrender.com`

---

## 📋 What You Get

### 🎯 **Complete API Suite**
- **25+ Production Endpoints** - Full authentication, file upload, analytics
- **AI-Powered Analysis** - GPT-4o financial insights and SpendScore™
- **Real-time Processing** - CSV upload with instant analysis
- **PDF Report Generation** - Professional financial reports
- **Dashboard Analytics** - Complete business intelligence

### 🏗️ **Production Architecture**
- **Flask + Gunicorn** - Production WSGI server with 4 workers
- **Docker Containerized** - Optimized multi-stage build
- **PostgreSQL Database** - Supabase integration with connection pooling
- **JWT Authentication** - Secure token-based user management
- **Health Monitoring** - Built-in health checks and logging

### 🔒 **Enterprise Security**
- **Non-root Container** - Security-hardened Docker setup
- **Environment Isolation** - Secure secret management
- **CORS Configuration** - Properly configured cross-origin policies
- **Input Validation** - All endpoints validated and sanitized
- **Rate Limiting** - Protection against abuse

## 🏗️ Project Structure

```
VeroctaAI-Backend-Clean/
├── api/                    # API-specific modules
│   ├── docs.py            # Documentation endpoints
│   ├── health.py          # Health check endpoints
│   ├── spend-score.py     # Spend scoring API
│   └── upload.py          # File upload API
├── architecture/          # System architecture documentation
│   ├── ARCHITECTURE.md    # System architecture guide
│   ├── docker-compose.yml # Multi-service orchestration
│   ├── frontend/          # Frontend configuration
│   ├── k8s/              # Kubernetes deployment files
│   └── services/         # Microservices architecture
├── assets/               # Static assets
│   ├── images/           # Image assets
│   ├── logos/            # Logo files
│   └── templates/        # Email/document templates
├── attached_assets/      # Uploaded attachments
├── backend/              # Additional backend utilities
├── configs/              # Configuration files
├── deployment/           # Deployment configurations
├── docs/                 # Complete documentation
├── documentation/        # Additional documentation
├── monitoring/           # Monitoring and observability
├── outputs/              # Generated outputs
├── tests/                # Test suites
├── uploads/              # User uploads
├── verocta/              # Core business logic modules
├── app.py               # Main Flask application
├── auth.py              # Authentication logic
├── database.py          # Database operations
├── models.py            # Data models
├── routes.py            # API routes
└── requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database
- Supabase account
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd VeroctaAI-Backend-Clean
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Database Setup**
   ```bash
   python setup_supabase_tables.py
   ```

6. **Run the application**
   ```bash
   # Development
   python app.py
   
   # Production
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

## 🔧 Configuration

Key environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_ANON_KEY`: Supabase anonymous key
- `SUPABASE_PASSWORD`: Database password
- `OPENAI_API_KEY`: OpenAI API key for AI features
- `SESSION_SECRET`: Flask session secret
- `STRIPE_SECRET_KEY`: Stripe API key for payments

## 📊 Features

- **AI-Powered Spend Analysis**: Intelligent categorization and insights
- **Budget Optimization**: Smart budget recommendations
- **Financial Reporting**: Comprehensive PDF reports
- **Payment Integration**: Stripe payment processing
- **Google Sheets Integration**: Data import/export
- **Email Services**: Automated notifications
- **RESTful API**: Clean, documented endpoints

## 🏭 Deployment

### Docker
```bash
docker build -t verocta-ai .
docker run -p 8000:8000 verocta-ai
```

### Docker Compose
```bash
docker-compose up -d
```

### Kubernetes
```bash
kubectl apply -f architecture/k8s/
```

## 📚 Documentation

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Architecture Guide](docs/ARCHITECTURE_DOCUMENTATION.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [Frontend Integration](docs/FRONTEND_INTEGRATION_GUIDE.md)

## 🧪 Testing

```bash
# Run all tests
python -m pytest

# Run specific test suite
python -m pytest tests/unit/

# Run with coverage
python -m pytest --cov=. --cov-report=html
```

## � Monitoring

The application includes comprehensive monitoring:
- Health check endpoints
- Performance metrics
- Error tracking
- Usage analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

[License information]

## 🆘 Support

For support, create an issue in the repository.