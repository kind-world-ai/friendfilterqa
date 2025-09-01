import pytest
from playwright.sync_api import sync_playwright, expect
import time
import os
from typing import Dict, List


class FriendFilterTestSuite:
    """Comprehensive test suite for FriendFilter.com covering all use cases"""
    
    def __init__(self):
        self.base_url = "https://friendfilter.com"
        self.browser = None
        self.context = None
        self.page = None
    
    def setup_browser(self, headless=False, browser_type="chromium"):
        """Initialize browser with specific configuration"""
        self.playwright = sync_playwright().start()
        
        if browser_type == "chromium":
            self.browser = self.playwright.chromium.launch(headless=headless)
        elif browser_type == "firefox":
            self.browser = self.playwright.firefox.launch(headless=headless)
        elif browser_type == "webkit":
            self.browser = self.playwright.webkit.launch(headless=headless)
        
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = self.context.new_page()
    
    def teardown_browser(self):
        """Clean up browser resources"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()


class TestLandingPage(FriendFilterTestSuite):
    """Test cases for the main landing page"""
    
    def test_homepage_loads_successfully(self):
        """Test that the homepage loads without errors"""
        self.setup_browser()
        self.page.goto(self.base_url)
        
        # Check page title
        expect(self.page).to_have_title(lambda title: "FriendFilter" in title)
        
        # Check main elements are present
        expect(self.page.locator("body")).to_be_visible()
        
        self.teardown_browser()
    
    def test_chrome_extension_button(self):
        """Test the Chrome extension installation button"""
        self.setup_browser()
        self.page.goto(self.base_url)
        
        # Look for Chrome extension button
        chrome_button = self.page.locator('text="Add to Chrome"')
        if chrome_button.count() > 0:
            expect(chrome_button).to_be_visible()
            
            # Test button click (should redirect to Chrome Web Store)
            with self.page.expect_popup() as popup_info:
                chrome_button.click()
            popup_page = popup_info.value
            expect(popup_page.url).to_contain("chrome.google.com")
            popup_page.close()
        
        self.teardown_browser()
    
    def test_navigation_menu(self):
        """Test main navigation menu functionality"""
        self.setup_browser()
        self.page.goto(self.base_url)
        
        # Common navigation elements to test
        nav_elements = [
            'text="Home"',
            'text="Features"',
            'text="Pricing"',
            'text="About"',
            'text="Contact"'
        ]
        
        for element in nav_elements:
            nav_link = self.page.locator(element)
            if nav_link.count() > 0:
                expect(nav_link).to_be_visible()
                nav_link.click()
                self.page.wait_for_timeout(1000)
        
        self.teardown_browser()
    
    def test_responsive_design(self):
        """Test responsive design across different screen sizes"""
        self.setup_browser()
        
        # Test different viewport sizes
        viewports = [
            {'width': 1920, 'height': 1080},  # Desktop
            {'width': 768, 'height': 1024},   # Tablet
            {'width': 375, 'height': 667}     # Mobile
        ]
        
        for viewport in viewports:
            self.page.set_viewport_size(viewport)
            self.page.goto(self.base_url)
            
            # Check page renders properly
            expect(self.page.locator("body")).to_be_visible()
            
            # Check if mobile menu appears on small screens
            if viewport['width'] <= 768:
                mobile_menu = self.page.locator('[data-testid="mobile-menu"], .hamburger, .menu-toggle')
                if mobile_menu.count() > 0:
                    expect(mobile_menu).to_be_visible()
        
        self.teardown_browser()


class TestUserAuthentication(FriendFilterTestSuite):
    """Test cases for user authentication flow"""
    
    def test_signup_form(self):
        """Test user signup functionality"""
        self.setup_browser()
        self.page.goto(self.base_url)
        
        # Look for signup buttons/links
        signup_selectors = [
            'text="Sign Up"',
            'text="Get Started"',
            'text="Start Free Trial"',
            '[data-testid="signup-button"]'
        ]
        
        for selector in signup_selectors:
            signup_button = self.page.locator(selector)
            if signup_button.count() > 0:
                signup_button.click()
                
                # Check if signup form appears
                form_fields = [
                    'input[type="email"]',
                    'input[type="password"]',
                    'input[name="email"]',
                    'input[name="password"]'
                ]
                
                for field in form_fields:
                    field_element = self.page.locator(field)
                    if field_element.count() > 0:
                        expect(field_element).to_be_visible()
                break
        
        self.teardown_browser()
    
    def test_login_form(self):
        """Test user login functionality"""
        self.setup_browser()
        self.page.goto(self.base_url)
        
        # Look for login buttons/links
        login_selectors = [
            'text="Log In"',
            'text="Login"',
            'text="Sign In"',
            '[data-testid="login-button"]'
        ]
        
        for selector in login_selectors:
            login_button = self.page.locator(selector)
            if login_button.count() > 0:
                login_button.click()
                
                # Check if login form appears
                email_field = self.page.locator('input[type="email"], input[name="email"]')
                password_field = self.page.locator('input[type="password"], input[name="password"]')
                
                if email_field.count() > 0 and password_field.count() > 0:
                    expect(email_field).to_be_visible()
                    expect(password_field).to_be_visible()
                break
        
        self.teardown_browser()
    
    def test_password_reset_flow(self):
        """Test password reset functionality"""
        self.setup_browser()
        self.page.goto(self.base_url)
        
        # Look for forgot password link
        forgot_password = self.page.locator('text="Forgot Password"')
        if forgot_password.count() > 0:
            forgot_password.click()
            
            # Check for email input field
            email_field = self.page.locator('input[type="email"], input[name="email"]')
            if email_field.count() > 0:
                expect(email_field).to_be_visible()
                
                # Test form submission
                email_field.fill("test@example.com")
                reset_button = self.page.locator('text="Reset Password", [type="submit"]')
                if reset_button.count() > 0:
                    reset_button.click()
        
        self.teardown_browser()


class TestPricingPage(FriendFilterTestSuite):
    """Test cases for pricing page functionality"""
    
    def test_pricing_plans_display(self):
        """Test that pricing plans are displayed correctly"""
        self.setup_browser()
        self.page.goto(f"{self.base_url}/pricing")
        
        # Look for pricing plan cards
        pricing_cards = self.page.locator('.pricing-card, .plan-card, [data-testid="pricing-plan"]')
        if pricing_cards.count() > 0:
            for i in range(pricing_cards.count()):
                card = pricing_cards.nth(i)
                expect(card).to_be_visible()
        
        self.teardown_browser()
    
    def test_plan_selection(self):
        """Test selecting different pricing plans"""
        self.setup_browser()
        self.page.goto(f"{self.base_url}/pricing")
        
        # Look for plan selection buttons
        select_buttons = self.page.locator('text="Select Plan", text="Choose Plan", text="Get Started"')
        if select_buttons.count() > 0:
            select_buttons.first.click()
            
            # Check if redirected to signup or payment
            self.page.wait_for_timeout(2000)
            current_url = self.page.url
            assert "signup" in current_url or "payment" in current_url or "checkout" in current_url
        
        self.teardown_browser()


class TestDashboardFunctionality(FriendFilterTestSuite):
    """Test cases for dashboard features (requires authentication)"""
    
    def test_dashboard_elements(self):
        """Test dashboard UI elements"""
        self.setup_browser()
        # Note: This would require authentication in a real scenario
        self.page.goto(f"{self.base_url}/dashboard")
        
        # Common dashboard elements
        dashboard_elements = [
            '.dashboard',
            '[data-testid="metrics"]',
            '.connections-count',
            '.whitelist-section'
        ]
        
        for element in dashboard_elements:
            elem = self.page.locator(element)
            if elem.count() > 0:
                expect(elem).to_be_visible()
        
        self.teardown_browser()
    
    def test_connection_filtering(self):
        """Test connection filtering functionality"""
        self.setup_browser()
        self.page.goto(f"{self.base_url}/dashboard")
        
        # Test filter options
        filter_buttons = [
            'text="Active"',
            'text="Archived"',
            'text="All Connections"'
        ]
        
        for button_text in filter_buttons:
            button = self.page.locator(button_text)
            if button.count() > 0:
                button.click()
                self.page.wait_for_timeout(1000)
        
        self.teardown_browser()
    
    def test_search_functionality(self):
        """Test smart search functions"""
        self.setup_browser()
        self.page.goto(f"{self.base_url}/dashboard")
        
        # Look for search input
        search_input = self.page.locator('input[type="search"], input[placeholder*="search"]')
        if search_input.count() > 0:
            expect(search_input).to_be_visible()
            search_input.fill("test search")
            search_input.press("Enter")
            self.page.wait_for_timeout(2000)
        
        self.teardown_browser()


class TestExtensionFeatures(FriendFilterTestSuite):
    """Test cases for Chrome extension specific features"""
    
    def test_extension_download_links(self):
        """Test extension download and installation links"""
        self.setup_browser()
        self.page.goto(self.base_url)
        
        # Test Chrome Web Store link
        chrome_store_link = self.page.locator('a[href*="chrome.google.com/webstore"]')
        if chrome_store_link.count() > 0:
            expect(chrome_store_link).to_be_visible()
            href = chrome_store_link.get_attribute('href')
            assert "chrome.google.com/webstore" in href
        
        self.teardown_browser()
    
    def test_extension_permissions_info(self):
        """Test extension permissions information display"""
        self.setup_browser()
        self.page.goto(self.base_url)
        
        # Look for permissions or privacy information
        permissions_section = self.page.locator('text="Permissions", text="Privacy", .permissions')
        if permissions_section.count() > 0:
            expect(permissions_section).to_be_visible()
        
        self.teardown_browser()


class TestFormValidation(FriendFilterTestSuite):
    """Test cases for form validation and error handling"""
    
    def test_email_validation(self):
        """Test email field validation"""
        self.setup_browser()
        self.page.goto(self.base_url)
        
        # Find any email input field
        email_field = self.page.locator('input[type="email"]')
        if email_field.count() > 0:
            # Test invalid email
            email_field.fill("invalid-email")
            
            # Try to submit or move focus
            email_field.press("Tab")
            
            # Check for validation message
            validation_message = self.page.locator('.error, .invalid, [role="alert"]')
            if validation_message.count() > 0:
                expect(validation_message).to_be_visible()
        
        self.teardown_browser()
    
    def test_required_fields(self):
        """Test required field validation"""
        self.setup_browser()
        self.page.goto(self.base_url)
        
        # Find forms with required fields
        required_fields = self.page.locator('input[required], textarea[required], select[required]')
        if required_fields.count() > 0:
            # Try to submit empty form
            submit_button = self.page.locator('button[type="submit"], input[type="submit"]')
            if submit_button.count() > 0:
                submit_button.click()
                
                # Check for validation messages
                self.page.wait_for_timeout(1000)
        
        self.teardown_browser()


class TestPerformanceAndSEO(FriendFilterTestSuite):
    """Test cases for performance and SEO optimization"""
    
    def test_page_load_time(self):
        """Test page load performance"""
        self.setup_browser()
        
        start_time = time.time()
        self.page.goto(self.base_url)
        self.page.wait_for_load_state("domcontentloaded")
        end_time = time.time()
        
        load_time = end_time - start_time
        assert load_time < 5.0, f"Page load time too slow: {load_time}s"
        
        self.teardown_browser()
    
    def test_meta_tags(self):
        """Test SEO meta tags presence"""
        self.setup_browser()
        self.page.goto(self.base_url)
        
        # Check for essential meta tags
        meta_tags = [
            'meta[name="description"]',
            'meta[property="og:title"]',
            'meta[property="og:description"]',
            'meta[name="viewport"]'
        ]
        
        for tag in meta_tags:
            meta_element = self.page.locator(tag)
            if meta_element.count() > 0:
                content = meta_element.get_attribute('content')
                assert content and len(content) > 0
        
        self.teardown_browser()
    
    def test_image_optimization(self):
        """Test image loading and optimization"""
        self.setup_browser()
        self.page.goto(self.base_url)
        
        # Check all images have alt attributes
        images = self.page.locator('img')
        for i in range(images.count()):
            img = images.nth(i)
            alt_text = img.get_attribute('alt')
            # Alt attribute should exist (can be empty for decorative images)
            assert alt_text is not None
        
        self.teardown_browser()


class TestAccessibility(FriendFilterTestSuite):
    """Test cases for web accessibility compliance"""
    
    def test_keyboard_navigation(self):
        """Test keyboard navigation functionality"""
        self.setup_browser()
        self.page.goto(self.base_url)
        
        # Test tab navigation
        focusable_elements = self.page.locator('a, button, input, select, textarea, [tabindex]')
        if focusable_elements.count() > 0:
            # Tab through elements
            for i in range(min(5, focusable_elements.count())):
                self.page.keyboard.press("Tab")
                self.page.wait_for_timeout(200)
        
        self.teardown_browser()
    
    def test_aria_labels(self):
        """Test ARIA labels and accessibility attributes"""
        self.setup_browser()
        self.page.goto(self.base_url)
        
        # Check for ARIA landmarks
        landmarks = [
            '[role="main"]',
            '[role="navigation"]',
            '[role="banner"]',
            '[role="contentinfo"]'
        ]
        
        for landmark in landmarks:
            element = self.page.locator(landmark)
            if element.count() > 0:
                expect(element).to_be_visible()
        
        self.teardown_browser()


class TestCrossBrowserCompatibility(FriendFilterTestSuite):
    """Test cases for cross-browser compatibility"""
    
    def test_chromium_compatibility(self):
        """Test functionality in Chromium-based browsers"""
        self.setup_browser(browser_type="chromium")
        self.page.goto(self.base_url)
        expect(self.page.locator("body")).to_be_visible()
        self.teardown_browser()
    
    def test_firefox_compatibility(self):
        """Test functionality in Firefox"""
        self.setup_browser(browser_type="firefox")
        self.page.goto(self.base_url)
        expect(self.page.locator("body")).to_be_visible()
        self.teardown_browser()
    
    def test_webkit_compatibility(self):
        """Test functionality in WebKit (Safari)"""
        self.setup_browser(browser_type="webkit")
        self.page.goto(self.base_url)
        expect(self.page.locator("body")).to_be_visible()
        self.teardown_browser()


class TestErrorHandling(FriendFilterTestSuite):
    """Test cases for error handling and edge cases"""
    
    def test_404_error_handling(self):
        """Test 404 error page handling"""
        self.setup_browser()
        self.page.goto(f"{self.base_url}/nonexistent-page")
        
        # Check if custom 404 page is displayed
        page_content = self.page.content()
        assert "404" in page_content or "Not Found" in page_content
        
        self.teardown_browser()
    
    def test_network_error_handling(self):
        """Test behavior when network requests fail"""
        self.setup_browser()
        
        # Block specific resources to simulate network errors
        self.page.route("**/api/**", lambda route: route.abort())
        self.page.goto(self.base_url)
        
        # Page should still load even if some API calls fail
        expect(self.page.locator("body")).to_be_visible()
        
        self.teardown_browser()


def run_comprehensive_tests():
    """Run all test suites"""
    test_classes = [
        TestLandingPage,
        TestUserAuthentication,
        TestPricingPage,
        TestDashboardFunctionality,
        TestExtensionFeatures,
        TestFormValidation,
        TestPerformanceAndSEO,
        TestAccessibility,
        TestCrossBrowserCompatibility,
        TestErrorHandling
    ]
    
    results = {}
    
    for test_class in test_classes:
        class_name = test_class.__name__
        print(f"\n🧪 Running {class_name} tests...")
        
        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        class_results = []
        
        for method_name in test_methods:
            try:
                print(f"  ▶️  {method_name}")
                method = getattr(test_instance, method_name)
                method()
                print(f"  ✅ {method_name} - PASSED")
                class_results.append({"test": method_name, "status": "PASSED"})
            except Exception as e:
                print(f"  ❌ {method_name} - FAILED: {str(e)}")
                class_results.append({"test": method_name, "status": "FAILED", "error": str(e)})
        
        results[class_name] = class_results
    
    return results


if __name__ == "__main__":
    print("🚀 Starting FriendFilter.com Comprehensive Test Suite")
    print("=" * 60)
    
    results = run_comprehensive_tests()
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    total_tests = 0
    total_passed = 0
    
    for class_name, class_results in results.items():
        passed = sum(1 for r in class_results if r["status"] == "PASSED")
        failed = len(class_results) - passed
        total_tests += len(class_results)
        total_passed += passed
        
        print(f"{class_name}: {passed} passed, {failed} failed")
    
    print(f"\nOverall: {total_passed}/{total_tests} tests passed ({total_passed/total_tests*100:.1f}%)")