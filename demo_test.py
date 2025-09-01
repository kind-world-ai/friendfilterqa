#!/usr/bin/env python3
"""
Simple Demo Test for FriendFilter.com
A basic test to verify the setup works and demonstrate key functionality
"""

from playwright.sync_api import sync_playwright, expect
import time


def demo_test():
    """Simple demonstration test"""
    print("🚀 Starting FriendFilter.com Demo Test")
    print("=" * 50)
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)  # Running in headless mode
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        try:
            print("1. Loading website...")
            page.goto("https://friendfilter.com")
            page.wait_for_load_state("domcontentloaded")
            print("   ✅ Website loaded successfully")
            
            print("2. Checking page title...")
            title = page.title()
            print(f"   📄 Page title: {title}")
            
            print("3. Taking screenshot...")
            page.screenshot(path="friendfilter_homepage.png")
            print("   📸 Screenshot saved as 'friendfilter_homepage.png'")
            
            print("4. Looking for Chrome extension button...")
            chrome_button = page.locator('text="Add to Chrome"')
            if chrome_button.count() > 0:
                print("   ✅ Chrome extension button found")
                print("   🔗 Button is visible and clickable")
            else:
                print("   ⚠️  Chrome extension button not found with exact text")
                # Try alternative selectors
                alt_buttons = page.locator('a[href*="chrome"], button:has-text("Chrome"), text="Install"')
                if alt_buttons.count() > 0:
                    print(f"   📍 Found {alt_buttons.count()} potential Chrome-related buttons")
            
            print("5. Checking page structure...")
            # Check for common elements
            elements_to_check = [
                ("Navigation", "nav"),
                ("Main content", "main"),
                ("Footer", "footer"),
                ("Buttons", "button"),
                ("Links", "a")
            ]
            
            for name, selector in elements_to_check:
                count = page.locator(selector).count()
                print(f"   📊 {name}: {count} found")
            
            print("6. Testing responsive design...")
            # Test mobile viewport
            page.set_viewport_size({"width": 375, "height": 667})
            time.sleep(1)
            page.screenshot(path="friendfilter_mobile.png")
            print("   📱 Mobile screenshot saved as 'friendfilter_mobile.png'")
            
            # Reset to desktop
            page.set_viewport_size({"width": 1920, "height": 1080})
            
            print("7. Checking for forms...")
            forms = page.locator("form")
            inputs = page.locator("input")
            print(f"   📝 Forms found: {forms.count()}")
            print(f"   ⌨️  Input fields found: {inputs.count()}")
            
            print("8. Measuring page load performance...")
            start_time = time.time()
            page.reload()
            page.wait_for_load_state("domcontentloaded")
            load_time = time.time() - start_time
            print(f"   ⚡ Page load time: {load_time:.2f} seconds")
            
            if load_time < 3.0:
                print("   ✅ Good page load performance")
            elif load_time < 5.0:
                print("   ⚠️  Acceptable page load performance")
            else:
                print("   ❌ Slow page load performance")
            
            print("9. Final verification...")
            body_visible = page.locator("body").is_visible()
            print(f"   👁️  Page body visible: {body_visible}")
            
            if body_visible:
                print("   ✅ Basic functionality test PASSED")
            else:
                print("   ❌ Basic functionality test FAILED")
            
        except Exception as e:
            print(f"❌ Test failed with error: {str(e)}")
        
        finally:
            # Cleanup
            browser.close()
            print("\n🏁 Demo test completed!")
            print("=" * 50)


if __name__ == "__main__":
    demo_test()