"""
Page Object Models for FriendFilter.com
This file contains reusable page objects for better test organization
"""

from playwright.sync_api import Page, expect
from typing import Optional


class BasePage:
    """Base page object with common functionality"""
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://friendfilter.com"
    
    def navigate_to(self, path: str = ""):
        """Navigate to a specific path on the website"""
        url = f"{self.base_url}{path}" if path else self.base_url
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")
    
    def wait_for_element(self, selector: str, timeout: int = 5000):
        """Wait for an element to be visible"""
        return self.page.wait_for_selector(selector, timeout=timeout)
    
    def take_screenshot(self, name: str):
        """Take a screenshot for debugging"""
        self.page.screenshot(path=f"screenshots/{name}.png")


class LandingPage(BasePage):
    """Page object for the main landing page"""
    
    # Selectors
    CHROME_EXTENSION_BUTTON = 'text="Add to Chrome"'
    MAIN_HEADING = 'h1'
    NAVIGATION_MENU = 'nav'
    CTA_BUTTONS = 'text="Get Started", text="Start Free Trial"'
    FEATURES_SECTION = '.features, #features'
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def load(self):
        """Load the landing page"""
        self.navigate_to()
        return self
    
    def click_chrome_extension_button(self):
        """Click the Chrome extension installation button"""
        button = self.page.locator(self.CHROME_EXTENSION_BUTTON)
        if button.count() > 0:
            with self.page.expect_popup() as popup_info:
                button.click()
            return popup_info.value
        return None
    
    def get_main_heading(self) -> str:
        """Get the main heading text"""
        heading = self.page.locator(self.MAIN_HEADING)
        return heading.text_content() if heading.count() > 0 else ""
    
    def click_cta_button(self):
        """Click the main CTA button"""
        cta = self.page.locator(self.CTA_BUTTONS).first
        if cta.count() > 0:
            cta.click()
    
    def is_loaded(self) -> bool:
        """Check if the page is properly loaded"""
        return self.page.locator("body").is_visible()


class AuthenticationPage(BasePage):
    """Page object for authentication (login/signup)"""
    
    # Selectors
    EMAIL_INPUT = 'input[type="email"], input[name="email"]'
    PASSWORD_INPUT = 'input[type="password"], input[name="password"]'
    CONFIRM_PASSWORD_INPUT = 'input[name="confirm_password"], input[name="password_confirmation"]'
    LOGIN_BUTTON = 'button[type="submit"], input[type="submit"]'
    SIGNUP_LINK = 'text="Sign Up", text="Register"'
    LOGIN_LINK = 'text="Log In", text="Login", text="Sign In"'
    FORGOT_PASSWORD_LINK = 'text="Forgot Password"'
    ERROR_MESSAGE = '.error, .alert-error, [role="alert"]'
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def fill_email(self, email: str):
        """Fill the email field"""
        email_field = self.page.locator(self.EMAIL_INPUT)
        if email_field.count() > 0:
            email_field.fill(email)
    
    def fill_password(self, password: str):
        """Fill the password field"""
        password_field = self.page.locator(self.PASSWORD_INPUT)
        if password_field.count() > 0:
            password_field.fill(password)
    
    def fill_confirm_password(self, password: str):
        """Fill the confirm password field (for signup)"""
        confirm_field = self.page.locator(self.CONFIRM_PASSWORD_INPUT)
        if confirm_field.count() > 0:
            confirm_field.fill(password)
    
    def submit_form(self):
        """Submit the authentication form"""
        submit_button = self.page.locator(self.LOGIN_BUTTON)
        if submit_button.count() > 0:
            submit_button.click()
    
    def click_forgot_password(self):
        """Click the forgot password link"""
        link = self.page.locator(self.FORGOT_PASSWORD_LINK)
        if link.count() > 0:
            link.click()
    
    def get_error_message(self) -> str:
        """Get any error message displayed"""
        error = self.page.locator(self.ERROR_MESSAGE)
        return error.text_content() if error.count() > 0 else ""
    
    def login(self, email: str, password: str):
        """Complete login flow"""
        self.fill_email(email)
        self.fill_password(password)
        self.submit_form()
    
    def signup(self, email: str, password: str, confirm_password: str = None):
        """Complete signup flow"""
        self.fill_email(email)
        self.fill_password(password)
        if confirm_password:
            self.fill_confirm_password(confirm_password)
        self.submit_form()


class PricingPage(BasePage):
    """Page object for the pricing page"""
    
    # Selectors
    PRICING_CARDS = '.pricing-card, .plan-card, [data-testid="pricing-plan"]'
    SELECT_PLAN_BUTTONS = 'text="Select Plan", text="Choose Plan", text="Get Started"'
    FREE_PLAN = 'text="Free", .free-plan'
    PREMIUM_PLAN = 'text="Premium", text="Pro", .premium-plan'
    BILLING_TOGGLE = '.billing-toggle, input[type="checkbox"]'
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def load(self):
        """Load the pricing page"""
        self.navigate_to("/pricing")
        return self
    
    def get_pricing_cards_count(self) -> int:
        """Get the number of pricing plan cards"""
        return self.page.locator(self.PRICING_CARDS).count()
    
    def select_plan(self, plan_index: int = 0):
        """Select a pricing plan by index"""
        select_buttons = self.page.locator(self.SELECT_PLAN_BUTTONS)
        if select_buttons.count() > plan_index:
            select_buttons.nth(plan_index).click()
    
    def toggle_billing_period(self):
        """Toggle between monthly/yearly billing"""
        toggle = self.page.locator(self.BILLING_TOGGLE)
        if toggle.count() > 0:
            toggle.click()


class DashboardPage(BasePage):
    """Page object for the user dashboard"""
    
    # Selectors
    DASHBOARD_CONTAINER = '.dashboard, [data-testid="dashboard"]'
    METRICS_SECTION = '[data-testid="metrics"], .metrics'
    CONNECTIONS_COUNT = '.connections-count, .stats'
    SEARCH_INPUT = 'input[type="search"], input[placeholder*="search"]'
    FILTER_BUTTONS = 'text="Active", text="Archived", text="All"'
    WHITELIST_SECTION = '.whitelist, [data-testid="whitelist"]'
    SETTINGS_BUTTON = 'text="Settings", [data-testid="settings"]'
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def load(self):
        """Load the dashboard page"""
        self.navigate_to("/dashboard")
        return self
    
    def search_connections(self, query: str):
        """Search for connections"""
        search_input = self.page.locator(self.SEARCH_INPUT)
        if search_input.count() > 0:
            search_input.fill(query)
            search_input.press("Enter")
    
    def filter_connections(self, filter_type: str):
        """Filter connections by type (Active, Archived, All)"""
        filter_button = self.page.locator(f'text="{filter_type}"')
        if filter_button.count() > 0:
            filter_button.click()
    
    def get_connections_count(self) -> str:
        """Get the connections count display"""
        count_element = self.page.locator(self.CONNECTIONS_COUNT)
        return count_element.text_content() if count_element.count() > 0 else "0"
    
    def is_loaded(self) -> bool:
        """Check if dashboard is loaded"""
        return self.page.locator(self.DASHBOARD_CONTAINER).is_visible()


class ExtensionPage(BasePage):
    """Page object for Chrome extension related functionality"""
    
    # Selectors
    CHROME_WEB_STORE_LINK = 'a[href*="chrome.google.com/webstore"]'
    DOWNLOAD_BUTTON = 'text="Download", text="Install"'
    PERMISSIONS_INFO = '.permissions, text="Permissions"'
    PRIVACY_INFO = '.privacy, text="Privacy"'
    INSTALLATION_STEPS = '.installation-steps, .setup-guide'
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def click_chrome_store_link(self):
        """Click the Chrome Web Store link"""
        link = self.page.locator(self.CHROME_WEB_STORE_LINK)
        if link.count() > 0:
            with self.page.expect_popup() as popup_info:
                link.click()
            return popup_info.value
        return None
    
    def get_chrome_store_url(self) -> str:
        """Get the Chrome Web Store URL"""
        link = self.page.locator(self.CHROME_WEB_STORE_LINK)
        return link.get_attribute('href') if link.count() > 0 else ""
    
    def check_permissions_displayed(self) -> bool:
        """Check if permissions information is displayed"""
        return self.page.locator(self.PERMISSIONS_INFO).count() > 0
    
    def check_privacy_info_displayed(self) -> bool:
        """Check if privacy information is displayed"""
        return self.page.locator(self.PRIVACY_INFO).count() > 0


# Utility functions for common test operations
def setup_test_browser(playwright, headless=True, browser_type="chromium"):
    """Setup browser for testing"""
    if browser_type == "chromium":
        browser = playwright.chromium.launch(headless=headless)
    elif browser_type == "firefox":
        browser = playwright.firefox.launch(headless=headless)
    elif browser_type == "webkit":
        browser = playwright.webkit.launch(headless=headless)
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    
    page = context.new_page()
    return browser, context, page


def cleanup_browser(browser):
    """Clean up browser resources"""
    if browser:
        browser.close()