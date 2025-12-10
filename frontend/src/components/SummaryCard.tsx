'use client';

import { formatSentimentScore, getSentimentLabel, getSentimentColor } from '@/lib/utils';

interface SummaryCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  sentimentScore?: number;
}

export default function SummaryCard({ title, value, subtitle, sentimentScore }: SummaryCardProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
        {title}
      </h3>
      <div className="mt-2">
        <p className="text-3xl font-semibold text-gray-900 dark:text-gray-100">
          {value}
        </p>
        {sentimentScore !== undefined && (
          <div className="mt-2">
            <p className={`text-lg font-medium ${getSentimentColor(sentimentScore)}`}>
              {formatSentimentScore(sentimentScore)} - {getSentimentLabel(sentimentScore)}
            </p>
          </div>
        )}
        {subtitle && (
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {subtitle}
          </p>
        )}
      </div>
    </div>
  );
}

