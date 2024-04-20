import os
import streamlit as st
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
# Connect to PostgreSQL database
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

st.set_page_config(layout="wide")
st.title("Book Explorer")
st.sidebar.header("Filters")

# Get user input for search
search_query = st.sidebar.text_input("Search by name or description")

# Get user input for filtering
rating_filter = st.sidebar.slider("Minimum rating", 1, 5, 1)
price_filter_min, price_filter_max = st.sidebar.slider("Price range", 0.0, 100.0, (10.0, 50.0))
sort_by = st.sidebar.radio("Sort by", ["Rating", "Price"])
order_by = st.sidebar.radio("Display by", ["DESC", "ASC"])
order_clause = f"ORDER BY {sort_by.lower()} {order_by}" if sort_by else ""

# Initialize pagination settings
if 'page' not in st.session_state:
    st.session_state.page = 0
ITEMS_PER_PAGE = 20

# Build the base query for pagination
query = f"""
SELECT * FROM books
WHERE (LOWER(title) LIKE LOWER(%s) OR LOWER(description) LIKE LOWER(%s))
AND rating >= %s
AND price BETWEEN %s AND %s
{order_clause}
LIMIT %s OFFSET %s;
"""

# Execute the query with user inputs including pagination
cur.execute(query, ('%' + search_query + '%', '%' + search_query + '%', rating_filter, price_filter_min, price_filter_max, ITEMS_PER_PAGE, st.session_state.page * ITEMS_PER_PAGE))

# Fetch results
rows = cur.fetchall()

# Convert query results to a pandas DataFrame and drop the ID column
df = pd.DataFrame(rows, columns=["ID", "Title", "Description", "Price", "Rating"]).drop(columns="ID")

# Display results in the Streamlit app
st.write("Books matching your criteria:")
st.dataframe(df, width=1200)

# Pagination controls
col1, col2 = st.columns(2)
with col1:
    if st.button("Previous"):
        if st.session_state.page > 0:
            st.session_state.page -= 1

with col2:
    if st.button("Next"):
        # Query to get the total number of books that match the criteria (without pagination limit and offset)
        cur.execute("SELECT COUNT(*) FROM books WHERE (LOWER(title) LIKE LOWER(%s) OR LOWER(description) LIKE LOWER(%s)) AND rating >= %s AND price BETWEEN %s AND %s", ('%' + search_query + '%', '%' + search_query + '%', rating_filter, price_filter_min, price_filter_max))
        total_books = cur.fetchone()[0]
        if st.session_state.page < (total_books // ITEMS_PER_PAGE):
            st.session_state.page += 1