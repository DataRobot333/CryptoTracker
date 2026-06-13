# CryptoTracker Architecture

## System Overview

This project is an automated cryptocurrency data pipeline running on a Raspberry Pi.

## Data Flow

CoinMarketCap API  
↓  
Python Collector (collector.py)  
↓  
Environment Variables (.env)  
↓  
PostgreSQL Database  
↓  
SQL Queries / Analytics Layer  
↓  
Dashboard (future: Grafana / Metabase)  
↓  
Alert System (future: Telegram Bot)  
  
## Components

### 1. Data Collection Layer

* Python script runs on scheduled intervals (cron)
* Fetches real-time crypto market data from API

### 2. Storage Layer

* PostgreSQL database
* Stores:

  * Coin metadata
  * Price snapshots
  * Market statistics

### 3. Configuration Layer

* `.env` file stores secrets safely
* `python-dotenv` loads environment variables

### 4. Future Analytics Layer

* SQL-based analysis
* Trend detection
* Market behavior tracking

### 5. Visualization Layer (Planned)

* Grafana or Metabase dashboards
* Real-time and historical insights

### 6. Notification Layer (Planned)

* Telegram alerts for price movements
* Rule-based triggers
