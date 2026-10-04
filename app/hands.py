from browser import Browser

browser = Browser()
page = browser.go_to("https://books.toscrape.com")
print(page[:200], "\n")
page = browser.click("link", "Poetry")
print(page[:200])
browser.close()
