'use client';

import { useState, useEffect } from 'react';
import { Activity, BarChart3, TrendingUp, TrendingDown, ArrowUp, ArrowDown } from 'lucide-react';

interface KeywordStat {
  keyword: string;
  avg_sentiment: number;
}

interface StatsData {
  total_articles: number;
  average_sentiment: number;
  top_keywords: KeywordStat[];
  bottom_keywords: KeywordStat[];
}

interface ApiResponse {
  success: boolean;
  stats: StatsData;
  error?: string;
}

export default function StatsCards() {
  const [stats, setStats] = useState<StatsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  // Hydration fix: only render content after component has mounted
  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return;

    const fetchStats = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch('http://127.0.0.1:5000/api/stats');
        const result: ApiResponse = await response.json();
        
        if (result.success && result.stats) {
          setStats(result.stats);
        } else {
          setError(result.error || 'Failed to fetch statistics');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
        console.error('Error fetching stats:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [mounted]);

  const formatSentimentPercentage = (score: number): string => {
    // Convert -1 to 1 range to percentage
    const percentage = ((score + 1) / 2) * 100;
    const sign = score >= 0 ? '+' : '';
    return `${sign}${percentage.toFixed(0)}%`;
  };

  const getSentimentColor = (score: number): string => {
    if (score > 0) return 'text-green-500';
    if (score < 0) return 'text-red-500';
    return 'text-slate-400';
  };

  // Prevent hydration mismatch by not rendering until mounted
  if (!mounted) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-slate-900/50 rounded-xl border border-slate-800 p-6 shadow-sm">
          <p className="text-sm text-slate-400">Loading stats...</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-slate-900/50 rounded-xl border border-slate-800 p-6 shadow-sm">
          <p className="text-sm text-slate-400">Loading stats...</p>
        </div>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-slate-900/50 rounded-xl border border-red-800 p-6 shadow-sm">
          <p className="text-sm text-red-400">
            {error || 'Failed to load statistics'}
          </p>
        </div>
      </div>
    );
  }

  const sentimentColor = getSentimentColor(stats.average_sentiment);
  const sentimentScore = formatSentimentPercentage(stats.average_sentiment);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {/* Card 1: Sentiment */}
      <div className="bg-slate-900/50 rounded-xl border border-slate-800 p-6 shadow-sm">
        <div className="flex items-start justify-between mb-4">
          <div>
            <p className="text-sm font-medium text-slate-400 mb-2">Overall Market Sentiment</p>
            <p className={`text-4xl font-bold ${sentimentColor}`}>{sentimentScore}</p>
          </div>
          <Activity className="w-6 h-6 text-slate-500" />
        </div>
      </div>

      {/* Card 2: Total Articles */}
      <div className="bg-slate-900/50 rounded-xl border border-slate-800 p-6 shadow-sm">
        <div className="flex items-start justify-between mb-4">
          <div>
            <p className="text-sm font-medium text-slate-400 mb-2">Total Articles</p>
            <p className="text-4xl font-bold text-white">{stats.total_articles.toLocaleString()}</p>
          </div>
          <BarChart3 className="w-6 h-6 text-slate-500" />
        </div>
      </div>

      {/* Card 3: Top Performers (Green Up Arrow) */}
      <div className="bg-slate-900/50 rounded-xl border border-slate-800 p-6 shadow-sm">
        <div className="flex items-start justify-between mb-4">
          <div>
            <p className="text-sm font-medium text-slate-400 mb-2">Top Performers</p>
          </div>
          <TrendingUp className="w-6 h-6 text-green-500" />
        </div>
        {stats.top_keywords.length > 0 ? (
          <div className="space-y-3">
            {stats.top_keywords.map((item, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <ArrowUp className="w-4 h-4 text-green-500" />
                  <span className="text-white font-semibold">{item.keyword}</span>
                </div>
                <span className="text-sm text-green-500 font-medium">
                  {item.avg_sentiment.toFixed(2)}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-slate-500">No data available</p>
        )}
      </div>

      {/* Card 4: Needs Attention (Red Down Arrow) */}
      <div className="bg-slate-900/50 rounded-xl border border-slate-800 p-6 shadow-sm">
        <div className="flex items-start justify-between mb-4">
          <div>
            <p className="text-sm font-medium text-slate-400 mb-2">Needs Attention</p>
          </div>
          <TrendingDown className="w-6 h-6 text-red-500" />
        </div>
        {stats.bottom_keywords.length > 0 ? (
          <div className="space-y-3">
            {stats.bottom_keywords.map((item, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <ArrowDown className="w-4 h-4 text-red-500" />
                  <span className="text-white font-semibold">{item.keyword}</span>
                </div>
                <span className="text-sm text-red-500 font-medium">
                  {item.avg_sentiment.toFixed(2)}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-slate-500">No data available</p>
        )}
      </div>
    </div>
  );
}
