#!/usr/bin/env python3
"""
Database Connection Test Script for VeroctaAI
Tests all database connection methods and configurations
"""

import os
import sys
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_direct_connection():
    """Test direct connection to Supabase"""
    print("\n🔌 TESTING DIRECT CONNECTION")
    print("=" * 40)
    
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment")
        return False
    
    print(f"🔗 Connection String: {database_url.replace('VeroctaAI123', '***')}")
    
    try:
        # Create engine with Supabase-optimized settings
        engine = create_engine(
            database_url,
            poolclass=NullPool,
            pool_pre_ping=True,
            connect_args={
                "sslmode": "require",
                "connect_timeout": 10,
                "application_name": "VeroctaAI-Test"
            }
        )
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connection successful!")
            print(f"📊 PostgreSQL Version: {version}")
            
            # Test basic operations
            connection.execute(text("SELECT current_database()"))
            connection.execute(text("SELECT current_user"))
            print("✅ Basic operations successful!")
            
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def test_alternative_connections():
    """Test alternative connection methods"""
    print("\n🔄 TESTING ALTERNATIVE CONNECTIONS")
    print("=" * 40)
    
    # Transaction Pooler
    transaction_url = "postgresql+psycopg2://postgres.peddjxzwicclrqbnooiz:VeroctaAI123@aws-1-us-east-2.pooler.supabase.com:6543/postgres?sslmode=require"
    
    print("🔗 Testing Transaction Pooler...")
    try:
        engine = create_engine(transaction_url, poolclass=NullPool, pool_pre_ping=True)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Transaction Pooler: Working")
    except Exception as e:
        print(f"⚠️  Transaction Pooler: {str(e)}")
    
    # Session Pooler
    session_url = "postgresql+psycopg2://postgres.peddjxzwicclrqbnooiz:VeroctaAI123@aws-1-us-east-2.pooler.supabase.com:5432/postgres?sslmode=require"
    
    print("🔗 Testing Session Pooler...")
    try:
        engine = create_engine(session_url, poolclass=NullPool, pool_pre_ping=True)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Session Pooler: Working")
    except Exception as e:
        print(f"⚠️  Session Pooler: {str(e)}")

def test_database_modules():
    """Test database modules from the application"""
    print("\n🧪 TESTING DATABASE MODULES")
    print("=" * 40)
    
    try:
        # Test main database module
        from database import test_connection, connected, engine
        print(f"📦 Main database module - Connected: {connected}")
        
        if test_connection():
            print("✅ Main database test_connection(): Working")
        else:
            print("⚠️  Main database test_connection(): Failed")
            
    except Exception as e:
        print(f"❌ Main database module error: {str(e)}")
    
    try:
        # Test enhanced database module
        from database_enhanced import enhanced_db
        print(f"📦 Enhanced database module - Connected: {enhanced_db.connected}")
        
        if enhanced_db.connected:
            session = enhanced_db.get_session()
            if session:
                session.close()
                print("✅ Enhanced database session: Working")
            else:
                print("⚠️  Enhanced database session: Failed")
        else:
            print("⚠️  Enhanced database not connected")
            
    except Exception as e:
        print(f"❌ Enhanced database module error: {str(e)}")

def main():
    """Main test function"""
    print("🧪 VEROCTA AI DATABASE CONNECTION TEST")
    print("=" * 50)
    
    # Test direct connection
    direct_success = test_direct_connection()
    
    # Test alternative connections
    test_alternative_connections()
    
    # Test database modules
    test_database_modules()
    
    print("\n🎯 SUMMARY")
    print("=" * 20)
    
    if direct_success:
        print("✅ Database connection is working!")
        print("🚀 Your backend can connect to Supabase successfully")
        print("💡 Ready for production deployment")
    else:
        print("❌ Database connection issues detected")
        print("🔧 Check your credentials and network connection")
        print("📋 Ensure DATABASE_URL is correctly configured")
    
    return direct_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)