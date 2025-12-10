'use client';

import { useMemo } from 'react';
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
import { SentimentData } from '@/lib/api';
import { formatDisplayDate, formatSentimentScore } from '@/lib/utils';

interface SentimentChartProps {
  data: SentimentData[];
  keyword?: string;
}

interface ChartDataPoint {
  date: string;
  averageSentiment: number;
  count: number;
}

export default function SentimentChart({ data, keyword }: SentimentChartProps) {
  const chartData = useMemo(() => {
    if (!data || data.length === 0) return [];

    // Group by date and calculate average sentiment
    const grouped = data.reduce((acc, item) => {
      const date = item.created_at.split('T')[0]; // Get date part only
      if (!acc[date]) {
        acc[date] = { total: 0, count: 0 };
      }
      acc[date].total += item.sentiment_score;
      acc[date].count += 1;
      return acc;
    }, {} as Record<string, { total: number; count: number }>);

    // Convert to array and calculate averages
    const chartDataPoints: ChartDataPoint[] = Object.entries(grouped)
      .map(([date, stats]) => ({
        date,
        averageSentiment: stats.total / stats.count,
        count: stats.count,
      }))
      .sort((a, b) => a.date.localeCompare(b.date));

    return chartDataPoints;
  }, [data]);

  if (chartData.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
          Sentiment Trend {keyword && `- ${keyword}`}
        </h2>
        <div className="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
          No data available for the selected filters
        </div>
      </div>
    );
  }

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-gray-800 p-3 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg">
          <p className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
            {formatDisplayDate(label)}
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Average Sentiment: <span className="font-semibold">{formatSentimentScore(payload[0].value)}</span>
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Articles: <span className="font-semibold">{payload[0].payload.count}</span>
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
        Sentiment Trend {keyword && `- ${keyword}`}
      </h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="date"
            tickFormatter={(value) => formatDisplayDate(value)}
            stroke="#6b7280"
          />
          <YAxis
            domain={[-1, 1]}
            tickFormatter={(value) => formatSentimentScore(value)}
            stroke="#6b7280"
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Line
            type="monotone"
            dataKey="averageSentiment"
            name="Average Sentiment"
            stroke="#0ea5e9"
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

