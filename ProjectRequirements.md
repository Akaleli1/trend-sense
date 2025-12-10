## 📄 Project Requirements Document: Tech Trend Sentiment Analyst

This document outlines the scope, objectives, technical requirements, and career goals for the "Tech Trend Sentiment Analyst" project.

### 1. Project Goal

To build a full-stack, data-driven platform that analyzes large volumes of text data from technical communities and news sources, utilizes AI for sentiment scoring, and visualizes the results to track technology trends over time.

### 2. Core Requirements & Features

* **Data Acquisition (ETL - Extract):** Implement a Python script to periodically pull data from 3rd party APIs (e.g., Reddit API, News API) based on configurable tech keywords (e.g., "Next.js," "TypeScript," "AI").
* **AI Processing (ETL - Transform):**
    * Integrate with an LLM API (e.g., OpenAI, Gemini).
    * Use **Prompt Engineering** to obtain structured, numerical output.
    * Output must include a **Sentiment Score** (numerical float between -1.0 and +1.0) and a brief summary.
* **Data Storage (ETL - Load):** Store the processed, enriched data in a **SQLite** database.
* **Data Visualization (Frontend):** Develop a dashboard to display time-series analysis of sentiment scores for different technologies (e.g., a line graph showing Next.js sentiment over the last 30 days).
* **User Interface:** A fast, responsive, and accessible UI built with Next.js. Must include filtering/search capabilities by keyword and time range.

### 3. Technical Stack (Production Focus)

This stack is optimized for modern development and showcases current industry best practices.

| Component | Technology | Rationale & Career Fit |
| :--- | :--- | :--- |
| **Frontend Framework** | **Next.js (React)** | [cite_start]Demonstrates strong experience in modern, performant web development[cite: 36]. Provides SSR and routing. |
| **Styling** | **Tailwind CSS** | Fast, utility-first styling for production-ready UI. |
| **Backend / API** | **Python (Flask/FastAPI)** | Industry standard for data processing and AI integration. [cite_start]Leverages existing Flask knowledge[cite: 37]. |
| **Data Engineering** | **Python** ETL Script | Core component to showcase **Data Engineering** skills. |
| **Database** | **SQLite** | Simplifies setup for a Jr-friendly project while demonstrating database management. |
| **Hosting** | **Vercel** | Seamless deployment for Next.js and Vercel Serverless Functions for the Python backend. |
| **Quality Assurance (QA)** | **Cypress** | [cite_start]Mandatory E2E testing for critical user flows[cite: 37]. |
| **Unit Testing** | **Jest** | [cite_start]Unit testing for React components and logic[cite: 37]. |

### 4. Career and Skill Demonstration Goals

This project must specifically highlight the following skills, aligning with the resume and career goals:

* [cite_start]**Frontend Expertise:** Advanced use of React/Next.js and ensuring high **UI quality**[cite: 36].
* [cite_start]**API Development/Integration:** Implementing a custom Python API for data processing and integrating with external APIs (Reddit, News)[cite: 6, 36].
* [cite_start]**Data Engineering/Analysis:** Executing the **Extract, Transform (AI), and Load** process and presenting analytical insights (time-series data)[cite: 33].
* **Artificial Intelligence (AI):** Practical application of LLM APIs for structured data extraction (sentiment scoring and summarization).
* [cite_start]**DevOps/Deployment:** Showcasing seamless CI/CD and **cloud deployment** using Vercel[cite: 9, 36].
* [cite_start]**QA Commitment:** Implementing rigorous testing practices (Cypress, Jest)[cite: 5, 36].