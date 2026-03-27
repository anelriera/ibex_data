# IBEX 35 Data Pipeline 

A Python script that automates the extraction of financial data from IBEX 35 companies (using Yahoo Finance) and sends it directly to Google Sheets via its official API.

Ideal for use as a live data source for **Looker Studio** or Power BI dashboards.

## What does the script do?

1. **Downloads in real-time** the prices of the 35 companies in the Spanish IBEX index.
2. **Extracts technical metadata**: Sector, Industry, Country, P/E Ratio, Dividend Yield, etc.
3. **Calculates key metrics**: Daily/Weekly/Monthly variation, annualized volatility, and distances to 52-week highs/lows.
4. **Syncs with the Cloud**: Clears old data and writes the updated table to a Google Sheet through a Google Cloud Service Account.

## Prerequisites (Installation)

Make sure you have Python installed, then install the required libraries by running:

```bash
pip install -r requirements.txt
```

## Google Sheets Configuration (Service Account)

For the script to have permission to edit your Google Sheet, you need to:

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/) and enable the **Google Sheets API** and **Google Drive API**.
2. Create a **Service Account** and generate a private key in JSON format.
3. Download that file, rename it to `credentials.json`, and save it in the same folder as this script.
4. Copy the `client_email` from inside that JSON, go to your Google Sheet in the browser, and **grant Editor permissions** to that email.
5. Paste your Google Sheet URL at the end of the `ibex_scraper.py` file.

> **⚠️ SECURITY WARNING**: Never upload your `credentials.json` file to public repositories like GitHub. The `.gitignore` file included in this project is already configured to automatically ignore it.

## Usage

Simply run the script in your terminal. It will take between 1 and 2 minutes to gather all the information from Yahoo Finance and upload it automatically.

```bash
python ibex_scraper.py
```
