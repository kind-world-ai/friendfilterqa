import asyncio
import pytest
from playwright.async_api import async_playwright, expect


class TestStreamingAdmin:
    
    async def setup_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
    
    async def teardown_browser(self):
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()
    
    async def test_admin_login_and_user_management(self):
        await self.setup_browser()
        
        try:
            # Navigate to admin panel
            await self.page.goto("https://acestreamz.com/admin")
            
            # Click login link
            await self.page.get_by_role("link", name="Log in").click()
            
            # Login with credentials
            await self.page.get_by_role("textbox", name="Email Email").fill("mike@nightcoders.com")
            await self.page.get_by_role("textbox", name="Password Password").fill("rismoM-rywryp-gisge1")
            await self.page.get_by_role("checkbox", name="Remember me").check()
            await self.page.get_by_role("button", name="Log in").click()
            
            # Accept terms/cookies
            await self.page.get_by_role("button", name="Accept").click()
            
            # Navigate to Backend
            await self.page.get_by_text("Backend").click()
            
            # Go to Users section
            await self.page.get_by_role("link", name="Users").click()
            
            # Verify users page loaded
            await expect(self.page).to_have_url("**/users")
            
            # Edit user (Joy Kumar)
            await self.page.get_by_role("row", name="62 Badge Joy Kumar Blocked").get_by_role("button").click()
            await self.page.get_by_role("link", name="Edit").click()
            
            # Navigate to Accounts
            await self.page.get_by_role("link", name="Accounts").click()
            
            # View account details
            await self.page.get_by_role("row", name="5 Badge bitpixel coders 16.00").get_by_role("button").nth(1).click()
            await self.page.get_by_role("link", name="View").click()
            
            # Verify account view loaded
            await expect(self.page).to_have_url("**/view")
            
        finally:
            await self.teardown_browser()


async def main():
    test = TestStreamingAdmin()
    await test.test_admin_login_and_user_management()


if __name__ == "__main__":
    asyncio.run(main())
