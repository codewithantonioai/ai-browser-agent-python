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
