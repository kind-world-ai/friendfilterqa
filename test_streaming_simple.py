import asyncio
from playwright.async_api import async_playwright


async def test_streaming_admin():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("🚀 Starting streaming admin test...")
            
            # Navigate to admin panel
            await page.goto("https://acestreamz.com/admin")
            print("✅ Navigated to admin panel")
            
            # Login
            await page.get_by_role("link", name="Log in").click()
            await page.get_by_role("textbox", name="Email Email").fill("mike@nightcoders.com")
            await page.get_by_role("textbox", name="Password Password").fill("rismoM-rywryp-gisge1")
            await page.get_by_role("checkbox", name="Remember me").check()
            await page.get_by_role("button", name="Log in").click()
            print("✅ Login completed")
            
            # Accept terms
            await page.get_by_role("button", name="Accept").click()
            print("✅ Terms accepted")
            
            # Navigate to Backend
            await page.get_by_text("Backend").click()
            print("✅ Navigated to Backend")
            
            # Go to Users
            await page.get_by_role("link", name="Users").click()
            print("✅ Navigated to Users section")
            
            # Edit user
            await page.get_by_role("row", name="62 Badge Joy Kumar Blocked").get_by_role("button").click()
            await page.get_by_role("link", name="Edit").click()
            print("✅ User edit initiated")
            
            # Go to Accounts
            await page.get_by_role("link", name="Accounts").click()
            print("✅ Navigated to Accounts")
            
            # View account
            await page.get_by_role("row", name="5 Badge bitpixel coders 16.00").get_by_role("button").nth(1).click()
            await page.get_by_role("link", name="View").click()
            print("✅ Account view opened")
            
            print("🎉 Test completed successfully!")
            
        except Exception as e:
            await page.screenshot(path="test_failure.png")
            print(f"❌ Test failed: {e}")
            raise
        
        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    asyncio.run(test_streaming_admin())
