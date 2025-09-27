"""
VeroctaAI Enterprise Analytics Service - Unit Tests
Comprehensive test suite for analytics functionality
"""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

from services.analytics.main import (
    calculate_advanced_spend_score,
    generate_ai_insights,
    TransactionData,
    SpendScoreRequest,
    SpendScoreResponse
)

class TestSpendScoreCalculation:
    """Test SpendScore calculation functionality"""
    
    def test_empty_transactions(self):
        """Test SpendScore with empty transaction list"""
        result = calculate_advanced_spend_score([])
        
        assert result['score'] == 0
        assert result['tier'] == 'No Data'
        assert 'No transaction data available' in result['insights']
    
    def test_insufficient_transactions(self):
        """Test SpendScore with insufficient transactions"""
        transactions = [
            TransactionData(date='2024-01-01', amount=100, vendor='Test', category='Test'),
            TransactionData(date='2024-01-02', amount=200, vendor='Test', category='Test')
        ]
        
        result = calculate_advanced_spend_score(transactions)
        
        assert result['score'] == 0
        assert result['tier'] == 'Insufficient Data'
        assert 'Insufficient data for analysis' in result['insights']
    
    def test_valid_transactions(self):
        """Test SpendScore with valid transactions"""
        transactions = [
            TransactionData(date='2024-01-01', amount=100, vendor='Vendor1', category='Category1'),
            TransactionData(date='2024-01-02', amount=200, vendor='Vendor2', category='Category2'),
            TransactionData(date='2024-01-03', amount=150, vendor='Vendor3', category='Category1'),
            TransactionData(date='2024-01-04', amount=300, vendor='Vendor1', category='Category3'),
            TransactionData(date='2024-01-05', amount=250, vendor='Vendor2', category='Category2')
        ]
        
        result = calculate_advanced_spend_score(transactions)
        
        assert 0 <= result['score'] <= 100
        assert result['tier'] in ['Excellent', 'Very Good', 'Good', 'Fair', 'Needs Improvement']
        assert isinstance(result['breakdown'], dict)
        assert isinstance(result['insights'], list)
        assert isinstance(result['recommendations'], list)
    
    def test_score_components(self):
        """Test individual score components"""
        transactions = [
            TransactionData(date='2024-01-01', amount=100, vendor='Vendor1', category='Category1'),
            TransactionData(date='2024-01-02', amount=100, vendor='Vendor2', category='Category2'),
            TransactionData(date='2024-01-03', amount=100, vendor='Vendor3', category='Category3'),
            TransactionData(date='2024-01-04', amount=100, vendor='Vendor4', category='Category4'),
            TransactionData(date='2024-01-05', amount=100, vendor='Vendor5', category='Category5')
        ]
        
        result = calculate_advanced_spend_score(transactions)
        
        # Check that all score components are present
        expected_components = ['efficiency', 'diversity', 'vendor_management', 'frequency', 'consistency']
        for component in expected_components:
            assert component in result['breakdown']
            assert 0 <= result['breakdown'][component] <= 100
    
    def test_high_score_scenario(self):
        """Test scenario that should produce high SpendScore"""
        # Create transactions with good patterns
        transactions = []
        base_date = datetime(2024, 1, 1)
        
        # Regular monthly transactions with good diversity
        for month in range(12):
            for day in range(1, 6):  # 5 transactions per month
                date = base_date + timedelta(days=month * 30 + day)
                transactions.append(TransactionData(
                    date=date.strftime('%Y-%m-%d'),
                    amount=100 + (day * 10),  # Consistent amounts
                    vendor=f'Vendor{day}',
                    category=f'Category{day}'
                ))
        
        result = calculate_advanced_spend_score(transactions)
        
        # Should have a good score due to consistency and diversity
        assert result['score'] > 60
        assert result['tier'] in ['Excellent', 'Very Good', 'Good']
    
    def test_low_score_scenario(self):
        """Test scenario that should produce low SpendScore"""
        # Create transactions with poor patterns
        transactions = []
        base_date = datetime(2024, 1, 1)
        
        # Irregular transactions with high variance
        amounts = [1000, 50, 2000, 25, 1500, 75, 3000, 10, 2500, 100]
        vendors = ['Vendor1'] * 10  # Same vendor
        categories = ['Category1'] * 10  # Same category
        
        for i, (amount, vendor, category) in enumerate(zip(amounts, vendors, categories)):
            date = base_date + timedelta(days=i * 7)  # Weekly but irregular
            transactions.append(TransactionData(
                date=date.strftime('%Y-%m-%d'),
                amount=amount,
                vendor=vendor,
                category=category
            ))
        
        result = calculate_advanced_spend_score(transactions)
        
        # Should have a lower score due to poor patterns
        assert result['score'] < 80
        assert result['tier'] in ['Fair', 'Needs Improvement']

class TestAIIntegration:
    """Test AI integration functionality"""
    
    @patch('services.analytics.main.openai_client')
    async def test_generate_ai_insights_success(self, mock_openai):
        """Test successful AI insights generation"""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "1. Optimize subscription management\n2. Implement automated categorization\n3. Review vendor contracts"
        mock_openai.chat.completions.create.return_value = mock_response
        
        transactions = [
            TransactionData(date='2024-01-01', amount=100, vendor='Vendor1', category='Category1'),
            TransactionData(date='2024-01-02', amount=200, vendor='Vendor2', category='Category2')
        ]
        
        insights = await generate_ai_insights(transactions, 75.0)
        
        assert len(insights) == 3
        assert "Optimize subscription management" in insights[0]
        assert "Implement automated categorization" in insights[1]
        assert "Review vendor contracts" in insights[2]
    
    @patch('services.analytics.main.openai_client', None)
    async def test_generate_ai_insights_no_openai(self):
        """Test AI insights when OpenAI is not configured"""
        transactions = [
            TransactionData(date='2024-01-01', amount=100, vendor='Vendor1', category='Category1')
        ]
        
        insights = await generate_ai_insights(transactions, 75.0)
        
        assert len(insights) == 1
        assert "AI insights not available" in insights[0]
    
    @patch('services.analytics.main.openai_client')
    async def test_generate_ai_insights_error(self, mock_openai):
        """Test AI insights generation with error"""
        mock_openai.chat.completions.create.side_effect = Exception("API Error")
        
        transactions = [
            TransactionData(date='2024-01-01', amount=100, vendor='Vendor1', category='Category1')
        ]
        
        insights = await generate_ai_insights(transactions, 75.0)
        
        assert len(insights) == 1
        assert "AI insights temporarily unavailable" in insights[0]

class TestDataValidation:
    """Test data validation and edge cases"""
    
    def test_invalid_date_format(self):
        """Test handling of invalid date formats"""
        transactions = [
            TransactionData(date='invalid-date', amount=100, vendor='Vendor1', category='Category1'),
            TransactionData(date='2024-01-01', amount=200, vendor='Vendor2', category='Category2'),
            TransactionData(date='2024-01-02', amount=300, vendor='Vendor3', category='Category3')
        ]
        
        result = calculate_advanced_spend_score(transactions)
        
        # Should still work with valid transactions
        assert result['score'] > 0
        assert result['tier'] != 'No Data'
    
    def test_negative_amounts(self):
        """Test handling of negative amounts (refunds)"""
        transactions = [
            TransactionData(date='2024-01-01', amount=100, vendor='Vendor1', category='Category1'),
            TransactionData(date='2024-01-02', amount=-50, vendor='Vendor1', category='Category1'),  # Refund
            TransactionData(date='2024-01-03', amount=200, vendor='Vendor2', category='Category2')
        ]
        
        result = calculate_advanced_spend_score(transactions)
        
        assert result['score'] > 0
        assert result['tier'] != 'No Data'
    
    def test_large_amounts(self):
        """Test handling of large transaction amounts"""
        transactions = [
            TransactionData(date='2024-01-01', amount=1000000, vendor='Vendor1', category='Category1'),
            TransactionData(date='2024-01-02', amount=2000000, vendor='Vendor2', category='Category2'),
            TransactionData(date='2024-01-03', amount=1500000, vendor='Vendor3', category='Category3')
        ]
        
        result = calculate_advanced_spend_score(transactions)
        
        assert result['score'] > 0
        assert result['tier'] != 'No Data'
        assert isinstance(result['breakdown'], dict)
    
    def test_unicode_characters(self):
        """Test handling of unicode characters in vendor/category names"""
        transactions = [
            TransactionData(date='2024-01-01', amount=100, vendor='Vendor™', category='Category®'),
            TransactionData(date='2024-01-02', amount=200, vendor='Vendor©', category='Category™'),
            TransactionData(date='2024-01-03', amount=300, vendor='Vendor®', category='Category©')
        ]
        
        result = calculate_advanced_spend_score(transactions)
        
        assert result['score'] > 0
        assert result['tier'] != 'No Data'

class TestPerformance:
    """Test performance characteristics"""
    
    def test_large_dataset(self):
        """Test performance with large dataset"""
        transactions = []
        base_date = datetime(2024, 1, 1)
        
        # Create 1000 transactions
        for i in range(1000):
            date = base_date + timedelta(days=i % 365)
            transactions.append(TransactionData(
                date=date.strftime('%Y-%m-%d'),
                amount=100 + (i % 100),
                vendor=f'Vendor{i % 50}',
                category=f'Category{i % 20}'
            ))
        
        import time
        start_time = time.time()
        result = calculate_advanced_spend_score(transactions)
        end_time = time.time()
        
        # Should complete within reasonable time (less than 5 seconds)
        assert end_time - start_time < 5.0
        assert result['score'] > 0
        assert result['tier'] != 'No Data'
    
    def test_memory_usage(self):
        """Test memory usage with large dataset"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        transactions = []
        base_date = datetime(2024, 1, 1)
        
        # Create 5000 transactions
        for i in range(5000):
            date = base_date + timedelta(days=i % 365)
            transactions.append(TransactionData(
                date=date.strftime('%Y-%m-%d'),
                amount=100 + (i % 100),
                vendor=f'Vendor{i % 100}',
                category=f'Category{i % 50}'
            ))
        
        result = calculate_advanced_spend_score(transactions)
        final_memory = process.memory_info().rss
        
        # Memory increase should be reasonable (less than 100MB)
        memory_increase = (final_memory - initial_memory) / 1024 / 1024
        assert memory_increase < 100
        
        assert result['score'] > 0
        assert result['tier'] != 'No Data'

# Pytest fixtures
@pytest.fixture
def sample_transactions():
    """Fixture providing sample transaction data"""
    return [
        TransactionData(date='2024-01-01', amount=100, vendor='Vendor1', category='Category1'),
        TransactionData(date='2024-01-02', amount=200, vendor='Vendor2', category='Category2'),
        TransactionData(date='2024-01-03', amount=150, vendor='Vendor3', category='Category1'),
        TransactionData(date='2024-01-04', amount=300, vendor='Vendor1', category='Category3'),
        TransactionData(date='2024-01-05', amount=250, vendor='Vendor2', category='Category2')
    ]

@pytest.fixture
def high_score_transactions():
    """Fixture providing transactions that should produce high score"""
    transactions = []
    base_date = datetime(2024, 1, 1)
    
    for month in range(6):  # 6 months of data
        for day in range(1, 6):  # 5 transactions per month
            date = base_date + timedelta(days=month * 30 + day)
            transactions.append(TransactionData(
                date=date.strftime('%Y-%m-%d'),
                amount=100 + (day * 10),  # Consistent amounts
                vendor=f'Vendor{day}',
                category=f'Category{day}'
            ))
    
    return transactions

# Integration tests
class TestIntegration:
    """Integration tests for analytics service"""
    
    @pytest.mark.asyncio
    async def test_full_analysis_pipeline(self, sample_transactions):
        """Test complete analysis pipeline"""
        # This would test the full FastAPI endpoint
        # For now, we'll test the core calculation function
        result = calculate_advanced_spend_score(sample_transactions)
        
        assert result['score'] > 0
        assert result['tier'] != 'No Data'
        assert len(result['insights']) > 0
        assert len(result['recommendations']) > 0
        assert 'breakdown' in result
        assert 'benchmarks' in result
