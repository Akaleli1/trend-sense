import SentimentChart from '@/components/dashboard/SentimentChart';
import StatsCards from '@/components/dashboard/StatsCards';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            TechPulse Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Real-time technology sentiment analysis and trends
          </p>
        </div>
        <div className="mb-8">
          <StatsCards />
        </div>
          <SentimentChart />
      </div>
    </div>
  );
}
