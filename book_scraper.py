import os
import requests
from bs4 import BeautifulSoup
import psycopg2
from dotenv import load_dotenv

load_dotenv()
# Connect to PostgreSQL database
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

def clear_database():
    try:
        cur.execute("DELETE FROM books")
        conn.commit()
        print("Database cleared.")
    except Exception as e:
        print("Error clearing the database:", e)
        conn.rollback()
clear_database()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        price DECIMAL(5,2),
        rating INTEGER
    )
    """
)

# scrape book_description
def scrape_book_details(book_url):
    response = requests.get(book_url)
    book_soup = BeautifulSoup(response.text, 'html.parser')
    description_tag = book_soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'].strip() if description_tag else "No description available"
    return description

# scrape book data
def book_scrapper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = soup.find_all('article', class_='product_pod')

    rating_convert = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        'Four': 4,
        'Five': 5
    }
    index = 0
    for book in books:
        title = book.find('h3').find('a')['title']
        price = book.find('p', class_='price_color').text[2:]
        rating = rating_convert[book.find('p', class_='star-rating')['class'][1]]
        book_url = 'https://books.toscrape.com/catalogue/' + book.find('h3').find('a')['href']
        print(book_url)
        description = scrape_book_details(book_url)
        cur.execute(
            "INSERT INTO books (title, description, price, rating) VALUES(%s, %s, %s, %s)", 
            (title,description, price, rating)
        )
        print("book",index)
        index += 1
    conn.commit()

# book scraper
index = 1
while index <= 50:
    url = f"https://books.toscrape.com/catalogue/page-{index}.html"
    print("Scraping " + url)
    book_scrapper(url)
    
    index += 1