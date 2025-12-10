'use client';

import { useState, useEffect } from 'react';
import { fetchKeywords } from '@/lib/api';
import { formatDateForAPI, getDateNDaysAgo } from '@/lib/utils';

export interface FilterState {
  keyword: string;
  source: string;
  startDate: string;
  endDate: string;
}

interface FilterBarProps {
  filters: FilterState;
  onFilterChange: (filters: FilterState) => void;
}

export default function FilterBar({ filters, onFilterChange }: FilterBarProps) {
  const [keywords, setKeywords] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadKeywords() {
      const response = await fetchKeywords();
      if (response.success) {
        setKeywords(response.keywords);
      }
      setLoading(false);
    }
    loadKeywords();
  }, []);

  const handleChange = (field: keyof FilterState, value: string) => {
    onFilterChange({
      ...filters,
      [field]: value,
    });
  };

  const handleQuickDateRange = (days: number) => {
    const endDate = formatDateForAPI(new Date());
    const startDate = formatDateForAPI(getDateNDaysAgo(days));
    onFilterChange({
      ...filters,
      startDate,
      endDate,
    });
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
        Filters
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Keyword Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Keyword
          </label>
          <select
            value={filters.keyword}
            onChange={(e) => handleChange('keyword', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-200"
            disabled={loading}
          >
            <option value="">All Keywords</option>
            {keywords.map((keyword) => (
              <option key={keyword} value={keyword}>
                {keyword}
              </option>
            ))}
          </select>
        </div>

        {/* Source Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Source
          </label>
          <select
            value={filters.source}
            onChange={(e) => handleChange('source', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-200"
          >
            <option value="">All Sources</option>
            <option value="reddit">Reddit</option>
            <option value="news">News</option>
          </select>
        </div>

        {/* Start Date */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Start Date
          </label>
          <input
            type="date"
            value={filters.startDate}
            onChange={(e) => handleChange('startDate', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-200"
          />
        </div>

        {/* End Date */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            End Date
          </label>
          <input
            type="date"
            value={filters.endDate}
            onChange={(e) => handleChange('endDate', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-200"
          />
        </div>
      </div>

      {/* Quick Date Range Buttons */}
      <div className="mt-4 flex flex-wrap gap-2">
        <span className="text-sm text-gray-600 dark:text-gray-400 mr-2">Quick ranges:</span>
        <button
          onClick={() => handleQuickDateRange(7)}
          className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
        >
          7 days
        </button>
        <button
          onClick={() => handleQuickDateRange(30)}
          className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
        >
          30 days
        </button>
        <button
          onClick={() => handleQuickDateRange(90)}
          className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
        >
          90 days
        </button>
      </div>
    </div>
  );
}

