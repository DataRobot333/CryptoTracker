# CryptoTracker Architecture

## System Overview

This project is an automated cryptocurrency data pipeline running on a Raspberry Pi ( for now, planning to ship everything into linux vps).

## Data Flow

CoinMarketCap API   
↓  
Python Collector (collector.py)  ==> completed
↓  
Environment Variables (.env)  ==> completed  
↓  
PostgreSQL Database ==> completed (evolve as project progress)
↓  
SQL Queries / Analytics Layer ==> in progress
↓  
Dashboard (future: Grafana / Metabase) ==> future plan
↓  
Alert System (future: Telegram Bot) ==> future plan
  
## Components

### 1. Data Collection Layer

* Python script runs on scheduled 10 min intervals (cron) 
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
* volume base analysis

### 5. Visualization Layer (Planned)

* Grafana or Metabase dashboards
* Real-time and historical insights

### 6. Notification Layer (Planned)

* Telegram alerts for price movements
* Rule-based triggers
