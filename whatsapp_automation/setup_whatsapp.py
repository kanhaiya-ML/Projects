from playwright.async_api import async_playwright
import asyncio

async def setup_whatsapp():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            headless=False,
            # channel="chrome",
            user_data_dir="./firefox_profile"
        )
        # context = await browser.new_context()  # no storage_state here
        page = await browser.new_page()

        await page.goto("https://web.whatsapp.com")
        
        print("Scan QR code — 30 seconds...")
        await page.wait_for_timeout(30000)
        
        # await context.storage_state(path="whatsapp_session.json")
        # print("Session saved!")
        
        await browser.close()

asyncio.run(setup_whatsapp())
