# Book Scraper & Weather Lookup App:
## Introduction
This project comprises two parts:
- Book Scraper app that daily scrapes data from a book retailer 
- Weather Lookup app for real-time weather lookups. 

Utilizing Streamlit, the Book Scraper stores book information in a database, while the Weather app allows users to search weather conditions by location.

## Running the Apps
1. Book Scraper App

    - Clone this repository and set up your virtual environment:
        ```bash
        pip install -r requirements.txt
        ```
    - Optional: Create a database and replace the database URL in '.env":
        ```bash
        DATABASE_URL=[YOUR DATABASE URL]
        ```
    - Run the app:
        ```bash
        streamlit run app.py
        ```
    - Github Action allows book_scraper script runs at 5pm every day.
    - Webpage Preview

2. Weather App
    - Run the app:
        ```bash
        streamlit run weather_app.py
        ```
    - Webpage Preview

## Lessons Learned
- Web Scraping: Automated data extraction from web pages into a structured database.
- Data Visualization: Developed a Streamlit interface to filter and visualize book data effectively.
- API Utilization: Integrated multiple APIs to convert location queries into weather forecasts.

## Future Improvements
- Enhanced Functionality: Add more complex query capabilities and batch scraping for books.
- User Experience: Improve the app's design for a more engaging user interface.
- Extended Forecasts: Include longer-term weather forecasts and historical data.