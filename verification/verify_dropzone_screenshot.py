
import asyncio
from playwright.async_api import async_playwright, expect

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://localhost:5000")

        # Verify drop zone attributes
        drop_zone = page.locator("#drop-zone")
        await expect(drop_zone).to_have_attribute("tabindex", "0")
        await expect(drop_zone).to_have_attribute("role", "button")
        await expect(drop_zone).to_have_attribute("aria-label", "Upload files")

        # Focus the drop zone
        await drop_zone.focus()

        # Take a screenshot of the focused drop zone to verify focus ring
        await page.screenshot(path="verification/dropzone_focused.png")
        print("Screenshot saved to verification/dropzone_focused.png")

        # Optional: Test keydown functionality if we can verify the file chooser opens.
        # This is tricky in headless mode without actually uploading files, but we can try
        # to trigger it and expect the file chooser event.

        async with page.expect_file_chooser() as fc_info:
            await page.keyboard.press("Enter")

        file_chooser = await fc_info.value
        print(f"File chooser triggered: {file_chooser}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
