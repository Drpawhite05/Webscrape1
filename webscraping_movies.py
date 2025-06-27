import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies.db'
table_name = 'Top_25'
csv_path = '/home/project/top_25_films.csv'
df = pd.DataFrame(columns=["Film", "Year", "Rotten Tomatoes Top 100"])

html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

for row in rows[:25]:
    col = row.find_all('td')
    if len(col) >= 4:
        data_dict = {
            "Film": col[1].get_text(strip=True),
            "Year": col[2].get_text(strip=True),
            "Rotten Tomatoes Top 100": col[3].get_text(strip=True)
        }
        df1 = pd.DataFrame(data_dict, index=[0])
        df = pd.concat([df, df1], ignore_index=True)

# Save full top 25 to CSV and DB
df.to_csv(csv_path, index=False)
conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()

# Filter: Films from the 2000s
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df_2000s = df[(df['Year'] >= 2000) & (df['Year'] <= 2009)]

print("\nFilms released in the 2000s:")
print(df_2000s)
