from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://books.toscrape.com")
    html = page.content()
    snapshot = page.locator("body").aria_snapshot()
    print(snapshot[:1200])
    print(f"\nHTML:     {len(html):,} characters")
    print(f"Snapshot: {len(snapshot):,} characters")
    browser.close()
