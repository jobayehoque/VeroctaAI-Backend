"""
VeroctaAI Enterprise Payment Service v2.0
Stripe integration with multi-currency support and advanced billing features
"""

import os
import logging
import json
import stripe
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
import redis
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/payment.log')
    ]
)
logger = logging.getLogger(__name__)

# Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://verocta:verocta123@localhost:5432/verocta_enterprise')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

# Initialize Stripe
if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY
    logger.info("✅ Stripe API initialized")
else:
    logger.warning("⚠️ Stripe API key not provided")

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
class SubscriptionPlan(BaseModel):
    """Subscription plan model"""
    id: str
    name: str
    description: str
    price: float
    currency: str = "usd"
    interval: str = "month"  # month, year
    features: List[str]
    limits: Dict[str, Any]

class CreateSubscriptionRequest(BaseModel):
    """Create subscription request"""
    customer_id: str
    plan_id: str
    payment_method_id: Optional[str] = None
    trial_period_days: Optional[int] = None
    coupon_code: Optional[str] = None

class UpdateSubscriptionRequest(BaseModel):
    """Update subscription request"""
    subscription_id: str
    plan_id: Optional[str] = None
    quantity: Optional[int] = None
    proration_behavior: str = "create_prorations"

class PaymentMethodRequest(BaseModel):
    """Payment method request"""
    customer_id: str
    payment_method_id: str
    set_as_default: bool = True

class InvoiceRequest(BaseModel):
    """Invoice request"""
    customer_id: str
    amount: float
    currency: str = "usd"
    description: str
    due_date: Optional[datetime] = None

# Subscription Plans Configuration
SUBSCRIPTION_PLANS = {
    "starter": {
        "id": "starter",
        "name": "Starter Plan",
        "description": "Perfect for small businesses getting started",
        "price": 29.99,
        "currency": "usd",
        "interval": "month",
        "features": [
            "Up to 1,000 transactions/month",
            "Basic SpendScore analysis",
            "Email support",
            "Standard reports"
        ],
        "limits": {
            "transactions": 1000,
            "users": 3,
            "reports": 10,
            "integrations": 2
        }
    },
    "professional": {
        "id": "professional",
        "name": "Professional Plan",
        "description": "Advanced features for growing businesses",
        "price": 79.99,
        "currency": "usd",
        "interval": "month",
        "features": [
            "Up to 10,000 transactions/month",
            "Advanced SpendScore with ML insights",
            "Priority support",
            "Custom reports",
            "API access",
            "QuickBooks integration"
        ],
        "limits": {
            "transactions": 10000,
            "users": 10,
            "reports": 50,
            "integrations": 5
        }
    },
    "enterprise": {
        "id": "enterprise",
        "name": "Enterprise Plan",
        "description": "Full-featured solution for large organizations",
        "price": 199.99,
        "currency": "usd",
        "interval": "month",
        "features": [
            "Unlimited transactions",
            "AI-powered insights",
            "Dedicated support",
            "White-label reports",
            "Full API access",
            "All integrations",
            "Custom analytics",
            "SLA guarantee"
        ],
        "limits": {
            "transactions": -1,  # Unlimited
            "users": -1,  # Unlimited
            "reports": -1,  # Unlimited
            "integrations": -1  # Unlimited
        }
    }
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 Starting VeroctaAI Enterprise Payment Service v2.0")
    
    # Initialize Stripe products and prices
    await initialize_stripe_products()
    
    yield
    
    logger.info("🛑 Shutting down Payment Service")

async def initialize_stripe_products():
    """Initialize Stripe products and prices"""
    if not STRIPE_SECRET_KEY:
        logger.warning("⚠️ Stripe not configured - skipping product initialization")
        return
    
    try:
        for plan_id, plan_data in SUBSCRIPTION_PLANS.items():
            # Check if product already exists
            products = stripe.Product.list(limit=100)
            existing_product = None
            
            for product in products.data:
                if product.metadata.get('plan_id') == plan_id:
                    existing_product = product
                    break
            
            if not existing_product:
                # Create product
                product = stripe.Product.create(
                    name=plan_data['name'],
                    description=plan_data['description'],
                    metadata={'plan_id': plan_id}
                )
                logger.info(f"✅ Created Stripe product: {plan_data['name']}")
            else:
                product = existing_product
                logger.info(f"✅ Found existing Stripe product: {plan_data['name']}")
            
            # Check if price already exists
            prices = stripe.Price.list(product=product.id, limit=100)
            existing_price = None
            
            for price in prices.data:
                if (price.unit_amount == int(plan_data['price'] * 100) and 
                    price.currency == plan_data['currency'] and 
                    price.recurring.interval == plan_data['interval']):
                    existing_price = price
                    break
            
            if not existing_price:
                # Create price
                price = stripe.Price.create(
                    product=product.id,
                    unit_amount=int(plan_data['price'] * 100),
                    currency=plan_data['currency'],
                    recurring={'interval': plan_data['interval']},
                    metadata={'plan_id': plan_id}
                )
                logger.info(f"✅ Created Stripe price: {plan_data['name']} - ${plan_data['price']}")
            else:
                logger.info(f"✅ Found existing Stripe price: {plan_data['name']} - ${plan_data['price']}")
                
    except Exception as e:
        logger.error(f"❌ Failed to initialize Stripe products: {e}")

# Create FastAPI app
app = FastAPI(
    title="VeroctaAI Enterprise Payment Service",
    description="Stripe integration with multi-currency support and advanced billing features",
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

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "stripe_configured": STRIPE_SECRET_KEY is not None
    }

@app.get("/api/v2/payment/plans")
async def get_subscription_plans():
    """Get available subscription plans"""
    return {
        "plans": list(SUBSCRIPTION_PLANS.values()),
        "currencies_supported": ["usd", "eur", "gbp", "aud", "cad", "nzd"],
        "billing_intervals": ["month", "year"]
    }

@app.post("/api/v2/payment/customers")
async def create_customer(request: dict):
    """Create Stripe customer"""
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        customer = stripe.Customer.create(
            email=request.get('email'),
            name=request.get('name'),
            metadata={
                'company_id': request.get('company_id'),
                'user_id': request.get('user_id')
            }
        )
        
        return {
            "customer_id": customer.id,
            "email": customer.email,
            "created": customer.created
        }
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error creating customer: {e}")
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/v2/payment/subscriptions")
async def create_subscription(request: CreateSubscriptionRequest):
    """Create subscription"""
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        # Get plan data
        plan_data = SUBSCRIPTION_PLANS.get(request.plan_id)
        if not plan_data:
            raise HTTPException(status_code=400, detail="Invalid plan ID")
        
        # Get or create price
        prices = stripe.Price.list(
            limit=100,
            active=True
        )
        
        price_id = None
        for price in prices.data:
            if (price.unit_amount == int(plan_data['price'] * 100) and 
                price.currency == plan_data['currency'] and 
                price.recurring.interval == plan_data['interval']):
                price_id = price.id
                break
        
        if not price_id:
            raise HTTPException(status_code=500, detail="Price not found for plan")
        
        # Create subscription
        subscription_data = {
            'customer': request.customer_id,
            'items': [{'price': price_id}],
            'payment_behavior': 'default_incomplete',
            'payment_settings': {'save_default_payment_method': 'on_subscription'},
            'expand': ['latest_invoice.payment_intent']
        }
        
        if request.trial_period_days:
            subscription_data['trial_period_days'] = request.trial_period_days
        
        if request.coupon_code:
            subscription_data['coupon'] = request.coupon_code
        
        subscription = stripe.Subscription.create(**subscription_data)
        
        return {
            "subscription_id": subscription.id,
            "status": subscription.status,
            "current_period_start": subscription.current_period_start,
            "current_period_end": subscription.current_period_end,
            "client_secret": subscription.latest_invoice.payment_intent.client_secret if subscription.latest_invoice.payment_intent else None
        }
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error creating subscription: {e}")
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    except Exception as e:
        logger.error(f"Error creating subscription: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/v2/payment/subscriptions/{subscription_id}")
async def get_subscription(subscription_id: str):
    """Get subscription details"""
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)
        
        return {
            "subscription_id": subscription.id,
            "status": subscription.status,
            "current_period_start": subscription.current_period_start,
            "current_period_end": subscription.current_period_end,
            "cancel_at_period_end": subscription.cancel_at_period_end,
            "plan": {
                "id": subscription.items.data[0].price.id,
                "amount": subscription.items.data[0].price.unit_amount / 100,
                "currency": subscription.items.data[0].price.currency,
                "interval": subscription.items.data[0].price.recurring.interval
            }
        }
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error retrieving subscription: {e}")
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    except Exception as e:
        logger.error(f"Error retrieving subscription: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.put("/api/v2/payment/subscriptions/{subscription_id}")
async def update_subscription(subscription_id: str, request: UpdateSubscriptionRequest):
    """Update subscription"""
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)
        
        update_data = {}
        
        if request.plan_id:
            # Get new price ID
            plan_data = SUBSCRIPTION_PLANS.get(request.plan_id)
            if not plan_data:
                raise HTTPException(status_code=400, detail="Invalid plan ID")
            
            prices = stripe.Price.list(limit=100, active=True)
            new_price_id = None
            
            for price in prices.data:
                if (price.unit_amount == int(plan_data['price'] * 100) and 
                    price.currency == plan_data['currency'] and 
                    price.recurring.interval == plan_data['interval']):
                    new_price_id = price.id
                    break
            
            if new_price_id:
                update_data['items'] = [{
                    'id': subscription.items.data[0].id,
                    'price': new_price_id
                }]
        
        if request.quantity:
            update_data['quantity'] = request.quantity
        
        if update_data:
            update_data['proration_behavior'] = request.proration_behavior
            subscription = stripe.Subscription.modify(subscription_id, **update_data)
        
        return {
            "subscription_id": subscription.id,
            "status": subscription.status,
            "current_period_start": subscription.current_period_start,
            "current_period_end": subscription.current_period_end
        }
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error updating subscription: {e}")
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    except Exception as e:
        logger.error(f"Error updating subscription: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.delete("/api/v2/payment/subscriptions/{subscription_id}")
async def cancel_subscription(subscription_id: str, immediately: bool = False):
    """Cancel subscription"""
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        if immediately:
            subscription = stripe.Subscription.delete(subscription_id)
        else:
            subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )
        
        return {
            "subscription_id": subscription.id,
            "status": subscription.status,
            "canceled_at": subscription.canceled_at,
            "cancel_at_period_end": subscription.cancel_at_period_end
        }
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error canceling subscription: {e}")
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    except Exception as e:
        logger.error(f"Error canceling subscription: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/v2/payment/webhooks")
async def handle_webhook(request: Request):
    """Handle Stripe webhooks"""
    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")
    
    try:
        payload = await request.body()
        sig_header = request.headers.get('stripe-signature')
        
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
        
        # Handle different event types
        if event['type'] == 'customer.subscription.created':
            logger.info(f"Subscription created: {event['data']['object']['id']}")
        elif event['type'] == 'customer.subscription.updated':
            logger.info(f"Subscription updated: {event['data']['object']['id']}")
        elif event['type'] == 'customer.subscription.deleted':
            logger.info(f"Subscription canceled: {event['data']['object']['id']}")
        elif event['type'] == 'invoice.payment_succeeded':
            logger.info(f"Payment succeeded: {event['data']['object']['id']}")
        elif event['type'] == 'invoice.payment_failed':
            logger.info(f"Payment failed: {event['data']['object']['id']}")
        
        return {"status": "success"}
        
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Webhook signature verification failed: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        logger.error(f"Webhook processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/v2/payment/invoices/{customer_id}")
async def get_customer_invoices(customer_id: str, limit: int = 10):
    """Get customer invoices"""
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        invoices = stripe.Invoice.list(
            customer=customer_id,
            limit=limit
        )
        
        return {
            "invoices": [
                {
                    "id": invoice.id,
                    "amount_paid": invoice.amount_paid,
                    "currency": invoice.currency,
                    "status": invoice.status,
                    "created": invoice.created,
                    "due_date": invoice.due_date,
                    "download_url": invoice.invoice_pdf
                }
                for invoice in invoices.data
            ]
        }
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error retrieving invoices: {e}")
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    except Exception as e:
        logger.error(f"Error retrieving invoices: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
        reload=os.getenv("RELOAD", "false").lower() == "true",
        log_level="info"
    )
