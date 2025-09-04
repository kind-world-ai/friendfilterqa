import asyncio
from playwright.async_api import async_playwright, expect
from streaming_page_objects import LoginPage, AdminDashboard, UserManagement


class TestStreamingAdminImproved:
    
    def __init__(self):
        self.base_url = "https://acestreamz.com/admin"
        self.credentials = {
            "email": "mike@nightcoders.com",
            "password": "rismoM-rywryp-gisge1"
        }
    
    async def setup_browser(self, headless=False):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        
        # Initialize page objects
        self.login_page = LoginPage(self.page)
        self.dashboard = AdminDashboard(self.page)
        self.user_mgmt = UserManagement(self.page)
    
    async def teardown_browser(self):
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()
    
    async def test_complete_admin_workflow(self):
        await self.setup_browser()
        
        try:
            # Navigate and login
            await self.page.goto(self.base_url)
            await self.login_page.login(
                self.credentials["email"], 
                self.credentials["password"]
            )
            
            # Navigate to backend and users
            await self.dashboard.navigate_to_backend()
            await self.dashboard.go_to_users()
            
            # Edit specific user
            await self.user_mgmt.edit_user("Joy Kumar")
            
            # Navigate to accounts and view details
            await self.dashboard.go_to_accounts()
            await self.user_mgmt.view_account("bitpixel coders")
            
            print("✅ Admin workflow test completed successfully")
            
        except Exception as e:
            await self.page.screenshot(path="test_failure.png")
            print(f"❌ Test failed: {e}")
            raise
        
        finally:
            await self.teardown_browser()


async def main():
    test = TestStreamingAdminImproved()
    await test.test_complete_admin_workflow()


if __name__ == "__main__":
    asyncio.run(main())
