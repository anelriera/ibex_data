# IBEX 35 Data Pipeline

An end-to-end data pipeline that extracts real-time financial data from all 35 companies in the Spanish IBEX index, stores it in the cloud, and visualizes it through an interactive live dashboard.

This project was built as a hands-on learning exercise to explore **Looker Studio** for data visualization and **MongoDB Atlas** for cloud-based historical storage — using a real-world financial dataset as the foundation.

## What it does

1. **Extracts** real-time prices and technical metadata from Yahoo Finance (Sector, P/E Ratio, Dividend Yield, volatility, 52-week highs/lows, and more)
2. **Calculates** key performance metrics: daily, weekly, and monthly variation, annualized volatility, and position within annual range
3. **Syncs** the processed data to Google Sheets via a Google Cloud Service Account
4. **Visualizes** everything in a live Looker Studio dashboard with interactive filters by sector, volatility, and performance
5. **Stores** daily snapshots in MongoDB Atlas to enable historical querying and trend analysis over time

## Live Dashboard

👉 [View the dashboard](https://datastudio.google.com/reporting/b771d15f-10c1-4c50-8141-41bd5352a9a1)

<img width="1031" height="772" alt="image" src="https://github.com/user-attachments/assets/60f2d571-f8f3-486f-a512-ae17934ef32c" />

## Tech Stack

- **Python** — data extraction and transformation
- **yfinance** — Yahoo Finance API wrapper
- **pandas** — data processing
- **gspread + Google Cloud** — Google Sheets sync via Service Account
- **Looker Studio** — live dashboard and visualization
- **MongoDB Atlas + pymongo** — cloud database for historical snapshot storage

## Setup

Make sure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

### Google Sheets Configuration

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/) and enable the **Google Sheets API** and **Google Drive API**
2. Create a **Service Account** and download its private key as JSON
3. Rename the file to `credentials.json` and place it in the project folder
4. Share your Google Sheet with the `client_email` inside that JSON (Editor permissions)
5. Paste your Google Sheet URL at the bottom of `ibex_scraper.py`

> **⚠️ Security**: Never upload `credentials.json` to public repositories. The `.gitignore` in this project is already configured to ignore it.

### MongoDB Configuration

The pipeline notebook (`mongo_pipeline.ipynb`) connects to MongoDB Atlas via a connection string stored as a **Colab Secret** (`MONGO_URI`). Never hardcode credentials in the notebook.

## Usage

```bash
python ibex_scraper.py
```

The script takes 1–2 minutes to pull data from all 35 companies and sync to Google Sheets. For MongoDB ingestion and historical analysis, run `mongo_pipeline.ipynb` in Google Colab.

## Roadmap

- [x] Yahoo Finance data extraction
- [x] Google Sheets sync via Service Account
- [x] Looker Studio live dashboard
- [x] MongoDB Atlas integration for historical storage and querying
