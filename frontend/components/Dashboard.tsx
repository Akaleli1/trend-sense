'use client';

import { useState, useEffect } from 'react';
import { fetchSentiments, fetchStats, SentimentData } from '@/lib/api';
import FilterBar, { FilterState } from './FilterBar';
import SentimentChart from './SentimentChart';
import SummaryCard from './SummaryCard';
import { formatDateForAPI, getDateNDaysAgo, formatSentimentScore, getSentimentColor, formatDisplayDate } from '@/lib/utils';

export default function Dashboard() {
  const [sentiments, setSentiments] = useState<SentimentData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState({ total_count: 0, average_sentiment: 0 });
  const [filters, setFilters] = useState<FilterState>({
    keyword: '',
    source: '',
    startDate: formatDateForAPI(getDateNDaysAgo(30)),
    endDate: formatDateForAPI(new Date()),
  });

  useEffect(() => {
    loadData();
  }, [filters]);

  async function loadData() {
    setLoading(true);
    setError(null);

    try {
      // Fetch sentiments
      const sentimentsResponse = await fetchSentiments({
        keyword: filters.keyword || undefined,
        source: filters.source || undefined,
        start_date: filters.startDate || undefined,
        end_date: filters.endDate || undefined,
      });

      if (sentimentsResponse.success) {
        setSentiments(sentimentsResponse.data);
      } else {
        setError(sentimentsResponse.error || 'Failed to load sentiments');
      }

      // Fetch stats
      const statsResponse = await fetchStats(filters.keyword || undefined);
      if (statsResponse.success) {
        setStats(statsResponse.stats);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }

  if (loading && sentiments.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/4 mb-6"></div>
            <div className="h-64 bg-gray-200 dark:bg-gray-700 rounded mb-6"></div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="h-32 bg-gray-200 dark:bg-gray-700 rounded"></div>
              <div className="h-32 bg-gray-200 dark:bg-gray-700 rounded"></div>
              <div className="h-32 bg-gray-200 dark:bg-gray-700 rounded"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-8">
          Tech Trend Sentiment Analyst
        </h1>

        {error && (
          <div className="mb-6 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-200 px-4 py-3 rounded-lg">
            <p className="font-medium">Error: {error}</p>
          </div>
        )}

        <FilterBar filters={filters} onFilterChange={setFilters} />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <SummaryCard
            title="Total Articles"
            value={stats.total_count}
            subtitle="All time"
          />
          <SummaryCard
            title="Average Sentiment"
            value={formatSentimentScore(stats.average_sentiment)}
            sentimentScore={stats.average_sentiment}
            subtitle="Overall sentiment"
          />
          <SummaryCard
            title="Filtered Results"
            value={sentiments.length}
            subtitle="Current view"
          />
        </div>

        <div className="mb-6">
          <SentimentChart data={sentiments} keyword={filters.keyword || undefined} />
        </div>

        {sentiments.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
              Recent Sentiments
            </h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Title
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Source
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Sentiment
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Date
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {sentiments.slice(0, 10).map((sentiment) => (
                    <tr key={sentiment.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {sentiment.title || 'No title'}
                        </div>
                        <div className="text-sm text-gray-500 dark:text-gray-400 truncate max-w-md">
                          {sentiment.summary}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                          {sentiment.source}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`text-sm font-medium ${getSentimentColor(sentiment.sentiment_score)}`}>
                          {formatSentimentScore(sentiment.sentiment_score)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        {formatDisplayDate(sentiment.created_at)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

