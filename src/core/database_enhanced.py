import os
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, JSON, DECIMAL, ForeignKey, Text, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.pool import NullPool
import json

# Enhanced Database Models for Complete SaaS Platform
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    company = Column(String(255))
    role = Column(String(50), default='user')  # user, admin, super_admin
    subscription_tier = Column(String(50), default='free')  # free, starter, pro, enterprise
    subscription_status = Column(String(50), default='active')  # active, cancelled, past_due
    stripe_customer_id = Column(String(255))
    avatar_url = Column(String(500))
    timezone = Column(String(100), default='UTC')
    currency = Column(String(10), default='USD')
    phone = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255))
    reset_token = Column(String(255))
    reset_token_expires = Column(DateTime)
    
    # Relationships
    reports = relationship("Report", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    insights = relationship("Insight", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    stripe_subscription_id = Column(String(255), unique=True)
    stripe_price_id = Column(String(255))
    tier = Column(String(50), nullable=False)  # starter, pro, enterprise
    status = Column(String(50), default='active')  # active, canceled, past_due, unpaid
    currency = Column(String(10), default='USD')
    amount = Column(DECIMAL(10, 2))
    billing_cycle = Column(String(50))  # monthly, annual
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    cancel_at_period_end = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")

class Report(Base):
    __tablename__ = 'reports'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    company = Column(String(255))
    file_name = Column(String(255))
    file_size = Column(BigInteger)
    data_source = Column(String(100))  # csv, google_sheets, quickbooks, etc.
    spend_score = Column(Integer)
    total_amount = Column(DECIMAL(15, 2))
    currency = Column(String(10), default='USD')
    transaction_count = Column(Integer)
    date_range_start = Column(DateTime)
    date_range_end = Column(DateTime)
    categories_count = Column(Integer)
    data = Column(JSON)  # Raw financial data
    analysis = Column(JSON)  # Processed analysis
    insights = Column(JSON)  # AI-generated insights
    recommendations = Column(JSON)  # Action recommendations
    status = Column(String(50), default='processing')  # processing, completed, failed
    processing_time = Column(DECIMAL(5, 2))  # Time in seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="reports")
    detailed_insights = relationship("Insight", back_populates="report")

class Insight(Base):
    __tablename__ = 'insights'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey('reports.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    insight_type = Column(String(100))  # waste_detection, trend_analysis, forecasting, etc.
    title = Column(String(255))
    description = Column(Text)
    ai_insights = Column(JSON)
    recommendations = Column(JSON)
    waste_percentage = Column(DECIMAL(5, 2))
    potential_savings = Column(DECIMAL(15, 2))
    duplicate_expenses = Column(Integer, default=0)
    spending_spikes = Column(Integer, default=0)
    savings_opportunities = Column(Integer, default=0)
    confidence_score = Column(DECIMAL(3, 2))  # 0.00 to 1.00
    priority = Column(String(20), default='medium')  # low, medium, high, critical
    is_implemented = Column(Boolean, default=False)
    implementation_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    report = relationship("Report", back_populates="detailed_insights")
    user = relationship("User", back_populates="insights")

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon = Column(String(100))
    color = Column(String(20))
    parent_category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    is_system = Column(Boolean, default=True)  # System vs user-defined
    created_at = Column(DateTime, default=datetime.utcnow)

class Integration(Base):
    __tablename__ = 'integrations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    integration_type = Column(String(100), nullable=False)  # google_sheets, quickbooks, xero
    provider_id = Column(String(255))  # External system ID
    credentials = Column(JSON)  # Encrypted credentials
    configuration = Column(JSON)  # Integration settings
    sync_frequency = Column(String(50), default='daily')  # manual, daily, weekly, monthly
    last_sync = Column(DateTime)
    next_sync = Column(DateTime)
    status = Column(String(50), default='active')  # active, error, disabled
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    action = Column(String(100), nullable=False)  # login, logout, create_report, etc.
    resource_type = Column(String(100))  # user, report, subscription, etc.
    resource_id = Column(String(255))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")

class EmailTemplate(Base):
    __tablename__ = 'email_templates'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    subject = Column(String(255), nullable=False)
    html_content = Column(Text, nullable=False)
    text_content = Column(Text)
    variables = Column(JSON)  # Template variables schema
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EmailQueue(Base):
    __tablename__ = 'email_queue'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    to_email = Column(String(255), nullable=False)
    from_email = Column(String(255))
    subject = Column(String(255), nullable=False)
    html_content = Column(Text)
    text_content = Column(Text)
    template_name = Column(String(100))
    template_data = Column(JSON)
    priority = Column(Integer, default=5)  # 1-10, higher is more priority
    status = Column(String(50), default='pending')  # pending, sent, failed
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    error_message = Column(Text)
    scheduled_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class SystemSetting(Base):
    __tablename__ = 'system_settings'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String(100), nullable=False, unique=True)
    value = Column(Text)
    data_type = Column(String(50), default='string')  # string, integer, boolean, json
    description = Column(Text)
    is_sensitive = Column(Boolean, default=False)  # Don't expose in API
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EnhancedDatabaseService:
    """Enhanced Database Service for Complete SaaS Platform"""
    
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        self.engine = None
        self.Session = None
        self.connected = False
        self._init_connection()
    
    def _init_connection(self):
        """Initialize database connection"""
        if not self.database_url:
            logging.warning("⚠️ DATABASE_URL not found - using in-memory storage only")
            return
            
        try:
            logging.info("Attempting enhanced database connection")
            
            # Create engine with optimized settings for Supabase
            self.engine = create_engine(
                self.database_url,
                poolclass=NullPool,  # Recommended for Supabase pooling
                pool_pre_ping=True,
                connect_args={
                    "sslmode": "require",
                    "connect_timeout": 10,
                    "application_name": "VeroctaAI-Backend-Enhanced"
                },
                echo=False  # Set to True for SQL debugging
            )
            
            # Test connection
            with self.engine.connect() as connection:
                from sqlalchemy import text
                connection.execute(text("SELECT 1"))
                logging.info("✅ Enhanced database connection established")
            
            # Create session maker
            self.Session = sessionmaker(bind=self.engine)
            self.connected = True
            
            # Create tables
            self.create_all_tables()
            
        except Exception as e:
            logging.error(f"⚠️ Enhanced database connection failed: {str(e)}")
            self.connected = False
    
    def create_all_tables(self):
        """Create all tables if they don't exist"""
        if not self.connected:
            return
            
        try:
            Base.metadata.create_all(self.engine)
            logging.info("✅ Enhanced database schema ready")
            self._seed_initial_data()
        except Exception as e:
            logging.error(f"Error creating enhanced tables: {str(e)}")
    
    def _seed_initial_data(self):
        """Seed initial system data"""
        try:
            session = self.Session()
            
            # Seed default categories
            default_categories = [
                {"name": "Office Supplies", "icon": "📝", "color": "#3B82F6"},
                {"name": "Technology", "icon": "💻", "color": "#8B5CF6"},
                {"name": "Marketing", "icon": "📢", "color": "#EF4444"},
                {"name": "Travel", "icon": "✈️", "color": "#10B981"},
                {"name": "Software Subscriptions", "icon": "🔄", "color": "#F59E0B"},
                {"name": "Professional Services", "icon": "🤝", "color": "#6366F1"},
                {"name": "Utilities", "icon": "⚡", "color": "#84CC16"},
                {"name": "Insurance", "icon": "🛡️", "color": "#EC4899"}
            ]
            
            for cat_data in default_categories:
                existing = session.query(Category).filter_by(name=cat_data["name"]).first()
                if not existing:
                    category = Category(**cat_data)
                    session.add(category)
            
            # Seed email templates
            email_templates = [
                {
                    "name": "welcome_email",
                    "subject": "Welcome to VeroctaAI - Your Financial Intelligence Platform",
                    "html_content": "<h1>Welcome {{user_name}}!</h1><p>Get ready to optimize your spending with AI-powered insights.</p>",
                    "variables": {"user_name": "string", "company": "string"}
                },
                {
                    "name": "report_ready",
                    "subject": "Your Financial Report is Ready - {{report_title}}",
                    "html_content": "<h1>Report Complete</h1><p>Your SpendScore: {{spend_score}}/100</p>",
                    "variables": {"report_title": "string", "spend_score": "integer"}
                }
            ]
            
            for template_data in email_templates:
                existing = session.query(EmailTemplate).filter_by(name=template_data["name"]).first()
                if not existing:
                    template = EmailTemplate(**template_data)
                    session.add(template)
            
            session.commit()
            session.close()
            logging.info("✅ Initial data seeded successfully")
            
        except Exception as e:
            logging.error(f"Error seeding initial data: {str(e)}")
    
    def get_session(self):
        """Get database session"""
        if not self.connected or not self.Session:
            return None
        return self.Session()

# Initialize enhanced database service
enhanced_db = EnhancedDatabaseService()