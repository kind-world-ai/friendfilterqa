from playwright.async_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
    
    async def login(self, email: str, password: str, remember_me: bool = True):
        await self.page.get_by_role("link", name="Log in").click()
        await self.page.get_by_role("textbox", name="Email Email").fill(email)
        await self.page.get_by_role("textbox", name="Password Password").fill(password)
        
        if remember_me:
            await self.page.get_by_role("checkbox", name="Remember me").check()
        
        await self.page.get_by_role("button", name="Log in").click()
        await self.page.get_by_role("button", name="Accept").click()


class AdminDashboard:
    def __init__(self, page: Page):
        self.page = page
    
    async def navigate_to_backend(self):
        await self.page.get_by_text("Backend").click()
    
    async def go_to_users(self):
        await self.page.get_by_role("link", name="Users").click()
        await expect(self.page).to_have_url("**/admin/users")
    
    async def go_to_accounts(self):
        await self.page.get_by_role("link", name="Accounts").click()


class UserManagement:
    def __init__(self, page: Page):
        self.page = page
    
    async def edit_user(self, user_name: str):
        await self.page.get_by_role("row", name=f"*{user_name}*").get_by_role("button").click()
        await self.page.get_by_role("link", name="Edit").click()
    
    async def view_account(self, account_name: str):
        await self.page.get_by_role("row", name=f"*{account_name}*").get_by_role("button").nth(1).click()
        await self.page.get_by_role("link", name="View").click()
        await expect(self.page).to_have_url("**/admin/**")
