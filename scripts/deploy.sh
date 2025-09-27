#!/bin/bash
# Production Deployment Script for VeroctaAI Backend
# Usage: ./deploy.sh [environment]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default environment
ENVIRONMENT=${1:-production}

echo -e "${BLUE}🚀 VeroctaAI Production Deployment Script${NC}"
echo -e "${BLUE}==========================================${NC}"
echo -e "Environment: ${YELLOW}$ENVIRONMENT${NC}"
echo ""

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    print_error "app.py not found. Please run this script from the VeroctaAI-Backend directory."
    exit 1
fi

print_status "Found app.py - in correct directory"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

print_status "Docker is installed"

# Check required files
print_info "Checking production files..."
required_files=("app.py" "requirements.txt" "Dockerfile" "render.yaml")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_status "$file found"
    else
        print_error "$file missing"
        exit 1
    fi
done

# Check if .env file exists
if [ ! -f ".env" ]; then
    if [ -f ".env.production" ]; then
        print_warning "No .env file found. Using .env.production as template."
        cp .env.production .env
        print_info "Please edit .env file with your actual values before deploying."
    else
        print_warning "No environment file found. Please create .env file with your configuration."
    fi
fi

# Validate requirements.txt
print_info "Validating requirements.txt..."
if grep -q "gunicorn" requirements.txt; then
    print_status "Gunicorn found in requirements"
else
    print_error "Gunicorn missing from requirements"
    exit 1
fi

if grep -q "flask" requirements.txt; then
    print_status "Flask found in requirements"
else
    print_error "Flask missing from requirements"
    exit 1
fi

# Validate Dockerfile
print_info "Validating Dockerfile..."
if grep -q "gunicorn" Dockerfile; then
    print_status "Dockerfile uses Gunicorn"
else
    print_error "Dockerfile doesn't use Gunicorn"
    exit 1
fi

# Validate render.yaml
print_info "Validating render.yaml..."
if grep -q "healthCheckPath: /api/health" render.yaml; then
    print_status "Health check path configured"
else
    print_error "Health check path not configured"
    exit 1
fi

# Build Docker image
print_info "Building Docker image..."
if docker build -t veroctai-backend:latest -t veroctai-backend:$ENVIRONMENT .; then
    print_status "Docker image built successfully"
else
    print_error "Failed to build Docker image"
    exit 1
fi

# Test the build
print_info "Testing Docker image..."
if docker run --rm veroctai-backend:latest python -c "import app; print('✅ App imports successfully')"; then
    print_status "Docker image test passed"
else
    print_error "Docker image test failed"
    exit 1
fi

# Run local test (optional)
if [ "$ENVIRONMENT" == "test" ] || [ "$2" == "--test" ]; then
    print_info "Starting local test server..."
    
    # Kill any existing containers
    docker stop veroctai-test 2>/dev/null || true
    docker rm veroctai-test 2>/dev/null || true
    
    # Start test container
    docker run -d \
        --name veroctai-test \
        --env-file .env \
        -p 8000:10000 \
        veroctai-backend:latest
    
    # Wait for container to start
    sleep 10
    
    # Test health endpoint
    if curl -f http://localhost:8000/api/health; then
        print_status "Local test server is healthy"
        echo ""
        print_info "Test server running at: http://localhost:8000"
        print_info "Health check: http://localhost:8000/api/health"
        print_info ""
        print_info "To stop test server: docker stop veroctai-test"
    else
        print_error "Local test server health check failed"
        docker logs veroctai-test
        docker stop veroctai-test
        docker rm veroctai-test
        exit 1
    fi
else
    print_info "Skipping local test. Use './deploy.sh test' or add '--test' flag to test locally."
fi

echo ""
print_status "Deployment preparation complete!"
echo ""
print_info "Next steps for Render deployment:"
echo -e "  1. Go to ${BLUE}https://render.com${NC}"
echo -e "  2. Connect your GitHub repository"
echo -e "  3. Create a new Web Service"
echo -e "  4. Use the ${YELLOW}render.yaml${NC} file for automatic configuration"
echo -e "  5. Set environment variables in Render dashboard"
echo -e "  6. Deploy and test at your-service.onrender.com/api/health"
echo ""
print_info "Environment variables to set in Render:"
echo -e "  - ${YELLOW}SESSION_SECRET${NC}: Auto-generated"
echo -e "  - ${YELLOW}JWT_SECRET_KEY${NC}: Auto-generated"
echo -e "  - ${YELLOW}OPENAI_API_KEY${NC}: Your OpenAI API key"
echo -e "  - ${YELLOW}SUPABASE_URL${NC}: Your Supabase URL"
echo -e "  - ${YELLOW}SUPABASE_ANON_KEY${NC}: Your Supabase anon key"
echo -e "  - ${YELLOW}SUPABASE_PASSWORD${NC}: Your database password"
echo ""
print_status "Deployment script completed successfully! 🎉"