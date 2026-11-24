import requests
import time
import csv
from bs4 import BeautifulSoup

# 把名言變成一個list
def parse_quotes(soup):
    results = []
    for q in soup.select("div.quote"):
        results.append({
            "text": q.select_one("span.text").get_text(), 
            "author": q.select_one("small.author").get_text(),
            "tags": [tag.get_text() for tag in q.select("a.tag")]
        })
    return results


BASE = "https://quotes.toscrape.com"
url = BASE + "/"
all_quotes = []

while True:
    try:
        r = requests.get(url)
        r.raise_for_status() 
    except requests.RequestException as e:
        print(f"抓取失敗: {e}")
        continue

    soup = BeautifulSoup(r.text, "html.parser")
    all_quotes.extend(parse_quotes(soup))
    print(f"已抓取 {len(all_quotes)} 則")

    next_btn = soup.select_one("li.next a")
    if next_btn is None:
        break
    url = BASE + next_btn["href"]
    time.sleep(1)  

with open("quote.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
    writer.writeheader()
    writer.writerows(all_quotes)

print(f"完成！{len(all_quotes)} 則！")
