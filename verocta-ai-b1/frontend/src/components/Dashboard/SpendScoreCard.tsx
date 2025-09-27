import React, { useState } from 'react'
import { motion } from 'framer-motion'
import {
  ChartBarIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  InformationCircleIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
} from '@heroicons/react/24/outline'

// Types
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

interface SpendScoreCardProps {
  data: SpendScoreData
}

const SpendScoreCard: React.FC<SpendScoreCardProps> = ({ data }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'insights' | 'recommendations'>('overview')

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600'
    if (score >= 80) return 'text-blue-600'
    if (score >= 70) return 'text-yellow-600'
    if (score >= 60) return 'text-orange-600'
    return 'text-red-600'
  }

  const getScoreBgColor = (score: number) => {
    if (score >= 90) return 'bg-green-100'
    if (score >= 80) return 'bg-blue-100'
    if (score >= 70) return 'bg-yellow-100'
    if (score >= 60) return 'bg-orange-100'
    return 'bg-red-100'
  }

  const getTierIcon = (tier: string) => {
    if (tier.toLowerCase().includes('excellent')) return <CheckCircleIcon className="h-6 w-6 text-green-600" />
    if (tier.toLowerCase().includes('good')) return <ChartBarIcon className="h-6 w-6 text-blue-600" />
    if (tier.toLowerCase().includes('fair')) return <InformationCircleIcon className="h-6 w-6 text-yellow-600" />
    return <ExclamationTriangleIcon className="h-6 w-6 text-red-600" />
  }

  const getTierColor = (tier: string) => {
    if (tier.toLowerCase().includes('excellent')) return 'text-green-600'
    if (tier.toLowerCase().includes('good')) return 'text-blue-600'
    if (tier.toLowerCase().includes('fair')) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-white">SpendScore™ Analysis</h3>
            <p className="text-blue-100 text-sm">AI-powered financial efficiency score</p>
          </div>
          <div className="text-right">
            <div className={`text-4xl font-bold ${getScoreColor(data.score)}`}>
              {data.score}
            </div>
            <div className="text-white text-sm">out of 100</div>
          </div>
        </div>
      </div>

      {/* Score Display */}
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            {getTierIcon(data.tier)}
            <div>
              <h4 className={`text-lg font-semibold ${getTierColor(data.tier)}`}>
                {data.tier}
              </h4>
              <p className="text-gray-600 text-sm">
                {data.score >= 90 ? 'Outstanding financial management' :
                 data.score >= 80 ? 'Very good spending patterns' :
                 data.score >= 70 ? 'Good financial practices' :
                 data.score >= 60 ? 'Room for improvement' :
                 'Needs significant optimization'}
              </p>
            </div>
          </div>
          
          {/* Progress Ring */}
          <div className="relative w-20 h-20">
            <svg className="w-20 h-20 transform -rotate-90" viewBox="0 0 36 36">
              <path
                className="text-gray-200"
                stroke="currentColor"
                strokeWidth="3"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <path
                className={getScoreColor(data.score)}
                stroke="currentColor"
                strokeWidth="3"
                fill="none"
                strokeDasharray={`${data.score}, 100`}
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className={`text-lg font-bold ${getScoreColor(data.score)}`}>
                {data.score}
              </span>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'overview', label: 'Overview' },
              { id: 'insights', label: 'Insights' },
              { id: 'recommendations', label: 'Recommendations' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="min-h-[200px]">
          {activeTab === 'overview' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="space-y-6"
            >
              {/* Score Breakdown */}
              <div>
                <h5 className="text-sm font-medium text-gray-900 mb-3">Score Breakdown</h5>
                <div className="space-y-3">
                  {Object.entries(data.breakdown).map(([key, value]) => (
                    <div key={key} className="flex items-center justify-between">
                      <span className="text-sm text-gray-600 capitalize">
                        {key.replace('_', ' ')}
                      </span>
                      <div className="flex items-center space-x-2">
                        <div className="w-24 bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full ${getScoreBgColor(value * 100)}`}
                            style={{ width: `${value * 100}%' }}
                          />
                        </div>
                        <span className="text-sm font-medium text-gray-900 w-8">
                          {Math.round(value * 100)}%
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Benchmarks */}
              {data.benchmarks && (
                <div>
                  <h5 className="text-sm font-medium text-gray-900 mb-3">Industry Benchmarks</h5>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gray-50 rounded-lg p-3">
                      <div className="text-xs text-gray-600">Industry Average</div>
                      <div className="text-lg font-semibold text-gray-900">
                        {data.benchmarks.industry_average || 75}
                      </div>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-3">
                      <div className="text-xs text-gray-600">Your Percentile</div>
                      <div className="text-lg font-semibold text-gray-900">
                        {data.benchmarks.your_percentile || Math.round(data.score)}%
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Anomalies */}
              {data.anomalies && data.anomalies.length > 0 && (
                <div>
                  <h5 className="text-sm font-medium text-gray-900 mb-3">
                    Detected Anomalies ({data.anomalies.length})
                  </h5>
                  <div className="space-y-2">
                    {data.anomalies.slice(0, 3).map((anomaly, index) => (
                      <div key={index} className="flex items-center space-x-2 text-sm text-orange-600">
                        <ExclamationTriangleIcon className="h-4 w-4" />
                        <span>
                          ${anomaly.amount.toLocaleString()} at {anomaly.vendor} on {anomaly.date}
                        </span>
                      </div>
                    ))}
                    {data.anomalies.length > 3 && (
                      <div className="text-xs text-gray-500">
                        +{data.anomalies.length - 3} more anomalies
                      </div>
                    )}
                  </div>
                </div>
              )}
            </motion.div>
          )}

          {activeTab === 'insights' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="space-y-4"
            >
              {data.insights && data.insights.length > 0 ? (
                data.insights.map((insight, index) => (
                  <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                    <InformationCircleIcon className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-blue-800">{insight}</p>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <InformationCircleIcon className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                  <p>No insights available at this time.</p>
                </div>
              )}
            </motion.div>
          )}

          {activeTab === 'recommendations' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="space-y-4"
            >
              {data.recommendations && data.recommendations.length > 0 ? (
                data.recommendations.map((recommendation, index) => (
                  <div key={index} className="flex items-start space-x-3 p-3 bg-green-50 rounded-lg">
                    <CheckCircleIcon className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-green-800">{recommendation}</p>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <CheckCircleIcon className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                  <p>No recommendations available at this time.</p>
                </div>
              )}
            </motion.div>
          )}
        </div>
      </div>
    </div>
  )
}

export default SpendScoreCard
