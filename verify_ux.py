import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Start the local server
        process = await asyncio.create_subprocess_shell('python api/index.py > /dev/null 2>&1', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await asyncio.sleep(5) # Give it time to start

        try:
            await page.goto("http://127.0.0.1:5000")

            # 1. Check Drop Zone Accessibility
            drop_zone = page.locator("#drop-zone")

            # Check tabindex
            tabindex = await drop_zone.get_attribute("tabindex")
            print(f"Drop Zone tabindex: {tabindex}") # Expected: None or 0

            # Check role
            role = await drop_zone.get_attribute("role")
            print(f"Drop Zone role: {role}") # Expected: button

            # Check aria-label
            aria_label = await drop_zone.get_attribute("aria-label")
            print(f"Drop Zone aria-label: {aria_label}")

            # 2. Check Delete Button Accessibility (simulate file add first?)
            # Since we can't easily drag and drop in this headless env without more setup,
            # we will inspect the JS logic for creating the button via static analysis or just assume it based on code reading.
            # But let's try to verify the drop zone focus at least.

            await drop_zone.focus()
            is_focused = await drop_zone.evaluate("document.activeElement === document.getElementById('drop-zone')")
            print(f"Drop Zone can receive focus: {is_focused}")

        finally:
            process.terminate()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
