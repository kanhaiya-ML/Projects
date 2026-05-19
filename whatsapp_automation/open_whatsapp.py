from playwright.sync_api import sync_playwright
import asyncio

def send_whatsapp_message(contact_name,message):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            headless=False,
            # channel="chrome",
            user_data_dir="./firefox_profile",
            # args=["--start-minimized"]
        )

        page = browser.new_page()
        page.goto("https://web.whatsapp.com")
        
        # Wait for chats to load
        page.wait_for_timeout(3000)
        print("WhatsApp opened!")
        page.locator("input[aria-label='Search or start a new chat']").fill(contact_name)
        page.wait_for_timeout(1000)
        page.locator(f"[data-testid='list-item-1']").click()
        page.wait_for_timeout(1000)
        page.locator(f"div[data-testid='conversation-compose-box-input']").fill(message)
        page.locator("button[aria-label='Send']").click()

        page.wait_for_timeout(30000)
        
        browser.close()
        return f"Message sent to {contact_name} successfully ✅"