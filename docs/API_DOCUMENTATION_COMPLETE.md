# 📡 VeroctaAI Complete API Documentation

**Version**: 2.0.0  
**Base URL**: 
- Development: `http://localhost:8001`  
- Production: `https://veroctaai.onrender.com`

---

## 📋 Table of Contents

1. [Authentication](#-authentication)
2. [Health & System](#-health--system)
3. [File Upload & Processing](#-file-upload--processing)
4. [Reports Management](#-reports-management)
5. [Analytics & Insights](#-analytics--insights)
6. [User Management](#-user-management)
7. [Dynamic SaaS APIs](#-dynamic-saas-apis)
8. [Error Handling](#-error-handling)
9. [Rate Limiting](#-rate-limiting)
10. [Postman Collection](#-postman-collection)

---

## 🔐 Authentication

### Overview
VeroctaAI uses JWT (JSON Web Token) based authentication. Most endpoints require a valid JWT token in the Authorization header.

### Header Format
```
Authorization: Bearer <jwt_token>
```

### Authentication Endpoints

#### 1. User Registration
**Endpoint**: `POST /api/auth/register`  
**Auth Required**: ❌

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "company": "Example Corp"
}
```

**Response** (200):
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "company": "Example Corp",
    "role": "user",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**cURL Example**:
```bash
curl -X POST https://veroctaai.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123",
    "first_name": "John",
    "last_name": "Doe",
    "company": "Example Corp"
  }'
```

#### 2. User Login
**Endpoint**: `POST /api/auth/login`  
**Auth Required**: ❌

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response** (200):
```json
{
  "success": true,
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "company": "Example Corp",
    "role": "user"
  }
}
```

#### 3. Get Current User
**Endpoint**: `GET /api/auth/me`  
**Auth Required**: ✅

**Response** (200):
```json
{
  "success": true,
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "company": "Example Corp",
    "role": "user",
    "subscription_tier": "free",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### 4. Refresh Token
**Endpoint**: `POST /api/auth/refresh`  
**Auth Required**: ✅ (Refresh Token)

**Headers**:
```
Authorization: Bearer <refresh_token>
```

**Response** (200):
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "message": "Token refreshed successfully"
}
```

#### 5. Logout
**Endpoint**: `POST /api/auth/logout`  
**Auth Required**: ✅

**Response** (200):
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

## 🏥 Health & System

### 1. Health Check
**Endpoint**: `GET /api/health`  
**Auth Required**: ❌

**Response** (200):
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "2.0.0",
  "services": {
    "database": {
      "status": "connected",
      "response_time_ms": 45
    },
    "ai": {
      "status": "available",
      "model": "gpt-4o",
      "response_time_ms": 120
    },
    "storage": {
      "status": "available",
      "free_space_mb": 1024
    }
  },
  "uptime_seconds": 3600,
  "environment": "production"
}
```

### 2. System Information
**Endpoint**: `GET /api/system/info`  
**Auth Required**: ✅ (Admin only)

**Response** (200):
```json
{
  "success": true,
  "system": {
    "version": "2.0.0",
    "python_version": "3.13",
    "flask_version": "3.1.1",
    "database_version": "PostgreSQL 17.6",
    "total_users": 150,
    "total_reports": 1205,
    "total_analyses": 3420
  }
}
```

---

## 📁 File Upload & Processing

### 1. Upload CSV File
**Endpoint**: `POST /api/upload`  
**Auth Required**: ❌  
**Content-Type**: `multipart/form-data`

**Form Data**:
- `file`: CSV file (max 16MB)
- `company_name`: Company name (optional)
- `description`: Report description (optional)

**Supported CSV Formats**:
- QuickBooks Export
- Wave Accounting
- Revolut Business
- Xero Export  
- Generic CSV (auto-detected)

**Response** (200):
```json
{
  "success": true,
  "message": "File processed successfully",
  "report_id": "uuid-here",
  "analysis": {
    "spend_score": 78,
    "total_amount": 15420.50,
    "transaction_count": 145,
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-01-31"
    },
    "categories": {
      "Office Supplies": 2340.50,
      "Marketing": 5100.00,
      "Software": 1980.00,
      "Travel": 6000.00
    },
    "ai_insights": {
      "key_findings": [
        "High spending on travel expenses suggests potential cost optimization",
        "Office supplies show consistent monthly patterns",
        "Software subscriptions could be consolidated"
      ],
      "recommendations": [
        "Consider negotiating volume discounts for travel",
        "Audit software subscriptions for duplicates",
        "Implement expense approval workflow"
      ],
      "potential_savings": 1850.00
    }
  }
}
```

**cURL Example**:
```bash
curl -X POST https://veroctaai.onrender.com/api/upload \
  -F "file=@expenses.csv" \
  -F "company_name=Example Corp" \
  -F "description=Q1 2024 Expenses"
```

---

## 📊 Reports Management

### 1. List User Reports
**Endpoint**: `GET /api/reports`  
**Auth Required**: ✅

**Query Parameters**:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)
- `sort`: Sort field (created_at, spend_score, total_amount)
- `order`: Sort order (asc, desc, default: desc)

**Response** (200):
```json
{
  "success": true,
  "reports": [
    {
      "id": "uuid-here",
      "title": "Q1 2024 Analysis",
      "company": "Example Corp",
      "spend_score": 78,
      "total_amount": 15420.50,
      "transaction_count": 145,
      "status": "completed",
      "created_at": "2024-01-15T10:30:00Z",
      "file_name": "expenses_q1.csv"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 23,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

### 2. Get Specific Report
**Endpoint**: `GET /api/reports/{report_id}`  
**Auth Required**: ✅

**Response** (200):
```json
{
  "success": true,
  "report": {
    "id": "uuid-here",
    "title": "Q1 2024 Analysis",
    "company": "Example Corp",
    "spend_score": 78,
    "total_amount": 15420.50,
    "transaction_count": 145,
    "data": {
      "transactions": [...],
      "categories": {...},
      "vendors": {...}
    },
    "analysis": {
      "metrics": {
        "frequency_score": 85,
        "category_diversity": 72,
        "budget_adherence": 68,
        "redundancy_detection": 90,
        "spike_detection": 75,
        "waste_ratio": 80
      },
      "patterns": {
        "recurring_expenses": [...],
        "outliers": [...],
        "trends": [...]
      }
    },
    "insights": {
      "ai_insights": {...},
      "recommendations": [...],
      "potential_savings": 1850.00,
      "confidence_score": 0.87
    },
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
  }
}
```

### 3. Create Report from Existing Data
**Endpoint**: `POST /api/reports`  
**Auth Required**: ✅

**Request Body**:
```json
{
  "title": "Q2 2024 Analysis",
  "company": "Example Corp",
  "description": "Quarterly expense analysis",
  "data_source": "manual",
  "transactions": [
    {
      "date": "2024-04-01",
      "description": "Office supplies",
      "amount": 150.00,
      "category": "Office"
    }
  ]
}
```

### 4. Delete Report
**Endpoint**: `DELETE /api/reports/{report_id}`  
**Auth Required**: ✅

**Response** (200):
```json
{
  "success": true,
  "message": "Report deleted successfully"
}
```

### 5. Download PDF Report
**Endpoint**: `GET /api/reports/{report_id}/pdf`  
**Auth Required**: ✅  
**Response Type**: `application/pdf`

**Response**: Binary PDF file

**cURL Example**:
```bash
curl -X GET https://veroctaai.onrender.com/api/reports/uuid-here/pdf \
  -H "Authorization: Bearer <token>" \
  -o report.pdf
```

---

## 📈 Analytics & Insights

### 1. Get Spend Score Analysis
**Endpoint**: `GET /api/spend-score`  
**Auth Required**: ✅

**Query Parameters**:
- `report_id`: Specific report ID (optional)
- `period`: Time period (month, quarter, year, default: month)

**Response** (200):
```json
{
  "success": true,
  "spend_score": {
    "overall_score": 78,
    "grade": "B+",
    "color": "amber",
    "metrics": {
      "frequency_score": {
        "value": 85,
        "weight": 0.15,
        "description": "Transaction frequency patterns"
      },
      "category_diversity": {
        "value": 72,
        "weight": 0.10,
        "description": "Spending category distribution"
      },
      "budget_adherence": {
        "value": 68,
        "weight": 0.20,
        "description": "Adherence to budget benchmarks"
      },
      "redundancy_detection": {
        "value": 90,
        "weight": 0.15,
        "description": "Duplicate expense detection"
      },
      "spike_detection": {
        "value": 75,
        "weight": 0.20,
        "description": "Unusual spending pattern detection"
      },
      "waste_ratio": {
        "value": 80,
        "weight": 0.20,
        "description": "Essential vs non-essential spending"
      }
    },
    "recommendations": [
      {
        "category": "cost_optimization",
        "priority": "high",
        "description": "Consolidate software subscriptions",
        "potential_savings": 450.00
      },
      {
        "category": "process_improvement", 
        "priority": "medium",
        "description": "Implement expense approval workflow",
        "potential_savings": 200.00
      }
    ],
    "insights": {
      "total_analyzed": 15420.50,
      "potential_savings": 1850.00,
      "waste_percentage": 12,
      "top_categories": ["Travel", "Marketing", "Office"],
      "risk_factors": ["High travel variability", "Duplicate subscriptions"]
    }
  }
}
```

### 2. Dashboard Statistics
**Endpoint**: `GET /api/dashboard/stats`  
**Auth Required**: ✅

**Response** (200):
```json
{
  "success": true,
  "stats": {
    "overview": {
      "total_reports": 23,
      "total_analyzed": 456789.50,
      "average_spend_score": 76,
      "total_savings_identified": 45670.00
    },
    "recent_activity": [
      {
        "type": "report_created",
        "title": "Q1 2024 Analysis",
        "date": "2024-01-15T10:30:00Z",
        "spend_score": 78
      }
    ],
    "trends": {
      "spend_score_trend": [
        {"month": "Jan", "score": 78},
        {"month": "Feb", "score": 82},
        {"month": "Mar", "score": 75}
      ],
      "spending_trend": [
        {"month": "Jan", "amount": 15420.50},
        {"month": "Feb", "amount": 13890.25},
        {"month": "Mar", "amount": 16750.75}
      ]
    },
    "category_breakdown": {
      "Office Supplies": 15.5,
      "Marketing": 25.2,
      "Software": 18.8,
      "Travel": 40.5
    }
  }
}
```

### 3. Advanced Analytics
**Endpoint**: `GET /api/analytics/advanced`  
**Auth Required**: ✅

**Query Parameters**:
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `categories`: Comma-separated category list
- `include_predictions`: Include AI predictions (true/false)

**Response** (200):
```json
{
  "success": true,
  "analytics": {
    "period": {
      "start": "2024-01-01",
      "end": "2024-03-31",
      "total_days": 90
    },
    "financial_summary": {
      "total_spent": 45670.25,
      "average_daily": 507.45,
      "median_transaction": 125.00,
      "largest_transaction": 5000.00,
      "transaction_count": 347
    },
    "category_analysis": {
      "top_categories": [
        {
          "name": "Travel",
          "amount": 18500.00,
          "percentage": 40.5,
          "transaction_count": 45,
          "trend": "increasing"
        }
      ],
      "category_efficiency": {
        "high_value": ["Software", "Marketing"],
        "optimization_needed": ["Office Supplies", "Miscellaneous"]
      }
    },
    "vendor_analysis": {
      "top_vendors": [
        {
          "name": "Microsoft",
          "amount": 2400.00,
          "transaction_count": 12,
          "category": "Software"
        }
      ],
      "consolidation_opportunities": [
        {
          "category": "Software",
          "vendors": ["Microsoft", "Adobe", "Slack"],
          "potential_savings": 350.00
        }
      ]
    },
    "predictions": {
      "next_month_forecast": 16250.00,
      "confidence_level": 0.85,
      "seasonal_adjustments": {
        "q4_increase": 15.5,
        "holiday_impact": 8.2
      }
    }
  }
}
```

---

## 👤 User Management

### 1. Update User Profile
**Endpoint**: `PUT /api/users/profile`  
**Auth Required**: ✅

**Request Body**:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "company": "Updated Corp",
  "phone": "+1-555-0123",
  "preferences": {
    "currency": "USD",
    "timezone": "America/New_York",
    "notifications": true
  }
}
```

### 2. Change Password
**Endpoint**: `POST /api/users/change-password`  
**Auth Required**: ✅

**Request Body**:
```json
{
  "current_password": "oldPassword123",
  "new_password": "newSecurePassword456"
}
```

### 3. User Analytics
**Endpoint**: `GET /api/users/analytics`  
**Auth Required**: ✅

**Response** (200):
```json
{
  "success": true,
  "user_analytics": {
    "account_age_days": 125,
    "total_reports": 23,
    "total_analyzed": 456789.50,
    "average_spend_score": 76,
    "usage_stats": {
      "api_calls_this_month": 145,
      "reports_this_month": 8,
      "last_login": "2024-01-15T08:30:00Z"
    }
  }
}
```

---

## 🔄 Dynamic SaaS APIs

### 1. Analytics Overview
**Endpoint**: `GET /api/v2/analytics/overview`  
**Auth Required**: ✅

**Response** (200):
```json
{
  "success": true,
  "data": {
    "total_revenue": 125430.50,
    "active_users": 1250,
    "conversion_rate": 3.2,
    "churn_rate": 2.1,
    "mrr": 15600.00,
    "growth_rate": 12.5
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 2. Billing Information
**Endpoint**: `GET /api/v2/billing/current`  
**Auth Required**: ✅

**Response** (200):
```json
{
  "success": true,
  "billing": {
    "current_plan": "Professional",
    "billing_cycle": "monthly",
    "amount": 49.99,
    "currency": "USD",
    "next_billing_date": "2024-02-15",
    "payment_method": "card_ending_4532",
    "usage": {
      "api_calls": 1250,
      "limit": 5000,
      "percentage": 25.0
    }
  }
}
```

### 3. Notifications
**Endpoint**: `GET /api/v2/notifications`  
**Auth Required**: ✅

**Response** (200):
```json
{
  "success": true,
  "notifications": [
    {
      "id": "notif_123",
      "type": "info",
      "title": "New Feature Available",
      "message": "Advanced analytics now available in your dashboard",
      "created_at": "2024-01-15T09:00:00Z",
      "read": false
    },
    {
      "id": "notif_124",
      "type": "warning",
      "title": "Usage Alert",
      "message": "You've used 80% of your monthly API quota",
      "created_at": "2024-01-14T15:30:00Z",
      "read": true
    }
  ],
  "unread_count": 3
}
```

### 4. System Monitoring
**Endpoint**: `GET /api/v2/monitoring/status`  
**Auth Required**: ✅ (Admin only)

**Response** (200):
```json
{
  "success": true,
  "system_status": {
    "overall": "operational",
    "services": {
      "api": {"status": "operational", "uptime": 99.98},
      "database": {"status": "operational", "uptime": 99.95},
      "ai_service": {"status": "operational", "uptime": 99.85},
      "file_processing": {"status": "operational", "uptime": 99.92}
    },
    "performance": {
      "avg_response_time": 145,
      "requests_per_minute": 1250,
      "error_rate": 0.02
    }
  }
}
```

---

## ❌ Error Handling

### Standard Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": "Email is required and must be valid",
    "field": "email"
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "req_123456789"
}
```

### Common Error Codes

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | `VALIDATION_ERROR` | Invalid request data |
| 401 | `AUTHENTICATION_REQUIRED` | Missing or invalid token |
| 403 | `INSUFFICIENT_PERMISSIONS` | User lacks required permissions |
| 404 | `RESOURCE_NOT_FOUND` | Requested resource doesn't exist |
| 409 | `RESOURCE_CONFLICT` | Resource already exists |
| 413 | `FILE_TOO_LARGE` | Uploaded file exceeds size limit |
| 415 | `UNSUPPORTED_MEDIA_TYPE` | Invalid file format |
| 422 | `PROCESSING_ERROR` | Unable to process request |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests |
| 500 | `INTERNAL_SERVER_ERROR` | Server error occurred |
| 503 | `SERVICE_UNAVAILABLE` | Service temporarily unavailable |

### Error Examples

#### Authentication Error
```json
{
  "success": false,
  "error": {
    "code": "AUTHENTICATION_REQUIRED",
    "message": "Authentication token is required",
    "details": "Include 'Authorization: Bearer <token>' header"
  }
}
```

#### Validation Error
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid file format",
    "details": "Only CSV files are supported",
    "field": "file"
  }
}
```

#### Rate Limit Error
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "details": "Maximum 100 requests per minute allowed",
    "retry_after": 45
  }
}
```

---

## 🚦 Rate Limiting

### Default Limits
- **General API**: 100 requests per minute per IP
- **File Upload**: 10 uploads per hour per user
- **Authentication**: 20 login attempts per hour per IP
- **Report Generation**: 50 reports per day per user

### Rate Limit Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 75
X-RateLimit-Reset: 1642262400
X-RateLimit-Window: 60
```

---

## 📮 Postman Collection

### Import Instructions

1. **Download Collection**: [VeroctaAI-API.postman_collection.json](./postman/VeroctaAI-API.postman_collection.json)
2. **Open Postman**
3. **Import** → **Upload Files** → Select downloaded file
4. **Import Environment**: [VeroctaAI-Environment.postman_environment.json](./postman/VeroctaAI-Environment.postman_environment.json)

### Environment Variables

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `base_url` | API base URL | `https://veroctaai.onrender.com` |
| `api_version` | API version | `v2` |
| `access_token` | JWT access token | `eyJ0eXAiOiJKV1Q...` |
| `refresh_token` | JWT refresh token | `eyJ0eXAiOiJKV1Q...` |
| `user_id` | Current user ID | `uuid-here` |

### Collection Structure

```
VeroctaAI API Collection
├── 01 - Authentication
│   ├── Register User
│   ├── Login User
│   ├── Get Current User
│   ├── Refresh Token
│   └── Logout
├── 02 - Health & System
│   ├── Health Check
│   └── System Info
├── 03 - File Upload
│   ├── Upload CSV File
│   └── Upload with Options
├── 04 - Reports
│   ├── List Reports
│   ├── Get Report Details
│   ├── Create Report
│   ├── Delete Report
│   └── Download PDF
├── 05 - Analytics
│   ├── Spend Score Analysis
│   ├── Dashboard Stats
│   └── Advanced Analytics
├── 06 - User Management
│   ├── Update Profile
│   ├── Change Password
│   └── User Analytics
└── 07 - SaaS Platform
    ├── Analytics Overview
    ├── Billing Info
    ├── Notifications
    └── System Monitoring
```

### Pre-request Scripts

The collection includes automatic token management:

```javascript
// Auto-refresh expired tokens
pm.test("Auto-refresh token", function () {
    const token = pm.environment.get("access_token");
    if (token && isTokenExpired(token)) {
        pm.sendRequest({
            url: pm.environment.get("base_url") + "/api/auth/refresh",
            method: "POST",
            header: {
                "Authorization": "Bearer " + pm.environment.get("refresh_token")
            }
        }, function (err, response) {
            if (!err && response.json().success) {
                pm.environment.set("access_token", response.json().access_token);
            }
        });
    }
});
```

---

## 🧪 Testing Examples

### Complete API Test Flow

```bash
#!/bin/bash
# VeroctaAI API Test Script

BASE_URL="https://veroctaai.onrender.com"
EMAIL="test@example.com"
PASSWORD="testPassword123"

echo "🚀 Starting VeroctaAI API Tests..."

# 1. Health Check
echo "1️⃣ Testing Health Endpoint..."
curl -s "$BASE_URL/api/health" | jq .

# 2. User Registration
echo "2️⃣ Registering Test User..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'$EMAIL'",
    "password": "'$PASSWORD'",
    "first_name": "Test",
    "last_name": "User",
    "company": "Test Corp"
  }')

ACCESS_TOKEN=$(echo $REGISTER_RESPONSE | jq -r .access_token)
echo "✅ User registered. Token: ${ACCESS_TOKEN:0:20}..."

# 3. File Upload
echo "3️⃣ Testing File Upload..."
# Create sample CSV
cat > test_expenses.csv << EOF
Date,Description,Amount,Category
2024-01-15,Office supplies,150.00,Office
2024-01-16,Software license,299.99,Software
2024-01-17,Travel expenses,450.00,Travel
EOF

UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/api/upload" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -F "file=@test_expenses.csv" \
  -F "company_name=Test Corp")

REPORT_ID=$(echo $UPLOAD_RESPONSE | jq -r .report_id)
echo "✅ File uploaded. Report ID: $REPORT_ID"

# 4. Get Reports
echo "4️⃣ Fetching Reports..."
curl -s -X GET "$BASE_URL/api/reports" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .

# 5. Spend Score Analysis
echo "5️⃣ Getting Spend Score..."
curl -s -X GET "$BASE_URL/api/spend-score" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .

# 6. Dashboard Stats
echo "6️⃣ Fetching Dashboard Stats..."
curl -s -X GET "$BASE_URL/api/dashboard/stats" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .

# Cleanup
rm test_expenses.csv

echo "🎉 API Tests Completed!"
```

---

## 📞 Support & Resources

- **API Documentation**: `/api/docs`
- **Swagger UI**: `/api/swagger`
- **OpenAPI Spec**: `/api/openapi.json`
- **GitHub Issues**: [Report Issues](https://github.com/jobayehoque/VeroctaAI-Backend/issues)
- **Email Support**: support@verocta.ai

---

**Last Updated**: January 15, 2024  
**API Version**: 2.0.0  
**Documentation Version**: 1.0.0