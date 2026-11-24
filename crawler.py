import requests
import time
import csv
from bs4 import BeautifulSoup

# 把名言變成一個list
def parse_quotes(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    # selected = soup.select("div.quote")
    # print(selected)
    for q in soup.select("div.quote"):
        results.append({
            "text": q.select_one("span.text").get_text(), 
            "author": q.select_one("small.author").get_text(),
            "tags": [tag.get_text() for tag in q.select("a.tag")]
        })
    return results

# url = "https://quotes.toscrape.com/"
# r = requests.get(url)

# print(r.status_code)
# print(r.encoding)
# print(r.text[:500])

# quotes = parse_quotes(r.text)
# print(len(quotes))
# print(quotes[0])

all_quotes = []
for page in range(1, 4):
    url = f"https://quotes.toscrape.com/page/{page}/"
    try:
        r = requests.get(url)
        r.raise_for_status()  # 如果狀態碼不是200，會丟出例外
    except requests.RequestException as e:
        print(f"第 {page} 頁失敗: {e}")
        continue
    all_quotes.extend(parse_quotes(r.text)) 
    # extend() 方法用於將一個可迭代對象（如列表、元組、集合等）中的元素逐一添加到另一個列表的末尾。與 append() 方法不同，append() 是將整個對象作為單一元素添加，而 extend() 則是將可迭代對象中的每個元素分別添加。
    time.sleep(1)  # 暫停1秒，避免對伺服器造成過大負擔

# print(len(all_quotes))
with open("quote.csv", "w", newline="", encoding="utf-8-sig") as f:
    # sig 讓 Excel 可以正確顯示中文，不會出現亂碼
    writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
    writer.writeheader()
    writer.writerows(all_quotes)

print(f"完成！{len(all_quotes)} 則！")
# 就可以直接在此路徑：/Users/kellylee/Downloads，找到新增的csv檔案，並且可以用Excel開啟，裡面有三個欄位：text、author、tags
