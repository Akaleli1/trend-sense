# Tech Trend Sentiment Analyst

A full-stack, data-driven platform that analyzes large volumes of text data from technical communities and news sources, utilizes AI for sentiment scoring, and visualizes the results to track technology trends over time.

## 🎯 Project Overview

This project demonstrates modern full-stack development practices with:
- **Data Engineering**: ETL pipeline for extracting, transforming, and loading data
- **AI Integration**: Google Gemini API for sentiment analysis
- **Backend API**: Flask REST API serving processed data
- **Frontend Dashboard**: Next.js dashboard with time-series visualizations
- **Quality Assurance**: Comprehensive testing with Jest and Cypress

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐
│ Reddit API  │     │  News API   │
└──────┬──────┘     └──────┬──────┘
       │                   │
       └─────────┬──────────┘
                 │
         ┌───────▼────────┐
         │  ETL Extract   │
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │ ETL Transform  │
         │  (Gemini API)   │
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │   ETL Load     │
         │  (SQLite DB)   │
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │   Flask API    │
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │  Next.js UI    │
         └────────────────┘
```

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn
- API Keys:
  - Google Gemini API key
  - Reddit API credentials (Client ID, Client Secret)
  - News API key

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd TrendSense
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install
```

### 4. Environment Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your API keys:
   - `GEMINI_API_KEY`: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`: Create at [Reddit Apps](https://www.reddit.com/prefs/apps)
   - `NEWS_API_KEY`: Get from [NewsAPI](https://newsapi.org/register)

### 5. Initialize Database

The database will be automatically created when you first run the ETL pipeline or start the Flask server.

### 6. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

The Flask API will be available at `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

The Next.js app will be available at `http://localhost:3000`

## 📊 Running the ETL Pipeline

To collect and process data:

```bash
cd backend
source venv/bin/activate
python -m backend.etl.main
```

Or with custom keywords:
```bash
python -m backend.etl.main --keywords "Python,JavaScript,React"
```

The ETL pipeline will:
1. **Extract** data from Reddit and News APIs
2. **Transform** using Gemini API for sentiment analysis
3. **Load** results into SQLite database

## 🧪 Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/backend/
# or
python -m unittest discover tests/backend/
```

### Frontend Unit Tests

```bash
cd frontend
npm test
```

### E2E Tests

```bash
cd frontend
npm run cypress:open
# or for headless mode
npm run cypress:run
```

## 📡 API Endpoints

### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00"
}
```

### `GET /api/sentiments`
Retrieve sentiment data with optional filters.

**Query Parameters:**
- `keyword` (optional): Filter by keyword
- `source` (optional): Filter by source (`reddit` or `news`)
- `start_date` (optional): Start date (YYYY-MM-DD)
- `end_date` (optional): End date (YYYY-MM-DD)
- `limit` (optional): Maximum number of results

**Example:**
```bash
curl "http://localhost:5000/api/sentiments?keyword=Python&start_date=2024-01-01&end_date=2024-01-31"
```

**Response:**
```json
{
  "success": true,
  "count": 10,
  "data": [
    {
      "id": 1,
      "keyword": "Python",
      "source": "reddit",
      "title": "Python is great!",
      "content": "...",
      "url": "https://...",
      "sentiment_score": 0.75,
      "summary": "Positive discussion about Python...",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

### `GET /api/keywords`
Get all available keywords.

**Response:**
```json
{
  "success": true,
  "keywords": ["Python", "JavaScript", "React", ...]
}
```

### `GET /api/stats`
Get statistics for sentiments.

**Query Parameters:**
- `keyword` (optional): Filter by keyword

**Example:**
```bash
curl "http://localhost:5000/api/stats?keyword=Python"
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_count": 150,
    "average_sentiment": 0.65
  }
}
```

## 🎨 Frontend Features

- **Interactive Dashboard**: Real-time sentiment visualization
- **Time-Series Charts**: Track sentiment trends over time
- **Advanced Filtering**: Filter by keyword, source, and date range
- **Summary Statistics**: View total articles and average sentiment
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Mode Support**: Automatic theme switching

## 📁 Project Structure

```
TrendSense/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── config.py              # Configuration management
│   ├── etl/                   # ETL pipeline
│   │   ├── extract.py         # Data extraction
│   │   ├── transform.py       # AI transformation
│   │   ├── load.py            # Database loading
│   │   └── main.py            # ETL orchestration
│   ├── database/              # Database utilities
│   │   ├── db.py              # Database operations
│   │   └── schema.sql         # Database schema
│   ├── models/                # Data models
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── app/                   # Next.js App Router
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/            # React components
│   │   ├── Dashboard.tsx
│   │   ├── SentimentChart.tsx
│   │   ├── FilterBar.tsx
│   │   └── SummaryCard.tsx
│   ├── lib/                   # Utilities
│   │   ├── api.ts             # API client
│   │   └── utils.ts           # Helper functions
│   └── package.json
├── tests/
│   └── backend/               # Backend tests
├── cypress/
│   └── e2e/                  # E2E tests
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables

See `.env.example` for all available configuration options. Key variables:

- **API Keys**: Required for data sources and AI processing
- **Database Path**: Where SQLite database is stored
- **Flask Configuration**: Server host, port, and debug mode
- **ETL Settings**: Keywords to track, fetch limits

### Customizing Keywords

Edit the `KEYWORDS` environment variable in `.env`:

```env
KEYWORDS=Python,JavaScript,React,Next.js,TypeScript,AI
```

## 🚢 Deployment

### Vercel (Frontend)

1. Connect your repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push

### Backend Deployment

For production deployment, consider:
- Using a production WSGI server (Gunicorn)
- Setting up proper environment variables
- Using a production database (PostgreSQL)
- Implementing proper logging and monitoring

## 🤝 Contributing

This is an open-source project. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

[Specify your license here]

## 🙏 Acknowledgments

- Google Gemini API for AI sentiment analysis
- Reddit API for community data
- NewsAPI for news articles
- Next.js and Flask communities

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

Built with ❤️ using Next.js, Flask, and Google Gemini

