import os
import logging
from sqlalchemy import create_engine, text, Column, String, Integer, DateTime, Boolean, JSON, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.pool import NullPool
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

# Load environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
Session = None
connected = False

# Initialize database connection lazily
def initialize_database():
    """Initialize database connection - called lazily when needed"""
    global engine, Session, connected
    
    if DATABASE_URL and not connected:
        try:
            logging.info("Attempting database connection using DATABASE_URL")
            
            # Create the SQLAlchemy engine with optimized settings for Supabase
            engine = create_engine(
                DATABASE_URL,
                poolclass=NullPool,  # Recommended for Supabase pooling
                pool_pre_ping=True,
                connect_args={
                    "sslmode": "require",
                    "connect_timeout": 5,  # Reduced timeout
                    "application_name": "VeroctaAI-Backend"
                }
            )
            
            # Test the connection with timeout
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                logging.info("✅ Database connection established and tested successfully")
            
            # Create session maker
            Session = sessionmaker(bind=engine)
            connected = True
            return True
            
        except Exception as e:
            logging.warning(f"⚠️ Database connection failed: {str(e)} - using in-memory storage")
            engine = None  
            Session = None
            connected = False
            return False
    elif not DATABASE_URL:
        logging.warning("⚠️ DATABASE_URL not found - using in-memory storage only")
        return False
    
    return connected

def test_connection():
    """Test database connection - required for health checks"""
    global engine, connected
    
    if not DATABASE_URL:
        return False
        
    try:
        if engine is None:
            # Try to recreate engine
            engine = create_engine(
                DATABASE_URL,
                poolclass=NullPool,
                pool_pre_ping=True,
                connect_args={
                    "sslmode": "require",
                    "connect_timeout": 10,
                    "application_name": "VeroctaAI-Backend"
                }
            )
        
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            connected = True
            return True
            
    except Exception as e:
        logging.error(f"Database connection test failed: {str(e)}")
        connected = False
        return False

# Define database models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default='user')
    company = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Report(Base):
    __tablename__ = 'reports'
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    user_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String, nullable=False)
    company = Column(String)
    spend_score = Column(Integer)
    data = Column(JSON)
    insights = Column(JSON)
    analysis = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String, default='completed')

class Insight(Base):
    __tablename__ = 'insights'
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    report_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    ai_insights = Column(JSON)
    recommendations = Column(JSON)
    waste_percentage = Column(DECIMAL(5,2))
    duplicate_expenses = Column(Integer, default=0)
    spending_spikes = Column(Integer, default=0)
    savings_opportunities = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseService:
    """Database service for VeroctaAI using SQLAlchemy"""
    
    def __init__(self):
        self.connected = False
        self.engine = None
        self.Session = None
        self._initialize_attempted = False
    
    def _ensure_connected(self):
        """Ensure database is connected before operations"""
        if not self._initialize_attempted:
            self._initialize_attempted = True
            if initialize_database():
                self.connected = connected
                self.engine = engine 
                self.Session = Session
        return self.connected
        
    def create_tables_if_not_exist(self):
        """Create tables if they don't exist"""
        if not self._ensure_connected():
            logging.warning("Database not connected - skipping table creation")
            return
            
        try:
            # Create all tables
            Base.metadata.create_all(self.engine)
            logging.info("Database schema ready")
            
        except Exception as e:
            logging.error(f"Error creating tables: {str(e)}")
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email from database"""
        if not self._ensure_connected() or not self.Session:
            return None
            
        try:
            session = self.Session()
            user = session.query(User).filter(User.email == email).first()
            session.close()
            
            if user:
                return {
                    'id': str(user.id),
                    'email': user.email,
                    'password_hash': user.password_hash,
                    'role': user.role,
                    'company': user.company,
                    'created_at': user.created_at.isoformat() if user.created_at is not None else None,
                    'is_active': user.is_active
                }
            return None
        except Exception as e:
            logging.error(f"Error fetching user: {str(e)}")
            return None
    
    def create_user(self, email: str, password_hash: str, company: str = None, role: str = "user") -> Optional[Dict]:
        """Create new user in database"""
        if not self._ensure_connected() or not self.Session:
            return None
            
        try:
            session = self.Session()
            
            new_user = User(
                email=email,
                password_hash=password_hash,
                company=company or 'Default Company',
                role=role,
                is_active=True
            )
            
            session.add(new_user)
            session.commit()
            
            user_dict = {
                'id': str(new_user.id),
                'email': new_user.email,
                'password_hash': new_user.password_hash,
                'role': new_user.role,
                'company': new_user.company,
                'created_at': new_user.created_at.isoformat() if new_user.created_at is not None else None,
                'is_active': new_user.is_active
            }
            
            session.close()
            return user_dict
        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            return None
    
    def create_report(self, user_id: str, title: str, company: str, data: Dict, 
                     spend_score: Optional[int] = None, insights: Optional[Dict] = None, analysis: Optional[Dict] = None) -> Optional[Dict]:
        """Create new report in database"""
        if not self._ensure_connected() or not self.Session:
            return None
            
        try:
            session = self.Session()
            
            new_report = Report(
                user_id=user_id,
                title=title,
                company=company,
                spend_score=spend_score,
                data=data,
                insights=insights or {},
                analysis=analysis or {},
                status='completed'
            )
            
            session.add(new_report)
            session.commit()
            
            report_dict = {
                'id': str(new_report.id),
                'user_id': str(new_report.user_id),
                'title': new_report.title,
                'company': new_report.company,
                'spend_score': new_report.spend_score,
                'data': new_report.data,
                'insights': new_report.insights,
                'analysis': new_report.analysis,
                'created_at': new_report.created_at.isoformat() if new_report.created_at is not None else None,
                'status': new_report.status
            }
            
            session.close()
            return report_dict
        except Exception as e:
            logging.error(f"Error creating report: {str(e)}")
            return None
    
    def get_user_reports(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user reports from database"""
        if not self._ensure_connected():
            return []
            
        try:
            session = self.Session()
            reports = session.query(Report).filter(Report.user_id == user_id).order_by(Report.created_at.desc()).limit(limit).all()
            
            reports_list = []
            for report in reports:
                reports_list.append({
                    'id': str(report.id),
                    'user_id': str(report.user_id),
                    'title': report.title,
                    'company': report.company,
                    'spend_score': report.spend_score,
                    'data': report.data,
                    'insights': report.insights,
                    'analysis': report.analysis,
                    'created_at': report.created_at.isoformat() if report.created_at else None,
                    'status': report.status
                })
            
            session.close()
            return reports_list
        except Exception as e:
            logging.error(f"Error fetching reports: {str(e)}")
            return []
    
    def get_report_by_id(self, report_id: str, user_id: str = None) -> Optional[Dict]:
        """Get specific report by ID"""
        if not self._ensure_connected():
            return None
            
        try:
            session = self.Session()
            query = session.query(Report).filter(Report.id == report_id)
            if user_id:
                query = query.filter(Report.user_id == user_id)
            
            report = query.first()
            session.close()
            
            if report:
                return {
                    'id': str(report.id),
                    'user_id': str(report.user_id),
                    'title': report.title,
                    'company': report.company,
                    'spend_score': report.spend_score,
                    'data': report.data,
                    'insights': report.insights,
                    'analysis': report.analysis,
                    'created_at': report.created_at.isoformat() if report.created_at else None,
                    'status': report.status
                }
            return None
        except Exception as e:
            logging.error(f"Error fetching report: {str(e)}")
            return None
    
    def save_insights(self, report_id: str, user_id: str, ai_insights: Dict, 
                     recommendations: List[str], metrics: Dict) -> Optional[Dict]:
        """Save AI insights to database"""
        if not self._ensure_connected():
            return None
            
        try:
            session = self.Session()
            
            new_insight = Insight(
                report_id=report_id,
                user_id=user_id,
                ai_insights=ai_insights,
                recommendations=recommendations,
                waste_percentage=metrics.get('waste_percentage', 0),
                duplicate_expenses=metrics.get('duplicate_expenses', 0),
                spending_spikes=metrics.get('spending_spikes', 0),
                savings_opportunities=metrics.get('savings_opportunities', 0)
            )
            
            session.add(new_insight)
            session.commit()
            
            insight_dict = {
                'id': str(new_insight.id),
                'report_id': str(new_insight.report_id),
                'user_id': str(new_insight.user_id),
                'ai_insights': new_insight.ai_insights,
                'recommendations': new_insight.recommendations,
                'waste_percentage': float(new_insight.waste_percentage) if new_insight.waste_percentage else 0,
                'duplicate_expenses': new_insight.duplicate_expenses,
                'spending_spikes': new_insight.spending_spikes,
                'savings_opportunities': new_insight.savings_opportunities,
                'created_at': new_insight.created_at.isoformat() if new_insight.created_at else None
            }
            
            session.close()
            return insight_dict
        except Exception as e:
            logging.error(f"Error saving insights: {str(e)}")
            return None
    
    def get_next_user_id(self) -> int:
        """Get next available user ID"""
        if not self._ensure_connected():
            return 1
            
        try:
            session = self.Session()
            count = session.query(User).count()
            session.close()
            return count + 1
        except Exception as e:
            logging.error(f"Error getting next user ID: {str(e)}")
            return 1
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID from database"""
        if not self._ensure_connected():
            return None
            
        try:
            session = self.Session()
            user = session.query(User).filter(User.id == user_id).first()
            session.close()
            
            if user:
                return {
                    'id': str(user.id),
                    'email': user.email,
                    'password_hash': user.password_hash,
                    'role': user.role,
                    'company': user.company,
                    'created_at': user.created_at.isoformat() if user.created_at else None,
                    'is_active': user.is_active
                }
            return None
        except Exception as e:
            logging.error(f"Error fetching user by ID: {str(e)}")
            return None

    def delete_report(self, report_id: str, user_id: str) -> bool:
        """Delete a report by ID for a specific user"""
        if not self._ensure_connected():
            return False
            
        try:
            session = self.Session()
            report = session.query(Report).filter(Report.id == report_id, Report.user_id == user_id).first()
            
            if report:
                session.delete(report)
                session.commit()
                session.close()
                return True
            
            session.close()
            return False
            
        except Exception as e:
            logging.error(f"Error deleting report: {str(e)}")
            return False

    def get_dashboard_stats(self, user_id: str) -> Dict:
        """Get dashboard statistics for user"""
        if not self._ensure_connected():
            return {
                'total_reports': 0,
                'avg_spend_score': 0,
                'total_savings': 0,
                'avg_waste_percentage': 0
            }
            
        try:
            session = self.Session()
            
            # Get reports
            reports = session.query(Report).filter(Report.user_id == user_id).all()
            total_reports = len(reports)
            
            if total_reports == 0:
                session.close()
                return {
                    'total_reports': 0,
                    'avg_spend_score': 0,
                    'total_savings': 0,
                    'avg_waste_percentage': 0
                }
            
            # Calculate average spend score
            avg_spend_score = sum(r.spend_score or 0 for r in reports) / total_reports
            
            # Calculate total savings (estimate 15% of total amount)
            total_amount = sum(r.data.get('total_amount', 0) if r.data else 0 for r in reports)
            total_savings = total_amount * 0.15
            
            # Get insights for waste percentage
            insights = session.query(Insight).filter(Insight.user_id == user_id).all()
            avg_waste_percentage = sum(float(i.waste_percentage) if i.waste_percentage else 0 for i in insights) / max(len(insights), 1)
            
            session.close()
            
            return {
                'total_reports': total_reports,
                'avg_spend_score': int(avg_spend_score),
                'total_savings': int(total_savings),
                'avg_waste_percentage': round(avg_waste_percentage, 1)
            }
            
        except Exception as e:
            logging.error(f"Error fetching dashboard stats: {str(e)}")
            return {
                'total_reports': 0,
                'avg_spend_score': 0,
                'total_savings': 0,
                'avg_waste_percentage': 0
            }

# Global database service instance
db_service = DatabaseService()