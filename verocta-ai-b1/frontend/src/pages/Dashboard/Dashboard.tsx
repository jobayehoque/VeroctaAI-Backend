import React, { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import {
  ChartBarIcon,
  DocumentTextIcon,
  CogIcon,
  CreditCardIcon,
  CloudArrowUpIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
} from '@heroicons/react/24/outline'

// Components
import SpendScoreCard from '../../components/Dashboard/SpendScoreCard'
import QuickActions from '../../components/Dashboard/QuickActions'
import RecentActivity from '../../components/Dashboard/RecentActivity'
import AnalyticsChart from '../../components/Charts/AnalyticsChart'
import LoadingSpinner from '../../components/UI/LoadingSpinner'
import ErrorBoundary from '../../components/UI/ErrorBoundary'

// Services
import { dashboardApi } from '../../services/api'
import { useAuth } from '../../contexts/AuthContext'

// Types
interface DashboardStats {
  totalReports: number
  avgSpendScore: number
  totalSavings: number
  avgWastePercentage: number
  monthlyTrend: number
  recentActivity: Array<{
    id: string
    type: string
    description: string
    timestamp: string
    status: 'success' | 'warning' | 'error'
  }>
}

interface SpendScoreData {
  score: number
  tier: string
  breakdown: Record<string, number>
  insights: string[]
  recommendations: string[]
  benchmarks: Record<string, any>
  anomalies: Array<{
    date: string
    amount: number
    vendor: string
    reason: string
  }>
  predictions: Record<string, any>
}

const Dashboard: React.FC = () => {
  const { user } = useAuth()
  const [selectedTimeRange, setSelectedTimeRange] = useState<'7d' | '30d' | '90d' | '1y'>('30d')

  // Fetch dashboard stats
  const { data: stats, isLoading: statsLoading, error: statsError } = useQuery({
    queryKey: ['dashboard-stats', selectedTimeRange],
    queryFn: () => dashboardApi.getStats(selectedTimeRange),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })

  // Fetch spend score data
  const { data: spendScore, isLoading: spendScoreLoading, error: spendScoreError } = useQuery({
    queryKey: ['spend-score', selectedTimeRange],
    queryFn: () => dashboardApi.getSpendScore(selectedTimeRange),
    staleTime: 10 * 60 * 1000, // 10 minutes
  })

  // Fetch recent activity
  const { data: recentActivity, isLoading: activityLoading } = useQuery({
    queryKey: ['recent-activity'],
    queryFn: dashboardApi.getRecentActivity,
    staleTime: 2 * 60 * 1000, // 2 minutes
  })

  if (statsLoading || spendScoreLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (statsError || spendScoreError) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <ExclamationTriangleIcon className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Dashboard</h2>
          <p className="text-gray-600 mb-4">Unable to load dashboard data. Please try again.</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
                <p className="text-gray-600 mt-1">
                  Welcome back, {user?.email || 'User'}! Here's your financial overview.
                </p>
              </div>
              
              {/* Time Range Selector */}
              <div className="flex space-x-2">
                {(['7d', '30d', '90d', '1y'] as const).map((range) => (
                  <button
                    key={range}
                    onClick={() => setSelectedTimeRange(range)}
                    className={`px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                      selectedTimeRange === range
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {range === '7d' ? '7 Days' : 
                     range === '30d' ? '30 Days' :
                     range === '90d' ? '90 Days' : '1 Year'}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Stats Grid */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
          >
            {/* Total Reports */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Reports</p>
                  <p className="text-3xl font-bold text-gray-900">{stats?.totalReports || 0}</p>
                </div>
                <DocumentTextIcon className="h-8 w-8 text-blue-600" />
              </div>
              <div className="mt-4 flex items-center text-sm text-green-600">
                <ArrowTrendingUpIcon className="h-4 w-4 mr-1" />
                <span>+12% from last month</span>
              </div>
            </div>

            {/* Average Spend Score */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Avg Spend Score</p>
                  <p className="text-3xl font-bold text-gray-900">{stats?.avgSpendScore || 0}</p>
                </div>
                <ChartBarIcon className="h-8 w-8 text-green-600" />
              </div>
              <div className="mt-4 flex items-center text-sm text-green-600">
                <CheckCircleIcon className="h-4 w-4 mr-1" />
                <span>Excellent performance</span>
              </div>
            </div>

            {/* Total Savings */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Savings</p>
                  <p className="text-3xl font-bold text-gray-900">
                    ${stats?.totalSavings?.toLocaleString() || 0}
                  </p>
                </div>
                <CreditCardIcon className="h-8 w-8 text-purple-600" />
              </div>
              <div className="mt-4 flex items-center text-sm text-green-600">
                <ArrowTrendingUpIcon className="h-4 w-4 mr-1" />
                <span>+8% this month</span>
              </div>
            </div>

            {/* Waste Percentage */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Waste Reduction</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {stats?.avgWastePercentage || 0}%
                  </p>
                </div>
                <ExclamationTriangleIcon className="h-8 w-8 text-orange-600" />
              </div>
              <div className="mt-4 flex items-center text-sm text-red-600">
                <ArrowTrendingDownIcon className="h-4 w-4 mr-1" />
                <span>Needs improvement</span>
              </div>
            </div>
          </motion.div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Column - Spend Score & Analytics */}
            <div className="lg:col-span-2 space-y-8">
              {/* Spend Score Card */}
              {spendScore && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.1 }}
                >
                  <SpendScoreCard data={spendScore} />
                </motion.div>
              )}

              {/* Analytics Chart */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
              >
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Spending Trends</h3>
                <AnalyticsChart timeRange={selectedTimeRange} />
              </motion.div>
            </div>

            {/* Right Column - Quick Actions & Activity */}
            <div className="space-y-8">
              {/* Quick Actions */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.3 }}
              >
                <QuickActions />
              </motion.div>

              {/* Recent Activity */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.4 }}
              >
                <RecentActivity 
                  data={recentActivity || []} 
                  isLoading={activityLoading}
                />
              </motion.div>
            </div>
          </div>
        </div>
      </div>
    </ErrorBoundary>
  )
}

export default Dashboard
