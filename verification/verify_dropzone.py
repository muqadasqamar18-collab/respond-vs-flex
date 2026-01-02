
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://localhost:5000")

        # Check if drop zone has tabindex
        drop_zone_tabindex = await page.evaluate("document.getElementById('drop-zone').getAttribute('tabindex')")
        print(f"Drop zone tabindex: {drop_zone_tabindex}")

        # Check if we can focus it by tabbing (this is a bit harder to assert directly without more complex logic,
        # but checking the attribute is a good proxy for intent).

        # We can also check active element
        await page.keyboard.press("Tab")
        # Assuming the first tab goes somewhere, let's see where.

        active_element_id = await page.evaluate("document.activeElement.id")
        print(f"Active element after 1 Tab: {active_element_id}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
