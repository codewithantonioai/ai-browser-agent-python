# Lesson 3 · The agent's eyes

▶ [Watch this lesson](https://youtu.be/1HuYr6E_nsM?t=326) (starts at 5:26)

## Goal

Lesson three. The agent's eyes.

## Commands and files (as shown in the video)

### `look.py` · code look

```python
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
```

## Recap

So: the model reads an aria snapshot, not HTML. It's three times smaller. And roles and names connect what the model sees to what Playwright clicks. Time to give it hands.
