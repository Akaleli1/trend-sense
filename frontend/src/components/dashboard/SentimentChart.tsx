'use client';

import { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { TrendingUp, Loader2 } from 'lucide-react';

interface TrendData {
  date: string;
  keyword: string;
  name?: string; // Optional name field from backend
  sentiment: number;
  articles: number;
}

interface ApiResponse {
  success: boolean;
  count: number;
  data: TrendData[];
  error?: string;
}

interface CustomTooltipProps {
  active?: boolean;
  payload?: Array<{
    value: number;
    payload: TrendData;
  }>;
  label?: string;
}

const CustomTooltip = ({ active, payload, label }: CustomTooltipProps) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    // Get keyword from payload - try both keyword and name fields
    const keyword = data.keyword || data.name || 'Unknown';
    
    return (
      <div className="bg-white dark:bg-gray-800 p-4 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg">
        <p className="text-sm font-bold text-gray-900 dark:text-gray-100 mb-2">
          {new Date(label || '').toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
          })}
        </p>
        <p className="text-sm text-blue-600 dark:text-blue-400 font-semibold mb-1">
          Tech: {keyword}
        </p>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Sentiment: <span className="font-semibold">{data.sentiment.toFixed(2)}</span>
        </p>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Articles: <span className="font-semibold">{data.articles}</span>
        </p>
      </div>
    );
  }
  return null;
};

export default function SentimentChart() {
  const [data, setData] = useState<TrendData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch('http://127.0.0.1:5000/api/trends');
        const result: ApiResponse = await response.json();
        
        if (result.success && result.data) {
          setData(result.data);
        } else {
          setError(result.error || 'Failed to fetch trends data');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred while fetching data');
        console.error('Error fetching trends:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTrends();
  }, []);

  // Calculate statistics
  const averageSentiment = data.length > 0
    ? data.reduce((sum, d) => sum + d.sentiment, 0) / data.length
    : 0;
  
  const totalArticles = data.reduce((sum, d) => sum + d.articles, 0);
  
  // Group data by date for the chart (average sentiment per date)
  // Preserve keyword information - use the first keyword found for each date
  const chartData = data.reduce((acc, item) => {
    const date = item.date;
    if (!acc[date]) {
      acc[date] = { 
        date, 
        sentiments: [], 
        articles: 0,
        keywords: [] as string[] // Track keywords for this date
      };
    }
    acc[date].sentiments.push(item.sentiment);
    acc[date].articles += item.articles;
    // Add keyword if not already present
    if (item.keyword && !acc[date].keywords.includes(item.keyword)) {
      acc[date].keywords.push(item.keyword);
    }
    return acc;
  }, {} as Record<string, { date: string; sentiments: number[]; articles: number; keywords: string[] }>);

  const chartDataPoints = Object.values(chartData).map(item => ({
    date: item.date,
    sentiment: item.sentiments.reduce((sum, s) => sum + s, 0) / item.sentiments.length,
    articles: item.articles,
    keyword: item.keywords.length > 0 ? item.keywords.join(', ') : 'Unknown', // Preserve keyword(s)
  })).sort((a, b) => a.date.localeCompare(b.date));

  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <div className="flex items-center justify-center h-64">
          <div className="flex flex-col items-center gap-3">
            <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            <p className="text-gray-600 dark:text-gray-400">Loading trends data...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <p className="text-red-600 dark:text-red-400 font-medium mb-2">Error loading data</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">{error}</p>
            <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
              Make sure the Flask backend is running on port 5000
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (chartDataPoints.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-2">
          Tech Sentiment Over Time
        </h2>
        <div className="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
          No data available
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-2">
            Tech Sentiment Over Time
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Real-time sentiment analysis from Hacker News & News API
          </p>
        </div>
        <div className="flex items-center gap-2 text-green-600">
          <TrendingUp className="w-5 h-5" />
          <span className="text-sm font-medium">Live Data</span>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartDataPoints} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="date"
            stroke="#6b7280"
            tickFormatter={(value) => {
              return new Date(value).toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
              });
            }}
          />
          <YAxis
            domain={[-1, 1]}
            stroke="#6b7280"
            tickFormatter={(value) => value.toFixed(1)}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Line
            type="monotone"
            dataKey="sentiment"
            name="Sentiment Score"
            stroke="#0ea5e9"
            strokeWidth={3}
            dot={{ r: 5, fill: '#0ea5e9' }}
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="mt-4 grid grid-cols-3 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400">Average Sentiment</p>
          <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            {averageSentiment.toFixed(2)}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400">Total Articles</p>
          <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            {totalArticles}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400">Data Points</p>
          <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            {chartDataPoints.length}
          </p>
        </div>
      </div>
    </div>
  );
}
