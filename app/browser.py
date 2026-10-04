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
