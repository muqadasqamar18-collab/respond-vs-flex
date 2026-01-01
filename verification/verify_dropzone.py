from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:5000")

        # Focus on the drop zone
        drop_zone = page.locator("#drop-zone")
        drop_zone.focus()

        # Take a screenshot of the focused state
        page.screenshot(path="verification/dropzone_focus.png")
        print("Screenshot saved to verification/dropzone_focus.png")
        browser.close()

if __name__ == "__main__":
    run()
