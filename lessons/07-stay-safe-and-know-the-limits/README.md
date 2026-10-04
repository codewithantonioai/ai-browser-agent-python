# Lesson 7 · Stay safe and know the limits

▶ [Watch this lesson](https://youtu.be/1HuYr6E_nsM?t=990) (starts at 16:30)

## Goal

Lesson seven. Stay safe, and know the limits.

## Commands and files (as shown in the video)

### `browser.py` · code allowed

```python
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

ALLOWED_SITES = {"books.toscrape.com", "localhost"}
MAX_CHARS = 20000


class Browser:
    def __init__(self, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context(
            viewport={"width": 1280, "height": 800},
            record_video_dir="videos",
            record_video_size={"width": 1280, "height": 800},
        )
        self.page = self.context.new_page()
        self.page.set_default_timeout(5000)

    def look(self):
        snapshot = self.page.locator("body").aria_snapshot()
        if len(snapshot) > MAX_CHARS:
            snapshot = snapshot[:MAX_CHARS] + "\n... (page cut here)"
        return f"URL: {self.page.url}\nTitle: {self.page.title()}\n\n{snapshot}"

    def go_to(self, url):
        site = urlparse(url).hostname
        if site not in ALLOWED_SITES:
            return f"Error: {site} is not on the list of allowed sites."
        self.page.goto(url)
        return self.look()

    def click(self, role, name):
        self.page.get_by_role(role, name=name, exact=True).first.click()
        return self.look()

    def type_text(self, label, text):
        self.page.get_by_label(label, exact=True).fill(text)
        return self.look()

    def choose(self, label, option):
        self.page.get_by_label(label, exact=True).select_option(label=option)
        return self.look()

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()
```

### `cheapest.py` · code script

```python
import time

from playwright.sync_api import sync_playwright

MYSTERY = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"

start = time.time()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(MYSTERY)
    books = []
    while True:
        for book in page.locator("article.product_pod").all():
            title = book.locator("h3 a").get_attribute("title")
            price = float(book.locator(".price_color").inner_text()[1:])
            books.append((price, title))
        next_page = page.get_by_role("link", name="next")
        if next_page.count() == 0:
            break
        next_page.click()
    browser.close()

price, title = min(books)
print(f"{title}: £{price}  ({len(books)} books, {time.time() - start:.1f} s)")
```

### Terminal · term script

```bash
uv run cheapest.py
```

## Recap

So: the allow list lives in code, page text is data and never orders, and routine tasks deserve a plain script.
