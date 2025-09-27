# VeroctaAI Financial Intelligence Platform

## Overview
VeroctaAI is a Flask-based backend API service that provides AI-powered financial intelligence and analytics. This is a backend-only repository where the frontend components have been removed, making it an API-only service.

## Project Status
- ✅ **Backend API**: Running on port 5000 
- ✅ **Dependencies**: All Python packages installed via requirements.txt
- ✅ **Workflow**: Configured to run Flask development server
- ✅ **Deployment**: Configured for autoscale deployment with Gunicorn
- ✅ **Database**: Connected to Supabase PostgreSQL with full persistence
- ⚠️ **AI Features**: OpenAI API key not configured

## Architecture
- **Framework**: Flask 3.1.1 with Flask-CORS and Flask-JWT-Extended
- **Authentication**: JWT-based user management 
- **File Processing**: CSV upload and analysis (QuickBooks, Wave, Revolut, Xero)
- **AI Integration**: OpenAI GPT for financial insights (requires API key)
- **Database**: Configurable with Supabase PostgreSQL or in-memory fallback
- **Deployment**: Gunicorn WSGI server for production

## Key Features
1. **Financial Analysis** - AI-powered spend analysis and insights
2. **File Processing** - CSV upload and data processing
3. **Authentication** - Secure JWT-based user management  
4. **Reports** - Generate and download financial reports
5. **Health Monitoring** - System status and health checks

## API Endpoints
- `GET /` - Landing page with API documentation
- `GET /api/health` - Health check and system status
- `GET /api/docs` - API documentation
- `POST /api/auth/login` - User authentication
- `POST /api/auth/register` - User registration
- `POST /api/upload` - File upload for analysis
- `POST /api/spend-score` - Generate spend analysis
- `GET /api/reports` - List user reports

## Environment Configuration
Required environment variables:
- `SESSION_SECRET` - Flask session secret (configured automatically)

Optional environment variables:
- `OPENAI_API_KEY` - For AI-powered financial insights
- `SUPABASE_URL` - Database connection URL
- `SUPABASE_PASSWORD` - Database password
- `SUPABASE_ANON_KEY` - Supabase anonymous key

## Development Setup
1. Dependencies are automatically installed from requirements.txt
2. Server runs on 0.0.0.0:5000 (accessible via Replit webview)
3. Debug mode enabled in development
4. CORS configured for common development origins

## Deployment Configuration
- **Target**: Autoscale (stateless web service)
- **Command**: `gunicorn --bind 0.0.0.0:5000 --reuse-port app:app`
- **Port**: 5000 (configured for Replit environment)

## File Structure
- `app.py` - Main Flask application and configuration
- `routes.py` - All API route definitions and handlers
- `auth.py` - Authentication and user management
- `database.py` - Database connection and operations
- `models.py` - Data models and report management
- `health.py` - System health monitoring
- `clone_verifier.py` - Project integrity verification
- `csv_parser.py` - CSV file processing utilities
- `gpt_utils.py` - OpenAI integration utilities
- `spend_score_engine.py` - Financial analysis engine
- `pdf_generator.py` - Report PDF generation

## Recent Setup Changes
- Created missing `clone_verifier.py` module for project integrity checks
- Resolved route conflicts between app.py and routes.py
- Configured Flask application to run on 0.0.0.0:5000
- Set up workflow for continuous development server
- Configured deployment settings for production use

## Next Steps
To fully activate all features:
1. Set up Supabase database credentials for data persistence
2. Configure OpenAI API key for AI-powered insights
3. Test all API endpoints with appropriate authentication
4. Deploy to production when ready

## Notes
- This is a backend-only repository; frontend components have been removed
- Server uses development configuration with debug mode enabled
- All routes return JSON responses except the main landing page
- CORS is configured to allow requests from common development origins