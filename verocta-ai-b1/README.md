# VeroctaAI Financial Intelligence Platform

A comprehensive financial intelligence platform that provides AI-powered spending analysis, budget optimization, and financial insights for businesses and individuals.

## 🚀 Features

- **AI-Powered Analysis**: Advanced spending pattern analysis using OpenAI
- **Financial Intelligence**: Comprehensive budget analysis and optimization
- **Multi-format Support**: CSV, Excel, and PDF financial data processing
- **Real-time Insights**: Dynamic financial dashboards and reporting
- **Secure Authentication**: JWT-based authentication with bcrypt encryption
- **Cloud Integration**: Supabase database and Google Sheets integration
- **Payment Processing**: Stripe integration for premium features
- **Email Notifications**: Automated report delivery via Resend

## 📁 Project Structure

```
verocta-ai/
├── backend/                    # Python Flask API
│   ├── app/                   # Application setup
│   ├── api/v1/               # API endpoints
│   ├── core/                 # Business logic
│   ├── models/               # Data models
│   ├── utils/                # Utility functions
│   └── tests/                # Backend tests
├── frontend/                  # React frontend
│   ├── src/                  # Source code
│   └── public/               # Static assets
├── docs/                     # Documentation
├── deployment/               # Deployment configs
├── scripts/                  # Utility scripts
└── tests/                    # Integration tests
```

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 3.1.1
- **Database**: PostgreSQL with Supabase
- **Authentication**: JWT with Flask-JWT-Extended
- **AI Integration**: OpenAI GPT API
- **Data Processing**: Pandas, NumPy
- **PDF Generation**: ReportLab

### Frontend
- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **Styling**: Modern CSS with responsive design
- **State Management**: React Hooks

### Infrastructure
- **Containerization**: Docker
- **Database**: Supabase (PostgreSQL)
- **Deployment**: Render, Vercel
- **Monitoring**: Custom logging and health checks

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)

### Backend Setup

1. **Clone and navigate to project**
   ```bash
   cd verocta-ai/backend
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

4. **Environment configuration**
   ```bash
   cp ../.env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python app/main.py
   ```

### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

## 🐳 Docker Deployment

### Development
```bash
docker-compose up --build
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up --build
```

## 📊 API Documentation

The API documentation is available at:
- Development: `http://localhost:5000/docs`
- Production: `https://your-domain.com/docs`

### Key Endpoints
- `POST /api/v1/auth/login` - User authentication
- `POST /api/v1/upload` - File upload for analysis
- `GET /api/v1/analysis/{id}` - Retrieve analysis results
- `POST /api/v1/generate-report` - Generate PDF reports

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SESSION_SECRET` | Flask session secret | ✅ |
| `SUPABASE_URL` | Supabase project URL | ✅ |
| `SUPABASE_ANON_KEY` | Supabase anonymous key | ✅ |
| `OPENAI_API_KEY` | OpenAI API key | ✅ |
| `STRIPE_SECRET_KEY` | Stripe secret key | ✅ |
| `RESEND_API_KEY` | Resend email API key | ✅ |

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📈 Monitoring

The application includes comprehensive monitoring:
- Health check endpoint: `/health`
- Structured logging with configurable levels
- Error tracking and reporting
- Performance metrics

## 🚀 Deployment

### Render Deployment
1. Connect your repository to Render
2. Use the provided `render.yaml` configuration
3. Set environment variables in Render dashboard

### Vercel Deployment (Frontend)
1. Connect repository to Vercel
2. Use the provided `vercel.json` configuration
3. Deploy with automatic CI/CD

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Documentation: [docs/](./docs/)
- Issues: GitHub Issues
- Email: support@veroctaai.com

## 🔄 Version History

- **v2.0.0** - Complete restructure and production readiness
- **v1.x.x** - Legacy versions (deprecated)