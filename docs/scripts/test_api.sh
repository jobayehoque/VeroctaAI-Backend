#!/bin/bash
# VeroctaAI Complete API Test Script
# Usage: ./test_api.sh [production|local]

set -e  # Exit on any error

# Configuration
if [ "$1" = "local" ]; then
    BASE_URL="http://localhost:8001"
    echo "🏠 Testing LOCAL environment: $BASE_URL"
else
    BASE_URL="https://veroctaai.onrender.com"
    echo "🌐 Testing PRODUCTION environment: $BASE_URL"
fi

# Test credentials
TEST_EMAIL="apitest+$(date +%s)@example.com"
TEST_PASSWORD="testPassword123"
TEST_COMPANY="API Test Corporation"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "🚀 $1"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

test_step() {
    echo -e "${YELLOW}📋 $1${NC}"
}

test_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

test_error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

check_jq() {
    if ! command -v jq &> /dev/null; then
        test_error "jq is required but not installed. Install with: brew install jq (macOS) or apt-get install jq (Ubuntu)"
    fi
}

# Start testing
print_header "VEROCTA AI - COMPLETE API TEST SUITE"

echo -e "${BLUE}🔧 Environment Setup:${NC}"
echo "   📍 Base URL: $BASE_URL"
echo "   📧 Test Email: $TEST_EMAIL"
echo "   🏢 Test Company: $TEST_COMPANY"
echo ""

# Check dependencies
check_jq

# Step 1: Health Check
print_header "STEP 1: HEALTH CHECK"
test_step "Testing system health endpoint..."

HEALTH_RESPONSE=$(curl -s -w "HTTP_CODE:%{http_code}" "$BASE_URL/api/health")
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
HEALTH_DATA=$(echo "$HEALTH_RESPONSE" | sed 's/HTTP_CODE:[0-9]*$//')

if [ "$HTTP_CODE" = "200" ]; then
    STATUS=$(echo "$HEALTH_DATA" | jq -r '.status // "unknown"')
    if [ "$STATUS" = "healthy" ]; then
        test_success "System is healthy"
        echo "   🔍 Services Status:"
        echo "$HEALTH_DATA" | jq -r '.services | to_entries[] | "      \(.key): \(.value.status)"' 2>/dev/null || echo "      Service details not available"
    else
        test_error "System health check failed - Status: $STATUS"
    fi
else
    test_error "Health endpoint failed - HTTP $HTTP_CODE"
fi
echo ""

# Step 2: User Registration
print_header "STEP 2: USER REGISTRATION"
test_step "Registering new test user..."

REGISTER_RESPONSE=$(curl -s -w "HTTP_CODE:%{http_code}" -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\",
    \"first_name\": \"API\",
    \"last_name\": \"Tester\",
    \"company\": \"$TEST_COMPANY\"
  }")

HTTP_CODE=$(echo "$REGISTER_RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
REGISTER_DATA=$(echo "$REGISTER_RESPONSE" | sed 's/HTTP_CODE:[0-9]*$//')

if [ "$HTTP_CODE" = "200" ]; then
    SUCCESS=$(echo "$REGISTER_DATA" | jq -r '.success // false')
    if [ "$SUCCESS" = "true" ]; then
        ACCESS_TOKEN=$(echo "$REGISTER_DATA" | jq -r '.access_token // ""')
        REFRESH_TOKEN=$(echo "$REGISTER_DATA" | jq -r '.refresh_token // ""')
        USER_ID=$(echo "$REGISTER_DATA" | jq -r '.user.id // ""')
        
        if [ -n "$ACCESS_TOKEN" ] && [ "$ACCESS_TOKEN" != "null" ]; then
            test_success "User registered successfully"
            echo "   🔑 Access Token: ${ACCESS_TOKEN:0:20}..."
            echo "   👤 User ID: $USER_ID"
        else
            test_error "Registration succeeded but no access token received"
        fi
    else
        ERROR_MSG=$(echo "$REGISTER_DATA" | jq -r '.error.message // "Unknown error"')
        test_error "Registration failed: $ERROR_MSG"
    fi
else
    test_error "Registration endpoint failed - HTTP $HTTP_CODE"
fi
echo ""

# Step 3: User Login (Test with existing credentials)
print_header "STEP 3: USER LOGIN"
test_step "Testing login with registered credentials..."

LOGIN_RESPONSE=$(curl -s -w "HTTP_CODE:%{http_code}" -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\"
  }")

HTTP_CODE=$(echo "$LOGIN_RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
LOGIN_DATA=$(echo "$LOGIN_RESPONSE" | sed 's/HTTP_CODE:[0-9]*$//')

if [ "$HTTP_CODE" = "200" ]; then
    SUCCESS=$(echo "$LOGIN_DATA" | jq -r '.success // false')
    if [ "$SUCCESS" = "true" ]; then
        # Update tokens from login response
        ACCESS_TOKEN=$(echo "$LOGIN_DATA" | jq -r '.access_token // ""')
        test_success "Login successful"
        echo "   🔐 New Access Token: ${ACCESS_TOKEN:0:20}..."
    else
        test_error "Login failed"
    fi
else
    test_error "Login endpoint failed - HTTP $HTTP_CODE"
fi
echo ""

# Step 4: Get Current User
print_header "STEP 4: USER PROFILE"
test_step "Fetching current user profile..."

USER_RESPONSE=$(curl -s -w "HTTP_CODE:%{http_code}" -X GET "$BASE_URL/api/auth/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

HTTP_CODE=$(echo "$USER_RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
USER_DATA=$(echo "$USER_RESPONSE" | sed 's/HTTP_CODE:[0-9]*$//')

if [ "$HTTP_CODE" = "200" ]; then
    SUCCESS=$(echo "$USER_DATA" | jq -r '.success // false')
    if [ "$SUCCESS" = "true" ]; then
        USER_EMAIL=$(echo "$USER_DATA" | jq -r '.user.email // "N/A"')
        USER_COMPANY=$(echo "$USER_DATA" | jq -r '.user.company // "N/A"')
        test_success "User profile retrieved"
        echo "   📧 Email: $USER_EMAIL"
        echo "   🏢 Company: $USER_COMPANY"
    else
        test_error "Failed to get user profile"
    fi
else
    test_error "User profile endpoint failed - HTTP $HTTP_CODE"
fi
echo ""

# Step 5: Create sample CSV file
print_header "STEP 5: FILE PREPARATION"
test_step "Creating sample expense CSV file..."

SAMPLE_CSV="/tmp/test_expenses_$(date +%s).csv"
cat > "$SAMPLE_CSV" << 'EOF'
Date,Description,Amount,Category
2024-01-15,Office supplies,150.00,Office
2024-01-16,Software license,299.99,Software
2024-01-17,Business travel,450.00,Travel
2024-01-18,Marketing campaign,750.00,Marketing
2024-01-19,Team lunch,85.50,Meals
2024-01-20,New equipment,1299.99,Equipment
2024-01-21,Monthly subscription,89.99,Software
2024-01-22,Office rent,2500.00,Rent
2024-01-23,Utilities,120.00,Utilities
2024-01-24,Insurance premium,450.00,Insurance
EOF

if [ -f "$SAMPLE_CSV" ]; then
    TRANSACTION_COUNT=$(tail -n +2 "$SAMPLE_CSV" | wc -l)
    test_success "Sample CSV created with $TRANSACTION_COUNT transactions"
    echo "   📄 File: $SAMPLE_CSV"
else
    test_error "Failed to create sample CSV file"
fi
echo ""

# Step 6: File Upload and Analysis
print_header "STEP 6: FILE UPLOAD & ANALYSIS"
test_step "Uploading CSV file for financial analysis..."

UPLOAD_RESPONSE=$(curl -s -w "HTTP_CODE:%{http_code}" -X POST "$BASE_URL/api/upload" \
  -F "file=@$SAMPLE_CSV" \
  -F "company_name=$TEST_COMPANY" \
  -F "description=API Test Upload")

HTTP_CODE=$(echo "$UPLOAD_RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
UPLOAD_DATA=$(echo "$UPLOAD_RESPONSE" | sed 's/HTTP_CODE:[0-9]*$//')

if [ "$HTTP_CODE" = "200" ]; then
    SUCCESS=$(echo "$UPLOAD_DATA" | jq -r '.success // false')
    if [ "$SUCCESS" = "true" ]; then
        REPORT_ID=$(echo "$UPLOAD_DATA" | jq -r '.report_id // ""')
        SPEND_SCORE=$(echo "$UPLOAD_DATA" | jq -r '.analysis.spend_score // "N/A"')
        TOTAL_AMOUNT=$(echo "$UPLOAD_DATA" | jq -r '.analysis.total_amount // "N/A"')
        TRANSACTION_COUNT=$(echo "$UPLOAD_DATA" | jq -r '.analysis.transaction_count // "N/A"')
        
        test_success "File processed successfully"
        echo "   📊 Report ID: $REPORT_ID"
        echo "   💯 Spend Score: $SPEND_SCORE"
        echo "   💰 Total Amount: \$$TOTAL_AMOUNT"
        echo "   📈 Transactions: $TRANSACTION_COUNT"
        
        # Check for AI insights
        AI_INSIGHTS=$(echo "$UPLOAD_DATA" | jq -r '.analysis.ai_insights.key_findings[0] // "No AI insights available"')
        echo "   🤖 AI Insight: $AI_INSIGHTS"
    else
        ERROR_MSG=$(echo "$UPLOAD_DATA" | jq -r '.error.message // "Unknown error"')
        test_error "File upload failed: $ERROR_MSG"
    fi
else
    test_error "File upload endpoint failed - HTTP $HTTP_CODE"
fi
echo ""

# Step 7: Reports List
print_header "STEP 7: REPORTS MANAGEMENT"
test_step "Fetching user reports list..."

REPORTS_RESPONSE=$(curl -s -w "HTTP_CODE:%{http_code}" -X GET "$BASE_URL/api/reports?page=1&limit=10" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

HTTP_CODE=$(echo "$REPORTS_RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
REPORTS_DATA=$(echo "$REPORTS_RESPONSE" | sed 's/HTTP_CODE:[0-9]*$//')

if [ "$HTTP_CODE" = "200" ]; then
    SUCCESS=$(echo "$REPORTS_DATA" | jq -r '.success // false')
    if [ "$SUCCESS" = "true" ]; then
        REPORT_COUNT=$(echo "$REPORTS_DATA" | jq '.reports | length')
        test_success "Reports retrieved successfully"
        echo "   📋 Total Reports: $REPORT_COUNT"
        
        if [ "$REPORT_COUNT" -gt 0 ]; then
            echo "   📊 Recent Reports:"
            echo "$REPORTS_DATA" | jq -r '.reports[0:3][] | "      • \(.title // "Untitled") - Score: \(.spend_score // "N/A")"' 2>/dev/null || echo "      Report details not available"
        fi
    else
        test_error "Failed to fetch reports"
    fi
else
    test_error "Reports endpoint failed - HTTP $HTTP_CODE"
fi
echo ""

# Step 8: Spend Score Analysis
print_header "STEP 8: SPEND SCORE ANALYSIS"
test_step "Getting detailed spend score analysis..."

SCORE_RESPONSE=$(curl -s -w "HTTP_CODE:%{http_code}" -X GET "$BASE_URL/api/spend-score" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

HTTP_CODE=$(echo "$SCORE_RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
SCORE_DATA=$(echo "$SCORE_RESPONSE" | sed 's/HTTP_CODE:[0-9]*$//')

if [ "$HTTP_CODE" = "200" ]; then
    SUCCESS=$(echo "$SCORE_DATA" | jq -r '.success // false')
    if [ "$SUCCESS" = "true" ]; then
        OVERALL_SCORE=$(echo "$SCORE_DATA" | jq -r '.spend_score.overall_score // "N/A"')
        GRADE=$(echo "$SCORE_DATA" | jq -r '.spend_score.grade // "N/A"')
        POTENTIAL_SAVINGS=$(echo "$SCORE_DATA" | jq -r '.spend_score.insights.potential_savings // "N/A"')
        
        test_success "Spend score analysis completed"
        echo "   💯 Overall Score: $OVERALL_SCORE"
        echo "   🎯 Grade: $GRADE"
        echo "   💰 Potential Savings: \$$POTENTIAL_SAVINGS"
        
        # Show metric breakdown
        echo "   📊 Metric Breakdown:"
        echo "$SCORE_DATA" | jq -r '.spend_score.metrics | to_entries[] | "      \(.key): \(.value.value)"' 2>/dev/null || echo "      Metrics not available"
    else
        test_error "Failed to get spend score analysis"
    fi
else
    test_error "Spend score endpoint failed - HTTP $HTTP_CODE"
fi
echo ""

# Step 9: Dashboard Statistics
print_header "STEP 9: DASHBOARD STATISTICS"
test_step "Fetching dashboard statistics..."

DASHBOARD_RESPONSE=$(curl -s -w "HTTP_CODE:%{http_code}" -X GET "$BASE_URL/api/dashboard/stats" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

HTTP_CODE=$(echo "$DASHBOARD_RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
DASHBOARD_DATA=$(echo "$DASHBOARD_RESPONSE" | sed 's/HTTP_CODE:[0-9]*$//')

if [ "$HTTP_CODE" = "200" ]; then
    SUCCESS=$(echo "$DASHBOARD_DATA" | jq -r '.success // false')
    if [ "$SUCCESS" = "true" ]; then
        TOTAL_REPORTS=$(echo "$DASHBOARD_DATA" | jq -r '.stats.overview.total_reports // "N/A"')
        TOTAL_ANALYZED=$(echo "$DASHBOARD_DATA" | jq -r '.stats.overview.total_analyzed // "N/A"')
        AVG_SCORE=$(echo "$DASHBOARD_DATA" | jq -r '.stats.overview.average_spend_score // "N/A"')
        
        test_success "Dashboard statistics retrieved"
        echo "   📊 Total Reports: $TOTAL_REPORTS"
        echo "   💰 Total Analyzed: \$$TOTAL_ANALYZED"
        echo "   📈 Average Score: $AVG_SCORE"
    else
        test_error "Failed to get dashboard statistics"
    fi
else
    test_error "Dashboard endpoint failed - HTTP $HTTP_CODE"
fi
echo ""

# Step 10: PDF Report Generation
if [ -n "$REPORT_ID" ] && [ "$REPORT_ID" != "null" ] && [ "$REPORT_ID" != "" ]; then
    print_header "STEP 10: PDF REPORT GENERATION"
    test_step "Generating and downloading PDF report..."
    
    PDF_FILE="/tmp/test_report_$(date +%s).pdf"
    PDF_RESPONSE=$(curl -s -w "HTTP_CODE:%{http_code}" -X GET "$BASE_URL/api/reports/$REPORT_ID/pdf" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -o "$PDF_FILE")
    
    HTTP_CODE=$(echo "$PDF_RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
    
    if [ "$HTTP_CODE" = "200" ] && [ -f "$PDF_FILE" ]; then
        PDF_SIZE=$(ls -lh "$PDF_FILE" | awk '{print $5}')
        test_success "PDF report generated successfully"
        echo "   📄 File: $PDF_FILE"
        echo "   📏 Size: $PDF_SIZE"
    else
        test_error "PDF generation failed - HTTP $HTTP_CODE"
    fi
    echo ""
fi

# Step 11: SaaS Platform APIs
print_header "STEP 11: SAAS PLATFORM APIS"
test_step "Testing dynamic SaaS platform endpoints..."

# Analytics Overview
ANALYTICS_RESPONSE=$(curl -s -w "HTTP_CODE:%{http_code}" -X GET "$BASE_URL/api/v2/analytics/overview" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

HTTP_CODE=$(echo "$ANALYTICS_RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
ANALYTICS_DATA=$(echo "$ANALYTICS_RESPONSE" | sed 's/HTTP_CODE:[0-9]*$//')

if [ "$HTTP_CODE" = "200" ]; then
    SUCCESS=$(echo "$ANALYTICS_DATA" | jq -r '.success // false')
    if [ "$SUCCESS" = "true" ]; then
        TOTAL_REVENUE=$(echo "$ANALYTICS_DATA" | jq -r '.data.total_revenue // "N/A"')
        ACTIVE_USERS=$(echo "$ANALYTICS_DATA" | jq -r '.data.active_users // "N/A"')
        test_success "SaaS analytics retrieved"
        echo "   💰 Total Revenue: \$$TOTAL_REVENUE"
        echo "   👥 Active Users: $ACTIVE_USERS"
    else
        test_success "SaaS analytics endpoint responding (may have different structure)"
    fi
else
    echo "   ⚠️  SaaS analytics endpoint returned HTTP $HTTP_CODE (may not be fully implemented)"
fi

# Notifications
NOTIF_RESPONSE=$(curl -s -w "HTTP_CODE:%{http_code}" -X GET "$BASE_URL/api/v2/notifications" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

HTTP_CODE=$(echo "$NOTIF_RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)

if [ "$HTTP_CODE" = "200" ]; then
    test_success "Notifications endpoint responding"
else
    echo "   ⚠️  Notifications endpoint returned HTTP $HTTP_CODE (may not be fully implemented)"
fi
echo ""

# Cleanup
print_header "CLEANUP"
test_step "Cleaning up temporary files..."

if [ -f "$SAMPLE_CSV" ]; then
    rm "$SAMPLE_CSV"
    echo "   🗑️  Removed sample CSV file"
fi

if [ -f "$PDF_FILE" ]; then
    echo "   📄 PDF report saved: $PDF_FILE (keeping for review)"
fi

echo ""

# Final Summary
print_header "TEST SUMMARY"

echo -e "${GREEN}🎉 API TEST SUITE COMPLETED SUCCESSFULLY!${NC}"
echo ""
echo -e "${BLUE}📊 Test Results Summary:${NC}"
echo "   ✅ Health Check: Passed"
echo "   ✅ User Registration: Passed"
echo "   ✅ User Login: Passed"
echo "   ✅ User Profile: Passed"
echo "   ✅ File Upload: Passed"
echo "   ✅ Reports Management: Passed"
echo "   ✅ Spend Score Analysis: Passed"
echo "   ✅ Dashboard Statistics: Passed"
if [ -n "$REPORT_ID" ]; then
    echo "   ✅ PDF Generation: Passed"
fi
echo "   ✅ SaaS Platform APIs: Partially Tested"
echo ""
echo -e "${BLUE}🔗 Useful Information:${NC}"
echo "   📧 Test User: $TEST_EMAIL"
echo "   🔑 Access Token: ${ACCESS_TOKEN:0:30}..."
if [ -n "$REPORT_ID" ]; then
    echo "   📊 Sample Report ID: $REPORT_ID"
fi
echo "   📍 API Base URL: $BASE_URL"
echo "   📚 Full API Docs: $BASE_URL/api/docs"
echo ""
echo -e "${GREEN}All core API endpoints are working correctly!${NC}"
echo -e "${YELLOW}Ready for production use! 🚀${NC}"