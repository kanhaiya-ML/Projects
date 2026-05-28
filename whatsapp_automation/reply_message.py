from playwright.sync_api import sync_playwright
from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def reply_new_message():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            channel="chrome",
            headless=False,
            user_data_dir="./chrome_profile"
        )
        page = browser.new_page()
        page.goto("https://web.whatsapp.com")
        while True:
            unread_chats = page.locator("span[data-testid='icon-unread-count']").all()
            last_sent_message = set()

            for chat in unread_chats:
                chat.locator("..").click()
                page.wait_for_timeout(1000)
                message = page.locator("span[data-testid='selectable-text']").last.text_content()

                if message in last_sent_message:
                    continue

                reply = llm.invoke(f"""You are a friendly person chatting on Whatsapp.
                                   Reply naturally in the same language as the message - English or Hinglish.
                                   Keep reply short like a real whatsapp message.
                                   Message: {message}""")
                reply = reply.content
                last_sent_message.add(reply)
                page.locator(f"div[data-testid='conversation-compose-box-input']").fill(reply)
                page.locator("button[aria-label='Send']").click()
                page.wait_for_timeout(10000)
reply_new_message()