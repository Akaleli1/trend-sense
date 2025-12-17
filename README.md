# 🚀 TechPulse Dashboard

**TechPulse Dashboard** is a full-stack real-time analytics platform designed to track technology trends and analyze market sentiment using Artificial Intelligence.

The application aggregates news from **Hacker News** and **News API**, analyzes the sentiment of headlines using **Google Gemini AI**, and visualizes the data through an interactive dashboard.

![TechPulse Dashboard](https://via.placeholder.com/800x450.png?text=Dashboard+Screenshot+Here)
*(You can replace this link with a real screenshot later)*

## 🌟 Key Features

- **🧠 AI-Powered Analysis:** Uses **Google Gemini AI** to calculate sentiment scores (-1.0 to +1.0) for every article.
- **⚡ Smart Caching System:** Implements an intelligent database caching layer. It checks if an article has already been analyzed to minimize API quota usage and latency.
- **📊 Interactive Visualization:** Features dynamic line charts (Recharts) and summary statistics cards to visualize trends over time.
- **🛠️ Robust ETL Pipeline:** A custom Python ETL (Extract, Transform, Load) process fetches, cleans, and stores data in a local SQLite database.
- **🎨 Modern UI:** Built with **Next.js 14**, **Tailwind CSS**, and **Lucide Icons**, featuring a dark-mode friendly professional design.

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | **Next.js (React)** | Server-side rendering, routing, and UI components. |
| **Styling** | **Tailwind CSS** | Utility-first CSS framework for modern styling. |
| **Backend** | **Python (Flask)** | RESTful API and ETL pipeline orchestration. |
| **Database** | **SQLite** | Local relational database for high-performance data persistence. |
| **AI Engine** | **Google Gemini API** | Natural Language Processing (NLP) for sentiment analysis. |
| **Data Sources** | **Hacker News, News API** | External APIs for fetching real-time tech news. |

## 🚀 Getting Started

Follow these instructions to run the project locally.

### Prerequisites
- Node.js & npm
- Python 3.8+
- API Keys for **Google Gemini** and **News API**.

### 1. Backend Setup (Python)

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your API keys
# FLASK_APP=app.py
# FLASK_ENV=development
# GEMINI_API_KEY=your_gemini_key
# NEWS_API_KEY=your_news_api_key

# Run the server (Runs on Port 5001)
python app.py
2. Frontend Setup (Next.js)
Open a new terminal window:

Bash

cd frontend

# Install dependencies
npm install

# Run the development server (Runs on Port 3000)
npm run dev
3. Usage
Open your browser and go to http://localhost:3000.

The dashboard will automatically fetch data from the local database.

To fetch new data from the internet and trigger AI analysis, you can hit the ETL endpoint (or use the built-in trigger if implemented).

📂 Project Structure
TrendSense/
├── backend/             # Flask API & ETL Logic
│   ├── data/            # SQLite Database location
│   ├── database/        # DB Connection & Schema
│   ├── etl/             # Data Fetcher & AI Analysis Scripts
│   └── app.py           # Main Entry Point
├── frontend/            # Next.js Application
│   ├── src/
│   │   ├── components/  # Reusable UI Components (Charts, Cards)
│   │   └── app/         # Pages & Routing
│   └── tailwind.config  # Style Configuration
└── README.md            # Project Documentation
🛡️ License
This project is open-source and available under the MIT License.