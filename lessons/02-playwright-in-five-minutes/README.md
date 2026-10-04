# Lesson 2 · Playwright in five minutes

▶ [Watch this lesson](https://youtu.be/1HuYr6E_nsM?t=169) (starts at 2:49)

## Goal

Lesson two. Playwright in five minutes.

## Commands and files (as shown in the video)

### Terminal · term init add

```bash
uv init --no-package webpilot
cd webpilot
uv add playwright openai
```

### Terminal · term install

```bash
uv run playwright install chromium
```

### `first.py` · code first

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://books.toscrape.com")
    print(page.title())
    page.screenshot(path="first.png")
    browser.close()
```

### Terminal · term first

```bash
uv run first.py
ls
```

## Recap

So far: a project with Playwright and OpenAI, a real Chromium, and a script that reads a page and takes a picture. Now, what should the model see?
