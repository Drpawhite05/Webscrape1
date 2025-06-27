import requests
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup

# ---------- CONFIGURATION ----------
URL = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
CSV_PATH = '/home/project/top_25_films.csv'
DB_NAME = 'Movies.db'
TABLE_NAME = 'Top_25'

# ---------- SCRAPE HTML ----------
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

# Locate the first table body
table = soup.find('table')
rows = table.find_all('tr')

# ---------- EXTRACT DATA ----------
movies = []
for row in rows[1:26]:  # Skip header, limit to top 25
    cols = row.find_all('td')
    if len(cols) >= 4:
        film = cols[1].get_text(strip=True)
        year = cols[2].get_text(strip=True)
        rt_rank = cols[3].get_text(strip=True)
        movies.append({"Film": film, "Year": year, "Rotten Tomatoes Top 100": rt_rank})

# Create DataFrame
df = pd.DataFrame(movies)

# ---------- SAVE TO CSV ----------
df.to_csv(CSV_PATH, index=False)
print(f"✅ Data saved to: {CSV_PATH}")

# ---------- SAVE TO DATABASE ----------
conn = sqlite3.connect(DB_NAME)
df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
conn.close()
print(f"✅ Data saved to SQLite DB: {DB_NAME} (table: {TABLE_NAME})")

# ---------- FILTER AND PRINT 2000s MOVIES ----------
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')  # Convert year to numeric
df_2000s = df[(df['Year'] >= 2000) & (df['Year'] <= 2009)]

print("\n🎬 Films Released in the 2000s:")
print(df_2000s)
