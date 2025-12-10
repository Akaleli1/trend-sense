'use client';

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
import { TrendingUp } from 'lucide-react';

// Mock data representing Tech Sentiment over Time for Next.js
const mockData = [
  { date: '2024-01-01', sentiment: 0.65, articles: 12 },
  { date: '2024-01-08', sentiment: 0.72, articles: 15 },
  { date: '2024-01-15', sentiment: 0.68, articles: 18 },
  { date: '2024-01-22', sentiment: 0.75, articles: 20 },
  { date: '2024-01-29', sentiment: 0.70, articles: 16 },
  { date: '2024-02-05', sentiment: 0.78, articles: 22 },
  { date: '2024-02-12', sentiment: 0.82, articles: 25 },
  { date: '2024-02-19', sentiment: 0.79, articles: 23 },
  { date: '2024-02-26', sentiment: 0.85, articles: 28 },
  { date: '2024-03-05', sentiment: 0.88, articles: 30 },
];

interface CustomTooltipProps {
  active?: boolean;
  payload?: Array<{
    value: number;
    payload: {
      date: string;
      sentiment: number;
      articles: number;
    };
  }>;
  label?: string;
}

const CustomTooltip = ({ active, payload, label }: CustomTooltipProps) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-white dark:bg-gray-800 p-3 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg">
        <p className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
          {new Date(label || '').toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
          })}
        </p>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Sentiment: <span className="font-semibold text-blue-600">{data.sentiment.toFixed(2)}</span>
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
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-2">
            Tech Sentiment Over Time
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Next.js sentiment analysis (Mock Data)
          </p>
        </div>
        <div className="flex items-center gap-2 text-green-600">
          <TrendingUp className="w-5 h-5" />
          <span className="text-sm font-medium">Positive Trend</span>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={mockData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
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
            domain={[0, 1]}
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
            {(mockData.reduce((sum, d) => sum + d.sentiment, 0) / mockData.length).toFixed(2)}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400">Total Articles</p>
          <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            {mockData.reduce((sum, d) => sum + d.articles, 0)}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400">Time Period</p>
          <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            {mockData.length} weeks
          </p>
        </div>
      </div>
    </div>
  );
}

