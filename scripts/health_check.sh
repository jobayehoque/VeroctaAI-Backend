#!/bin/bash
# Production Health Check Script for VeroctaAI Backend
# Usage: ./health_check.sh [URL]

URL=${1:-"http://localhost:10000"}
HEALTH_ENDPOINT="$URL/api/health"
MAX_RETRIES=5
RETRY_DELAY=2

echo "🏥 VeroctaAI Health Check"
echo "========================"
echo "Checking: $HEALTH_ENDPOINT"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Function to check health endpoint
check_health() {
    local attempt=$1
    
    print_info "Attempt $attempt/$MAX_RETRIES..."
    
    # Make request with timeout
    response=$(curl -s -m 10 -w "HTTPSTATUS:%{http_code};TIME:%{time_total}" "$HEALTH_ENDPOINT" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        # Extract HTTP status and response time
        http_status=$(echo "$response" | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
        response_time=$(echo "$response" | grep -o "TIME:[0-9.]*" | cut -d: -f2)
        body=$(echo "$response" | sed -E 's/HTTPSTATUS:[0-9]*;TIME:[0-9.]*$//')
        
        if [ "$http_status" = "200" ]; then
            print_status "Server is healthy!"
            print_info "Response time: ${response_time}s"
            
            # Parse JSON response if available
            if command -v jq &> /dev/null && echo "$body" | jq . &> /dev/null; then
                status=$(echo "$body" | jq -r '.status // "unknown"')
                timestamp=$(echo "$body" | jq -r '.timestamp // "unknown"')
                version=$(echo "$body" | jq -r '.version // "unknown"')
                
                echo "📊 Status: $status"
                echo "⏰ Timestamp: $timestamp"
                echo "🔢 Version: $version"
                
                # Check database status if available
                if echo "$body" | jq -e '.database' &> /dev/null; then
                    db_status=$(echo "$body" | jq -r '.database.status // "unknown"')
                    if [ "$db_status" = "connected" ]; then
                        print_status "Database: Connected"
                    else
                        print_warning "Database: $db_status"
                    fi
                fi
                
                # Check AI service status if available
                if echo "$body" | jq -e '.services.openai' &> /dev/null; then
                    ai_status=$(echo "$body" | jq -r '.services.openai // "unknown"')
                    if [ "$ai_status" = "available" ]; then
                        print_status "AI Service: Available"
                    else
                        print_warning "AI Service: $ai_status"
                    fi
                fi
            else
                echo "📄 Response: $body"
            fi
            
            return 0
        else
            print_error "HTTP $http_status - Server unhealthy"
            echo "📄 Response: $body"
            return 1
        fi
    else
        print_error "Connection failed - Server not responding"
        return 1
    fi
}

# Main health check loop
for i in $(seq 1 $MAX_RETRIES); do
    if check_health $i; then
        echo ""
        print_status "Health check passed! ✨"
        exit 0
    else
        if [ $i -lt $MAX_RETRIES ]; then
            print_warning "Retrying in ${RETRY_DELAY}s..."
            sleep $RETRY_DELAY
            echo ""
        fi
    fi
done

echo ""
print_error "Health check failed after $MAX_RETRIES attempts"
print_info "Troubleshooting steps:"
echo "  1. Check if server is running: docker ps"
echo "  2. Check server logs: docker logs [container-name]"
echo "  3. Verify URL: $HEALTH_ENDPOINT"
echo "  4. Check network connectivity"
echo "  5. Verify environment variables"

exit 1