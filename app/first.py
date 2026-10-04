from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://books.toscrape.com")
    print(page.title())
    page.screenshot(path="first.png")
    browser.close()
