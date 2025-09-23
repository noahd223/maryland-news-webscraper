# News Webscraper and Visualization

This project is a visualization dashboard for news articles from three Maryland-based sources: the Baltimore Banner, Capital Gazette, and Hyattsville Wire. The data is stored in a PostgreSQL database hosted on Neon and is sourced through web scraping.

You can find the visualization here: https://maryland-news-visualizer.streamlit.app/ or run the app locally by following the steps below.

## Features

- **Visualization Dashboard**: Built using Streamlit, the dashboard provides various visualizations, including:
  - Articles over time
  - Headline length and word count analysis
  - Section popularity and average article length
  - Geographical map of places mentioned in articles
- **Data Filtering**: Users can filter articles by source, section, and publication date.
- **Interactive Map**: Displays places mentioned in articles with links to the original articles.

## Data Pipeline

1. **Web Scraping**: Articles are scraped from the Baltimore Banner and Capitol Gazette using custom scrapers.
2. **Database**: The scraped data is stored in a PostgreSQL database hosted on Neon.
3. **Visualization**: The data is loaded into the Streamlit app for visualization and analysis.

## Requirements

- Python 3.8+
- Required Python libraries (listed in `requirements.txt`)

## Setup (for running locally)

1. Clone the repository:
   ```bash
   git clone 
   cd News-Webscraper
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run article-visualization/visualization_app.py
   ```

## Folder Structure

- `article-visualization/`: Contains the Streamlit app for visualization.
- `scrapers/`: Contains web scrapers for the Baltimore Banner, Capitol Gazette and Hyattsville Wire.
- `requirements.txt`: Lists the required Python libraries.

## Notes

- The database is hosted on Neon and requires SSL for connections.
- We may change sourcing to a different news outlet than The Baltimore Banner due to paywalls and unreliable data.

