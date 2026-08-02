# 🛒 Trendyol Price Comparison Tool

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web_App-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Selenium](https://img.shields.io/badge/Selenium-Web_Scraping-43B02A?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A web-based application that automatically collects prices for products on Trendyol and displays them in a comparison table.
Given a product link, the app dynamically analyzes the price, shipping information, and rating of every seller offering that product. Results are shown in the web interface and can be exported as CSV.

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Example Output](#-example-output)
- [Author](#-author)

## ✨ Features

- **Automated data collection (web scraping):** Fetches dynamic page content with Selenium and parses seller data with BeautifulSoup.
- **Price comparison:** Displays price, rating, and shipping info for every seller in a single table.
- **CSV export:** Download the full table as `products.csv` with one click.
- **Web interface:** A clean, mobile-friendly Flask app built with Bootstrap 5.

## 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.9+** | Core language |
| **Flask** | Web interface |
| **Selenium** | Dynamic content scraping |
| **BeautifulSoup4 (bs4)** | HTML parsing |
| **Pandas** | Data processing and CSV export |
| **Bootstrap 5** | UI design |

## 🚀 Getting Started

1. Install the required libraries:

```bash
pip install flask selenium beautifulsoup4 pandas webdriver-manager
```

2. Project structure:

```
trendyol-price-comparison/
├── app.py                  → Flask web application
├── web.py                  → Data scraping and analysis logic
├── products.csv            → Example output file
└── templates / static      → Web page assets (optional)
```

3. Start the app:

```bash
python app.py
```

4. Open your browser at: `http://127.0.0.1:5000`

## 📖 Usage

1. Run the application.
2. Enter a Trendyol product link on the page.
3. Click **"Fetch Data."**
4. Prices from all sellers will be listed in a table — download it as CSV if you'd like.

## 📊 Example Output

| Seller Name | Price | Shipping Info | Seller Rating | Product Rating |
|---|---|---|---|---|
| Trendyol | 999.90 | Free Shipping | 9.8 | 4.7 |
| ABC Elektronik | 1015.00 | Ships in 1 Day | 9.4 | 4.7 |
| XYZ Store | 1029.99 | Free Shipping | 9.6 | 4.7 |

## 👤 Author

**Sedanur Peker**
