from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://news.ycombinator.com/")
    titles = page.query_selector_all('a')[:10]
    print(titles)
    for title in titles:
        print(title.text_content())
    browser.close()

with sync_playwright() as playwright:
    run(playwright)