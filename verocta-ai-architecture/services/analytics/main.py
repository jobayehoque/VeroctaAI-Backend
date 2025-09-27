"""
VeroctaAI Enterprise Analytics Service v2.0
Advanced ML-powered financial analytics with SpendScore™ engine
"""

import os
import logging
import asyncio
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import redis
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import uvicorn

# ML Libraries
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import tensorflow as tf
from prophet import Prophet
import joblib

# OpenAI Integration
import openai
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/analytics.log')
    ]
)
logger = logging.getLogger(__name__)

# Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://verocta:verocta123@localhost:5432/verocta_enterprise')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    logger.info("✅ OpenAI client initialized")
else:
    openai_client = None
    logger.warning("⚠️ OpenAI API key not provided")

# Database connection
try:
    engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=30)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("✅ Database connection established")
except Exception as e:
    logger.error(f"❌ Database connection failed: {e}")
    engine = None
    SessionLocal = None

# Redis connection
try:
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    logger.info("✅ Redis connection established")
except Exception as e:
    logger.error(f"❌ Redis connection failed: {e}")
    redis_client = None

# Pydantic Models
class TransactionData(BaseModel):
    """Transaction data model"""
    date: str
    amount: float
    vendor: str
    category: str
    description: Optional[str] = None
    account: Optional[str] = None

class SpendScoreRequest(BaseModel):
    """SpendScore calculation request"""
    transactions: List[TransactionData]
    company_id: str
    user_id: str
    analysis_period: Optional[str] = "12_months"

class SpendScoreResponse(BaseModel):
    """SpendScore calculation response"""
    score: float = Field(..., ge=0, le=100)
    tier: str
    breakdown: Dict[str, float]
    insights: List[str]
    recommendations: List[str]
    benchmarks: Dict[str, Any]
    anomalies: List[Dict[str, Any]]
    predictions: Dict[str, Any]

class AnalyticsRequest(BaseModel):
    """Analytics request model"""
    data: List[TransactionData]
    analysis_type: str = "comprehensive"
    company_id: str
    user_id: str

# ML Models (Global variables for caching)
isolation_forest_model = None
prophet_model = None
clustering_model = None
scaler = StandardScaler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 Starting VeroctaAI Enterprise Analytics Service v2.0")
    
    # Load ML models
    await load_ml_models()
    
    yield
    
    logger.info("🛑 Shutting down Analytics Service")

# Create FastAPI app
app = FastAPI(
    title="VeroctaAI Enterprise Analytics Service",
    description="Advanced ML-powered financial analytics with SpendScore™ engine",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def load_ml_models():
    """Load and initialize ML models"""
    global isolation_forest_model, prophet_model, clustering_model
    
    try:
        # Initialize Isolation Forest for anomaly detection
        isolation_forest_model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        
        # Initialize Prophet for time series forecasting
        prophet_model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            seasonality_mode='multiplicative'
        )
        
        # Initialize KMeans for spending pattern clustering
        clustering_model = KMeans(
            n_clusters=5,
            random_state=42,
            n_init=10
        )
        
        logger.info("✅ ML models initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize ML models: {e}")

def calculate_advanced_spend_score(transactions: List[TransactionData]) -> Dict[str, Any]:
    """Calculate advanced SpendScore with ML algorithms"""
    
    if not transactions:
        return {
            "score": 0,
            "tier": "No Data",
            "breakdown": {},
            "insights": ["No transaction data available"],
            "recommendations": ["Upload financial data to get started"],
            "benchmarks": {},
            "anomalies": [],
            "predictions": {}
        }
    
    # Convert to DataFrame
    df = pd.DataFrame([t.dict() for t in transactions])
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df.dropna()
    
    if len(df) < 3:
        return {
            "score": 0,
            "tier": "Insufficient Data",
            "breakdown": {},
            "insights": ["Insufficient data for analysis (minimum 3 transactions required)"],
            "recommendations": ["Upload more transaction data"],
            "benchmarks": {},
            "anomalies": [],
            "predictions": {}
        }
    
    # Calculate base metrics
    total_amount = df['amount'].sum()
    avg_transaction = df['amount'].mean()
    transaction_count = len(df)
    date_range = (df['date'].max() - df['date'].min()).days
    
    # Category analysis
    category_analysis = df.groupby('category')['amount'].agg(['sum', 'count', 'mean']).reset_index()
    category_analysis['percentage'] = (category_analysis['sum'] / total_amount * 100).round(2)
    
    # Vendor analysis
    vendor_analysis = df.groupby('vendor')['amount'].agg(['sum', 'count']).reset_index()
    vendor_analysis['percentage'] = (vendor_analysis['sum'] / total_amount * 100).round(2)
    
    # Time-based analysis
    df['month'] = df['date'].dt.to_period('M')
    monthly_spending = df.groupby('month')['amount'].sum()
    
    # Calculate SpendScore components
    score_components = {}
    
    # 1. Spending Efficiency (30% weight)
    # Lower variance in spending is better
    spending_variance = monthly_spending.var() if len(monthly_spending) > 1 else 0
    efficiency_score = max(0, 100 - (spending_variance / total_amount * 100))
    score_components['efficiency'] = efficiency_score * 0.3
    
    # 2. Category Diversity (25% weight)
    # More categories with balanced spending is better
    category_count = len(category_analysis)
    category_balance = 1 - category_analysis['percentage'].std() / 100
    diversity_score = min(100, (category_count * 10) + (category_balance * 50))
    score_components['diversity'] = diversity_score * 0.25
    
    # 3. Vendor Management (20% weight)
    # Fewer vendors with higher average spending is better
    vendor_count = len(vendor_analysis)
    avg_vendor_spending = vendor_analysis['sum'].mean()
    vendor_score = min(100, (avg_vendor_spending / total_amount * 1000) - (vendor_count * 2))
    score_components['vendor_management'] = max(0, vendor_score) * 0.2
    
    # 4. Transaction Frequency (15% weight)
    # Regular transactions are better
    if date_range > 0:
        frequency_score = min(100, (transaction_count / date_range) * 30)
    else:
        frequency_score = 50
    score_components['frequency'] = frequency_score * 0.15
    
    # 5. Amount Consistency (10% weight)
    # Consistent transaction amounts are better
    amount_std = df['amount'].std()
    amount_mean = df['amount'].mean()
    consistency_score = max(0, 100 - (amount_std / amount_mean * 100)) if amount_mean > 0 else 0
    score_components['consistency'] = consistency_score * 0.1
    
    # Calculate final score
    final_score = sum(score_components.values())
    final_score = max(0, min(100, final_score))
    
    # Determine tier
    if final_score >= 90:
        tier = "Excellent"
    elif final_score >= 80:
        tier = "Very Good"
    elif final_score >= 70:
        tier = "Good"
    elif final_score >= 60:
        tier = "Fair"
    else:
        tier = "Needs Improvement"
    
    # Generate insights
    insights = []
    if efficiency_score < 70:
        insights.append("Spending patterns show high variance - consider budget planning")
    if diversity_score < 60:
        insights.append("Limited category diversity - explore new spending categories")
    if vendor_score < 60:
        insights.append("Consider consolidating vendors for better rates")
    
    # Generate recommendations
    recommendations = []
    if final_score < 80:
        recommendations.append("Implement automated expense categorization")
        recommendations.append("Set up budget alerts for key categories")
        recommendations.append("Review vendor contracts for better terms")
    
    # Anomaly detection
    anomalies = []
    if isolation_forest_model and len(df) > 10:
        try:
            # Prepare features for anomaly detection
            features = df[['amount']].values
            anomaly_scores = isolation_forest_model.fit_predict(features)
            anomaly_indices = np.where(anomaly_scores == -1)[0]
            
            for idx in anomaly_indices:
                transaction = df.iloc[idx]
                anomalies.append({
                    "date": transaction['date'].isoformat(),
                    "amount": float(transaction['amount']),
                    "vendor": transaction['vendor'],
                    "reason": "Unusual spending amount"
                })
        except Exception as e:
            logger.warning(f"Anomaly detection failed: {e}")
    
    # Predictions
    predictions = {}
    if prophet_model and len(monthly_spending) >= 3:
        try:
            # Prepare data for Prophet
            prophet_df = monthly_spending.reset_index()
            prophet_df.columns = ['ds', 'y']
            prophet_df['ds'] = prophet_df['ds'].dt.to_timestamp()
            
            # Fit model and make predictions
            model = Prophet()
            model.fit(prophet_df)
            future = model.make_future_dataframe(periods=3, freq='M')
            forecast = model.predict(future)
            
            predictions = {
                "next_3_months": forecast.tail(3)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict('records'),
                "trend": "increasing" if forecast['yhat'].iloc[-1] > forecast['yhat'].iloc[-4] else "decreasing"
            }
        except Exception as e:
            logger.warning(f"Prediction failed: {e}")
    
    return {
        "score": round(final_score, 2),
        "tier": tier,
        "breakdown": {k: round(v, 2) for k, v in score_components.items()},
        "insights": insights,
        "recommendations": recommendations,
        "benchmarks": {
            "industry_average": 75,
            "top_percentile": 90,
            "your_percentile": min(100, max(0, final_score))
        },
        "anomalies": anomalies,
        "predictions": predictions
    }

async def generate_ai_insights(transactions: List[TransactionData], spend_score: float) -> List[str]:
    """Generate AI-powered insights using OpenAI"""
    
    if not openai_client:
        return ["AI insights not available - OpenAI API key not configured"]
    
    try:
        # Prepare transaction summary
        total_amount = sum(t.amount for t in transactions)
        categories = list(set(t.category for t in transactions))
        vendors = list(set(t.vendor for t in transactions))
        
        prompt = f"""
        Analyze the following financial data and provide 3-5 actionable insights:
        
        - Total Amount: ${total_amount:,.2f}
        - Number of Transactions: {len(transactions)}
        - Categories: {', '.join(categories)}
        - Top Vendors: {', '.join(vendors[:5])}
        - SpendScore: {spend_score}/100
        
        Provide specific, actionable recommendations for improving financial efficiency.
        Focus on cost savings, process improvements, and financial optimization.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a financial analyst providing insights for business expense optimization."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        insights = response.choices[0].message.content.strip().split('\n')
        return [insight.strip('- ').strip() for insight in insights if insight.strip()]
        
    except Exception as e:
        logger.error(f"AI insights generation failed: {e}")
        return ["AI insights temporarily unavailable"]

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "ml_models_loaded": isolation_forest_model is not None,
        "openai_available": openai_client is not None
    }

@app.post("/api/v2/analytics/spend-score", response_model=SpendScoreResponse)
async def calculate_spend_score(request: SpendScoreRequest):
    """Calculate advanced SpendScore with ML algorithms"""
    
    try:
        # Calculate SpendScore
        result = calculate_advanced_spend_score(request.transactions)
        
        # Generate AI insights
        if openai_client:
            ai_insights = await generate_ai_insights(request.transactions, result['score'])
            result['insights'].extend(ai_insights)
        
        # Cache result in Redis
        if redis_client:
            cache_key = f"spend_score:{request.company_id}:{request.user_id}"
            redis_client.setex(cache_key, 3600, json.dumps(result))
        
        return SpendScoreResponse(**result)
        
    except Exception as e:
        logger.error(f"SpendScore calculation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/v2/analytics/comprehensive")
async def comprehensive_analysis(request: AnalyticsRequest):
    """Perform comprehensive financial analysis"""
    
    try:
        # Calculate SpendScore
        spend_score_result = calculate_advanced_spend_score(request.data)
        
        # Additional analysis
        df = pd.DataFrame([t.dict() for t in request.data])
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        # Category breakdown
        category_breakdown = df.groupby('category')['amount'].sum().to_dict()
        
        # Monthly trends
        df['month'] = df['date'].dt.to_period('M')
        monthly_trends = df.groupby('month')['amount'].sum().to_dict()
        
        # Vendor analysis
        vendor_analysis = df.groupby('vendor')['amount'].agg(['sum', 'count']).to_dict()
        
        return {
            "spend_score": spend_score_result,
            "category_breakdown": category_breakdown,
            "monthly_trends": monthly_trends,
            "vendor_analysis": vendor_analysis,
            "summary": {
                "total_amount": float(df['amount'].sum()),
                "transaction_count": len(df),
                "date_range": {
                    "start": df['date'].min().isoformat(),
                    "end": df['date'].max().isoformat()
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Comprehensive analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/v2/analytics/benchmarks")
async def get_benchmarks():
    """Get industry benchmarks"""
    
    return {
        "industry_averages": {
            "spend_score": 75,
            "category_diversity": 8,
            "vendor_consolidation": 0.3,
            "monthly_variance": 0.15
        },
        "top_percentile": {
            "spend_score": 90,
            "category_diversity": 12,
            "vendor_consolidation": 0.1,
            "monthly_variance": 0.05
        },
        "benchmark_categories": [
            "Software & SaaS",
            "Office Supplies",
            "Marketing & Advertising",
            "Travel & Entertainment",
            "Professional Services",
            "Utilities",
            "Insurance",
            "Legal & Compliance"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=os.getenv("RELOAD", "false").lower() == "true",
        log_level="info"
    )
