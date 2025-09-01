#!/usr/bin/env python3
"""
Visual Playwright Demo - Browser in Action
This demo runs with the browser visible so you can see Playwright working
"""

from playwright.sync_api import sync_playwright
import time

def visual_demo():
    """Run a visual demonstration with browser window open"""
    
    print("🎬 Visual Playwright Demo - Browser Window Will Open!")
    print("=" * 60)
    print("Watch the browser window to see Playwright in action...")
    print("The test will run slowly so you can see each step.")
    print()
    
    with sync_playwright() as p:
        # Launch browser with visible window (headless=False)
        print("🚀 Launching browser window...")
        browser = p.chromium.launch(
            headless=False,  # Show the browser window
            slow_mo=2000,    # Add 2 second delay between actions
            args=['--start-maximized']  # Start maximized
        )
        
        # Create a new page
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        try:
            # Step 1: Navigate to FriendFilter.com
            print("📍 Step 1: Navigating to FriendFilter.com...")
            page.goto("https://friendfilter.com")
            page.wait_for_load_state("domcontentloaded")
            print("   ✅ Page loaded!")
            time.sleep(3)  # Pause to let you see the page
            
            # Step 2: Highlight the Chrome extension button
            print("🔍 Step 2: Finding Chrome extension button...")
            chrome_button = page.locator('a[href*="chrome.google.com"]').first
            
            if chrome_button.count() > 0:
                # Scroll to the button
                chrome_button.scroll_into_view_if_needed()
                time.sleep(2)
                
                # Highlight the button by adding a red border
                chrome_button.evaluate("""
                    element => {
                        element.style.border = '5px solid red';
                        element.style.backgroundColor = 'yellow';
                    }
                """)
                
                button_text = chrome_button.text_content()
                print(f"   ✅ Found button: '{button_text}'")
                print("   👀 Button is now highlighted in red/yellow!")
                time.sleep(4)
                
                # Remove highlight
                chrome_button.evaluate("""
                    element => {
                        element.style.border = '';
                        element.style.backgroundColor = '';
                    }
                """)
            
            # Step 3: Test responsive design by changing viewport
            print("📱 Step 3: Testing responsive design...")
            
            # Switch to tablet view
            print("   📱 Switching to tablet view (768x1024)...")
            page.set_viewport_size({'width': 768, 'height': 1024})
            time.sleep(3)
            
            # Switch to mobile view
            print("   📱 Switching to mobile view (375x667)...")
            page.set_viewport_size({'width': 375, 'height': 667})
            time.sleep(3)
            
            # Back to desktop
            print("   🖥️  Back to desktop view...")
            page.set_viewport_size({'width': 1920, 'height': 1080})
            time.sleep(2)
            
            # Step 4: Interact with the page
            print("🖱️  Step 4: Interacting with page elements...")
            
            # Find and highlight all navigation links
            nav_links = page.locator('nav a, header a')
            nav_count = nav_links.count()
            
            if nav_count > 0:
                print(f"   🧭 Found {nav_count} navigation links, highlighting them...")
                
                # Highlight each navigation link one by one
                for i in range(min(5, nav_count)):
                    link = nav_links.nth(i)
                    if link.is_visible():
                        # Highlight this link
                        link.evaluate("""
                            element => {
                                element.style.backgroundColor = 'lightblue';
                                element.style.padding = '5px';
                                element.style.border = '2px solid blue';
                            }
                        """)
                        
                        try:
                            link_text = link.text_content().strip()
                            if link_text:
                                print(f"   👆 Highlighting: '{link_text}'")
                                time.sleep(1.5)
                        except:
                            pass
                        
                        # Remove highlight
                        link.evaluate("""
                            element => {
                                element.style.backgroundColor = '';
                                element.style.padding = '';
                                element.style.border = '';
                            }
                        """)
            
            # Step 5: Scroll through the page
            print("📜 Step 5: Scrolling through the page...")
            
            # Scroll down slowly
            for i in range(5):
                page.evaluate(f"window.scrollTo(0, {i * 300})")
                time.sleep(1)
            
            # Scroll back to top
            print("   ⬆️  Scrolling back to top...")
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(2)
            
            # Step 6: Take a screenshot
            print("📸 Step 6: Taking screenshot...")
            page.screenshot(path="visual_demo_screenshot.png", full_page=True)
            print("   ✅ Screenshot saved as 'visual_demo_screenshot.png'")
            time.sleep(2)
            
            # Step 7: Test form interactions (if any exist)
            print("📝 Step 7: Looking for interactive elements...")
            
            # Look for any input fields
            inputs = page.locator('input')
            input_count = inputs.count()
            
            if input_count > 0:
                print(f"   📝 Found {input_count} input fields")
                # Highlight first input field
                first_input = inputs.first
                first_input.evaluate("""
                    element => {
                        element.style.border = '3px solid green';
                        element.style.backgroundColor = 'lightgreen';
                    }
                """)
                time.sleep(2)
            else:
                print("   📝 No input fields found on this page")
            
            # Step 8: Final demonstration
            print("🎯 Step 8: Final demonstration - Testing Chrome button interaction...")
            
            # Scroll back to Chrome button
            if chrome_button.count() > 0:
                chrome_button.scroll_into_view_if_needed()
                time.sleep(1)
                
                # Highlight it again
                chrome_button.evaluate("""
                    element => {
                        element.style.border = '5px solid green';
                        element.style.backgroundColor = 'lightgreen';
                        element.style.transform = 'scale(1.1)';
                        element.style.transition = 'all 0.3s';
                    }
                """)
                
                print("   🎯 Chrome button highlighted and ready for interaction!")
                print("   (In a real test, we would click this button)")
                time.sleep(3)
                
                # Note: We don't actually click it to avoid opening Chrome Web Store
                print("   ℹ️  Skipping actual click to avoid opening new tabs")
            
            print("\n🎉 Visual demo completed!")
            print("   👀 You should have seen the browser:")
            print("   • Load the FriendFilter.com website")
            print("   • Highlight the Chrome extension button") 
            print("   • Test responsive design across different screen sizes")
            print("   • Highlight navigation elements")
            print("   • Scroll through the page")
            print("   • Take a screenshot")
            print("   • Interact with page elements")
            
            # Keep browser open for a moment
            print("\n⏳ Keeping browser open for 5 more seconds...")
            time.sleep(5)
            
        except Exception as e:
            print(f"❌ Error during demo: {str(e)}")
        
        finally:
            print("🔒 Closing browser...")
            browser.close()

if __name__ == "__main__":
    print("🎬 Starting Visual Playwright Demo")
    print("This will open a browser window and show you Playwright in action!")
    print("\nMake sure you can see your screen - the browser will open shortly...")
    time.sleep(3)
    
    visual_demo()
    
    print("\n✅ Demo finished!")
    print("You just saw Playwright:")
    print("• Automatically control a real browser")
    print("• Navigate websites and find elements") 
    print("• Test responsive design")
    print("• Interact with page elements")
    print("• Take screenshots")
    print("\n🚀 This is how you can automate testing of any website!")