"""
VeroctaAI Proprietary SpendScore™ Algorithm
Advanced 0-100 Rating System with RAG Visualization and AI-Powered Insights
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from decimal import Decimal
import json
import re
from dataclasses import dataclass
from enum import Enum

class SpendScoreLevel(Enum):
    """SpendScore RAG Classification"""
    EXCELLENT = "excellent"    # 90-100: Green
    GOOD = "good"             # 75-89: Light Green  
    AVERAGE = "average"       # 60-74: Amber
    POOR = "poor"             # 40-59: Orange
    CRITICAL = "critical"     # 0-39: Red

@dataclass
class SpendMetrics:
    """Core spending metrics for analysis"""
    total_amount: Decimal
    transaction_count: int
    unique_categories: int
    date_range_days: int
    duplicate_transactions: int
    high_variance_categories: int
    wasteful_spending: Decimal
    optimization_opportunities: int

@dataclass
class SpendScoreResult:
    """Complete SpendScore analysis result"""
    score: int
    level: SpendScoreLevel
    color: str
    label: str
    confidence: float
    metrics: SpendMetrics
    insights: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    waste_analysis: Dict[str, Any]
    benchmarks: Dict[str, Any]
    predictive_insights: Dict[str, Any]

class SpendScoreEngine:
    """Advanced SpendScore™ Calculation Engine"""
    
    def __init__(self):
        self.industry_benchmarks = self._load_industry_benchmarks()
        self.category_weights = self._define_category_weights()
        self.waste_patterns = self._define_waste_patterns()
        
    def _load_industry_benchmarks(self) -> Dict[str, Dict]:
        """Load industry spending benchmarks"""
        return {
            "technology": {
                "software_subscriptions": {"min": 0.15, "max": 0.35, "optimal": 0.25},
                "hardware": {"min": 0.10, "max": 0.20, "optimal": 0.15},
                "cloud_services": {"min": 0.20, "max": 0.40, "optimal": 0.30}
            },
            "professional_services": {
                "office_supplies": {"min": 0.02, "max": 0.08, "optimal": 0.05},
                "travel": {"min": 0.05, "max": 0.15, "optimal": 0.10},
                "marketing": {"min": 0.10, "max": 0.25, "optimal": 0.18}
            },
            "general": {
                "utilities": {"min": 0.05, "max": 0.12, "optimal": 0.08},
                "insurance": {"min": 0.03, "max": 0.10, "optimal": 0.06},
                "professional_services": {"min": 0.08, "max": 0.20, "optimal": 0.14}
            }
        }
    
    def _define_category_weights(self) -> Dict[str, float]:
        """Define weights for different spending categories"""
        return {
            "software_subscriptions": 1.0,  # High impact on efficiency
            "technology": 0.9,
            "marketing": 0.8,
            "professional_services": 0.7,
            "travel": 0.6,
            "office_supplies": 0.4,
            "utilities": 0.3,
            "other": 0.5
        }
    
    def _define_waste_patterns(self) -> List[Dict]:
        """Define patterns that indicate wasteful spending"""
        return [
            {
                "name": "duplicate_subscriptions",
                "pattern": r"(subscription|monthly|annual)",
                "threshold": 2,
                "weight": 0.3
            },
            {
                "name": "unused_software",
                "pattern": r"(software|saas|app)",
                "frequency_threshold": 0.1,  # Used less than 10% of time
                "weight": 0.25
            },
            {
                "name": "excessive_travel",
                "pattern": r"(travel|flight|hotel|uber|taxi)",
                "budget_percentage": 0.20,  # More than 20% of budget
                "weight": 0.2
            },
            {
                "name": "office_supply_waste",
                "pattern": r"(office|supplies|stationery)",
                "per_employee_threshold": 50,  # $50 per employee per month
                "weight": 0.15
            }
        ]
    
    def calculate_spend_score(self, financial_data: List[Dict], 
                            company_size: str = "small", 
                            industry: str = "general") -> SpendScoreResult:
        """
        Calculate comprehensive SpendScore™ with advanced analytics
        
        Args:
            financial_data: List of transaction dictionaries
            company_size: small, medium, large, enterprise
            industry: technology, professional_services, general, etc.
            
        Returns:
            SpendScoreResult with complete analysis
        """
        try:
            # Convert to DataFrame for analysis
            df = pd.DataFrame(financial_data)
            
            # Calculate core metrics
            metrics = self._calculate_core_metrics(df)
            
            # Perform waste analysis
            waste_analysis = self._analyze_waste_patterns(df)
            
            # Calculate efficiency scores
            efficiency_scores = self._calculate_efficiency_scores(df, metrics)
            
            # Generate benchmarks
            benchmarks = self._generate_benchmarks(df, industry, company_size)
            
            # Calculate final SpendScore
            score = self._calculate_final_score(efficiency_scores, waste_analysis, benchmarks)
            
            # Determine level and visualization
            level, color, label = self._determine_score_level(score)
            
            # Generate insights and recommendations
            insights = self._generate_insights(df, metrics, waste_analysis, benchmarks)
            recommendations = self._generate_recommendations(insights, waste_analysis)
            
            # Predictive analysis
            predictive_insights = self._generate_predictive_insights(df, metrics)
            
            # Calculate confidence score
            confidence = self._calculate_confidence(metrics, len(financial_data))
            
            return SpendScoreResult(
                score=score,
                level=level,
                color=color,
                label=label,
                confidence=confidence,
                metrics=metrics,
                insights=insights,
                recommendations=recommendations,
                waste_analysis=waste_analysis,
                benchmarks=benchmarks,
                predictive_insights=predictive_insights
            )
            
        except Exception as e:
            logging.error(f"Error calculating SpendScore: {str(e)}")
            return self._generate_fallback_score(financial_data)
    
    def _calculate_core_metrics(self, df: pd.DataFrame) -> SpendMetrics:
        """Calculate core spending metrics"""
        # Ensure amount column exists and is numeric
        if 'amount' not in df.columns:
            df['amount'] = df.get('Amount', df.get('total', 0))
        
        df['amount'] = pd.to_numeric(df['amount'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce').fillna(0)
        
        # Calculate date range
        date_cols = ['date', 'Date', 'transaction_date', 'created_at']
        date_col = None
        for col in date_cols:
            if col in df.columns:
                date_col = col
                break
        
        date_range_days = 30  # Default
        if date_col:
            try:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                date_range = df[date_col].max() - df[date_col].min()
                date_range_days = max(date_range.days, 1)
            except:
                pass
        
        # Detect duplicates
        duplicate_count = self._detect_duplicate_transactions(df)
        
        # Detect high variance categories
        high_variance_categories = self._detect_high_variance_categories(df)
        
        # Calculate wasteful spending
        wasteful_spending = self._calculate_wasteful_spending(df)
        
        # Count optimization opportunities
        optimization_opportunities = self._count_optimization_opportunities(df)
        
        return SpendMetrics(
            total_amount=Decimal(str(df['amount'].sum())),
            transaction_count=len(df),
            unique_categories=df.get('category', df.get('Category', pd.Series(['Other']))).nunique(),
            date_range_days=date_range_days,
            duplicate_transactions=duplicate_count,
            high_variance_categories=high_variance_categories,
            wasteful_spending=Decimal(str(wasteful_spending)),
            optimization_opportunities=optimization_opportunities
        )
    
    def _detect_duplicate_transactions(self, df: pd.DataFrame) -> int:
        """Detect potential duplicate transactions"""
        if len(df) < 2:
            return 0
            
        # Group by amount and description to find potential duplicates
        duplicate_groups = df.groupby(['amount', df.get('description', df.get('Description', 'unknown'))])
        duplicates = sum(1 for name, group in duplicate_groups if len(group) > 1)
        
        return duplicates
    
    def _detect_high_variance_categories(self, df: pd.DataFrame) -> int:
        """Detect categories with high spending variance"""
        category_col = df.get('category', df.get('Category', pd.Series(['Other'] * len(df))))
        
        if category_col.nunique() < 2:
            return 0
            
        category_stats = df.groupby(category_col)['amount'].agg(['mean', 'std'])
        high_variance = (category_stats['std'] / category_stats['mean'] > 1.0).sum()
        
        return int(high_variance)
    
    def _calculate_wasteful_spending(self, df: pd.DataFrame) -> float:
        """Calculate estimated wasteful spending"""
        wasteful_amount = 0
        
        # Check for waste patterns
        description_col = df.get('description', df.get('Description', pd.Series([''] * len(df))))
        
        for pattern in self.waste_patterns:
            pattern_matches = description_col.str.contains(pattern['pattern'], case=False, na=False)
            if pattern_matches.any():
                pattern_amount = df[pattern_matches]['amount'].sum()
                wasteful_amount += pattern_amount * pattern['weight']
        
        return float(wasteful_amount)
    
    def _count_optimization_opportunities(self, df: pd.DataFrame) -> int:
        """Count potential optimization opportunities"""
        opportunities = 0
        
        # High-frequency low-amount transactions (could be consolidated)
        small_transactions = df[df['amount'] < 50]
        if len(small_transactions) > 10:
            opportunities += 1
        
        # Unused subscriptions (same amount, regular intervals)
        monthly_amounts = df['amount'].round(2).value_counts()
        regular_payments = monthly_amounts[monthly_amounts >= 3]  # 3+ identical payments
        opportunities += len(regular_payments)
        
        # Categories with excessive spending
        category_col = df.get('category', df.get('Category', pd.Series(['Other'] * len(df))))
        category_totals = df.groupby(category_col)['amount'].sum()
        total_spending = df['amount'].sum()
        
        for category, amount in category_totals.items():
            if amount / total_spending > 0.4:  # More than 40% of total spending
                opportunities += 1
        
        return opportunities
    
    def _analyze_waste_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive waste pattern analysis"""
        waste_analysis = {
            "total_waste_detected": 0,
            "waste_percentage": 0,
            "waste_categories": [],
            "duplicate_transactions": [],
            "excessive_spending": [],
            "unused_subscriptions": []
        }
        
        total_spending = df['amount'].sum()
        total_waste = 0
        
        # Analyze each waste pattern
        description_col = df.get('description', df.get('Description', pd.Series([''] * len(df))))
        
        for pattern in self.waste_patterns:
            pattern_matches = description_col.str.contains(pattern['pattern'], case=False, na=False)
            if pattern_matches.any():
                pattern_df = df[pattern_matches]
                pattern_waste = pattern_df['amount'].sum() * pattern['weight']
                total_waste += pattern_waste
                
                waste_analysis["waste_categories"].append({
                    "name": pattern["name"],
                    "amount": float(pattern_waste),
                    "transactions": len(pattern_df),
                    "severity": "high" if pattern_waste > total_spending * 0.1 else "medium"
                })
        
        waste_analysis["total_waste_detected"] = float(total_waste)
        waste_analysis["waste_percentage"] = float((total_waste / total_spending * 100) if total_spending > 0 else 0)
        
        return waste_analysis
    
    def _calculate_efficiency_scores(self, df: pd.DataFrame, metrics: SpendMetrics) -> Dict[str, float]:
        """Calculate various efficiency scores"""
        scores = {}
        
        # Transaction efficiency (fewer, larger transactions are more efficient)
        avg_transaction = float(metrics.total_amount) / max(metrics.transaction_count, 1)
        scores['transaction_efficiency'] = min(avg_transaction / 100, 1.0) * 100  # Cap at 100
        
        # Category diversity (moderate diversity is optimal)
        category_diversity = min(metrics.unique_categories / 15, 1.0)  # Optimal around 15 categories
        scores['category_diversity'] = category_diversity * 100
        
        # Duplicate efficiency (fewer duplicates is better)
        duplicate_ratio = metrics.duplicate_transactions / max(metrics.transaction_count, 1)
        scores['duplicate_efficiency'] = max(0, (1 - duplicate_ratio)) * 100
        
        # Variance efficiency (consistent spending is better)
        variance_ratio = metrics.high_variance_categories / max(metrics.unique_categories, 1)
        scores['variance_efficiency'] = max(0, (1 - variance_ratio)) * 100
        
        return scores
    
    def _generate_benchmarks(self, df: pd.DataFrame, industry: str, company_size: str) -> Dict[str, Any]:
        """Generate industry and size-based benchmarks"""
        benchmarks = {
            "industry_comparison": {},
            "size_comparison": {},
            "optimal_ranges": {}
        }
        
        # Get industry benchmarks
        industry_data = self.industry_benchmarks.get(industry, self.industry_benchmarks["general"])
        
        # Calculate category percentages
        category_col = df.get('category', df.get('Category', pd.Series(['other'] * len(df))))
        total_spending = df['amount'].sum()
        
        category_percentages = {}
        for category in category_col.unique():
            category_amount = df[df[category_col.name] == category]['amount'].sum()
            category_percentages[category.lower()] = float(category_amount / total_spending) if total_spending > 0 else 0
        
        # Compare against benchmarks
        for category, percentage in category_percentages.items():
            if category in industry_data:
                benchmark = industry_data[category]
                benchmarks["industry_comparison"][category] = {
                    "actual": percentage,
                    "optimal": benchmark["optimal"],
                    "variance": abs(percentage - benchmark["optimal"]),
                    "status": self._get_benchmark_status(percentage, benchmark)
                }
        
        return benchmarks
    
    def _get_benchmark_status(self, actual: float, benchmark: Dict) -> str:
        """Determine benchmark status"""
        if benchmark["min"] <= actual <= benchmark["max"]:
            return "optimal" if abs(actual - benchmark["optimal"]) < 0.05 else "good"
        elif actual < benchmark["min"]:
            return "under"
        else:
            return "over"
    
    def _calculate_final_score(self, efficiency_scores: Dict, waste_analysis: Dict, benchmarks: Dict) -> int:
        """Calculate final SpendScore using weighted components"""
        
        # Base efficiency score (40% weight)
        base_score = np.mean(list(efficiency_scores.values())) * 0.4
        
        # Waste penalty (30% weight)
        waste_penalty = (100 - waste_analysis["waste_percentage"]) * 0.3
        
        # Benchmark score (20% weight) 
        benchmark_scores = []
        for category_data in benchmarks.get("industry_comparison", {}).values():
            if category_data["status"] == "optimal":
                benchmark_scores.append(100)
            elif category_data["status"] == "good":
                benchmark_scores.append(80)
            elif category_data["status"] in ["under", "over"]:
                benchmark_scores.append(60)
        
        benchmark_score = (np.mean(benchmark_scores) if benchmark_scores else 70) * 0.2
        
        # Opportunity bonus (10% weight)
        # Lower opportunity count means better current state
        opportunity_bonus = max(0, 100 - waste_analysis.get("total_waste_detected", 0)) * 0.1
        
        final_score = base_score + waste_penalty + benchmark_score + opportunity_bonus
        
        return int(np.clip(final_score, 0, 100))
    
    def _determine_score_level(self, score: int) -> Tuple[SpendScoreLevel, str, str]:
        """Determine SpendScore level and visualization"""
        if score >= 90:
            return SpendScoreLevel.EXCELLENT, "#10B981", "Excellent"  # Green
        elif score >= 75:
            return SpendScoreLevel.GOOD, "#34D399", "Good"  # Light Green
        elif score >= 60:
            return SpendScoreLevel.AVERAGE, "#F59E0B", "Average"  # Amber
        elif score >= 40:
            return SpendScoreLevel.POOR, "#F97316", "Poor"  # Orange
        else:
            return SpendScoreLevel.CRITICAL, "#EF4444", "Critical"  # Red
    
    def _generate_insights(self, df: pd.DataFrame, metrics: SpendMetrics, 
                          waste_analysis: Dict, benchmarks: Dict) -> Dict[str, Any]:
        """Generate comprehensive AI-powered insights"""
        insights = {
            "spending_summary": {
                "total_analyzed": float(metrics.total_amount),
                "transaction_count": metrics.transaction_count,
                "average_transaction": float(metrics.total_amount) / max(metrics.transaction_count, 1),
                "categories_analyzed": metrics.unique_categories
            },
            "key_findings": [],
            "efficiency_metrics": {
                "waste_percentage": waste_analysis["waste_percentage"],
                "duplicate_transactions": metrics.duplicate_transactions,
                "optimization_opportunities": metrics.optimization_opportunities
            },
            "category_insights": {},
            "trends": {},
            "risk_factors": []
        }
        
        # Generate key findings
        if waste_analysis["waste_percentage"] > 20:
            insights["key_findings"].append({
                "type": "waste_alert",
                "message": f"High waste detected: {waste_analysis['waste_percentage']:.1f}% of spending shows inefficiencies",
                "priority": "high"
            })
        
        if metrics.duplicate_transactions > 5:
            insights["key_findings"].append({
                "type": "duplicate_alert", 
                "message": f"{metrics.duplicate_transactions} potential duplicate transactions found",
                "priority": "medium"
            })
        
        # Category insights
        category_col = df.get('category', df.get('Category', pd.Series(['other'] * len(df))))
        category_analysis = df.groupby(category_col)['amount'].agg(['sum', 'count', 'mean'])
        
        for category, stats in category_analysis.iterrows():
            insights["category_insights"][category] = {
                "total_spent": float(stats['sum']),
                "transaction_count": int(stats['count']),
                "average_amount": float(stats['mean']),
                "percentage_of_total": float(stats['sum'] / df['amount'].sum() * 100)
            }
        
        return insights
    
    def _generate_recommendations(self, insights: Dict, waste_analysis: Dict) -> List[Dict[str, Any]]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Waste reduction recommendations
        if waste_analysis["waste_percentage"] > 15:
            recommendations.append({
                "type": "waste_reduction",
                "priority": "high",
                "title": "Reduce Wasteful Spending",
                "description": f"You can save up to {waste_analysis['waste_percentage']:.1f}% by eliminating wasteful expenses",
                "potential_savings": waste_analysis["total_waste_detected"],
                "action_items": [
                    "Review and cancel unused subscriptions",
                    "Consolidate duplicate services",
                    "Implement approval workflows for large expenses"
                ]
            })
        
        # Duplicate transaction recommendations
        duplicate_count = insights["efficiency_metrics"]["duplicate_transactions"]
        if duplicate_count > 3:
            recommendations.append({
                "type": "duplicate_cleanup",
                "priority": "medium", 
                "title": "Eliminate Duplicate Transactions",
                "description": f"Found {duplicate_count} potential duplicate transactions",
                "action_items": [
                    "Review similar amounts and descriptions",
                    "Implement expense tracking controls",
                    "Set up automated duplicate detection"
                ]
            })
        
        # Category optimization
        for category, data in insights["category_insights"].items():
            if data["percentage_of_total"] > 40:
                recommendations.append({
                    "type": "category_optimization",
                    "priority": "medium",
                    "title": f"Optimize {category.title()} Spending",
                    "description": f"{category.title()} represents {data['percentage_of_total']:.1f}% of total spending",
                    "action_items": [
                        f"Negotiate better rates for {category} services",
                        "Consider alternative providers",
                        "Implement budget caps for this category"
                    ]
                })
        
        return recommendations
    
    def _generate_predictive_insights(self, df: pd.DataFrame, metrics: SpendMetrics) -> Dict[str, Any]:
        """Generate predictive insights and forecasting"""
        predictive = {
            "monthly_forecast": {},
            "seasonal_trends": {},
            "risk_predictions": [],
            "growth_projections": {}
        }
        
        # Simple trend analysis
        if 'date' in df.columns or 'Date' in df.columns:
            try:
                date_col = 'date' if 'date' in df.columns else 'Date'
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                
                # Monthly aggregation
                monthly_spending = df.groupby(df[date_col].dt.to_period('M'))['amount'].sum()
                
                if len(monthly_spending) >= 2:
                    trend = np.polyfit(range(len(monthly_spending)), monthly_spending.values, 1)[0]
                    
                    predictive["monthly_forecast"] = {
                        "trend": "increasing" if trend > 0 else "decreasing",
                        "monthly_change": float(trend),
                        "next_month_prediction": float(monthly_spending.iloc[-1] + trend)
                    }
                    
                    # Risk predictions
                    if trend > monthly_spending.mean() * 0.1:  # Growing by more than 10% of average
                        predictive["risk_predictions"].append({
                            "type": "spending_increase",
                            "message": "Spending is trending upward significantly",
                            "recommendation": "Review budget and implement cost controls"
                        })
                        
            except Exception as e:
                logging.warning(f"Could not generate predictive insights: {str(e)}")
        
        return predictive
    
    def _calculate_confidence(self, metrics: SpendMetrics, data_points: int) -> float:
        """Calculate confidence score for the analysis"""
        confidence_factors = []
        
        # Data volume confidence
        if data_points >= 100:
            confidence_factors.append(1.0)
        elif data_points >= 50:
            confidence_factors.append(0.8)
        elif data_points >= 20:
            confidence_factors.append(0.6)
        else:
            confidence_factors.append(0.4)
        
        # Date range confidence
        if metrics.date_range_days >= 90:
            confidence_factors.append(1.0)
        elif metrics.date_range_days >= 30:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.6)
        
        # Category diversity confidence
        if metrics.unique_categories >= 10:
            confidence_factors.append(1.0)
        elif metrics.unique_categories >= 5:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.6)
        
        return float(np.mean(confidence_factors))
    
    def _generate_fallback_score(self, financial_data: List[Dict]) -> SpendScoreResult:
        """Generate fallback score when calculation fails"""
        return SpendScoreResult(
            score=50,
            level=SpendScoreLevel.AVERAGE,
            color="#F59E0B",
            label="Average",
            confidence=0.3,
            metrics=SpendMetrics(
                total_amount=Decimal("0"),
                transaction_count=len(financial_data),
                unique_categories=1,
                date_range_days=30,
                duplicate_transactions=0,
                high_variance_categories=0,
                wasteful_spending=Decimal("0"),
                optimization_opportunities=0
            ),
            insights={"error": "Could not analyze data properly"},
            recommendations=[],
            waste_analysis={"total_waste_detected": 0, "waste_percentage": 0},
            benchmarks={},
            predictive_insights={}
        )

# Export the engine
spend_score_engine = SpendScoreEngine()

def calculate_advanced_spend_score(financial_data: List[Dict], 
                                 company_size: str = "small",
                                 industry: str = "general") -> Dict[str, Any]:
    """
    Public API function for calculating SpendScore
    
    Args:
        financial_data: List of transaction dictionaries
        company_size: Company size classification
        industry: Industry classification
        
    Returns:
        Dict containing complete SpendScore analysis
    """
    result = spend_score_engine.calculate_spend_score(financial_data, company_size, industry)
    
    return {
        "spend_score": result.score,
        "level": result.level.value,
        "color": result.color,
        "label": result.label,
        "confidence": result.confidence,
        "total_amount": float(result.metrics.total_amount),
        "transaction_count": result.metrics.transaction_count,
        "waste_percentage": result.waste_analysis["waste_percentage"],
        "insights": result.insights,
        "recommendations": result.recommendations,
        "benchmarks": result.benchmarks,
        "predictive_insights": result.predictive_insights,
        "detailed_metrics": {
            "unique_categories": result.metrics.unique_categories,
            "duplicate_transactions": result.metrics.duplicate_transactions,
            "optimization_opportunities": result.metrics.optimization_opportunities,
            "wasteful_spending": float(result.metrics.wasteful_spending)
        }
    }


def get_enhanced_analysis(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Get complete enhanced analysis - compatibility function"""
    result = calculate_advanced_spend_score(transactions)
    return result


def get_score_label(score: float) -> str:
    """Get score label for compatibility"""
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 60:
        return "Average"
    elif score >= 40:
        return "Poor"
    else:
        return "Critical"


def get_score_color(score: float) -> str:
    """Get score color for compatibility"""
    if score >= 90:
        return "#10B981"  # Green
    elif score >= 75:
        return "#34D399"  # Light Green
    elif score >= 60:
        return "#F59E0B"  # Amber
    elif score >= 40:
        return "#F97316"  # Orange
    else:
        return "#EF4444"  # Red