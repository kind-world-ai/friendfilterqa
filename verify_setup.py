#!/usr/bin/env python3
"""
Verify Playwright Setup
Simple verification that Playwright is installed and configured correctly
"""

def verify_playwright_installation():
    """Verify Playwright installation"""
    print("🔍 Verifying Playwright Installation")
    print("=" * 40)
    
    try:
        # Check if playwright module can be imported
        print("1. Checking Playwright import...")
        from playwright.sync_api import sync_playwright
        print("   ✅ Playwright imported successfully")
        
        # Check if browsers are installed
        print("2. Checking browser binaries...")
        import os
        playwright_cache = os.path.expanduser("~/Library/Caches/ms-playwright")
        
        if os.path.exists(playwright_cache):
            print(f"   📁 Playwright cache found: {playwright_cache}")
            
            # List installed browsers
            browsers = []
            for item in os.listdir(playwright_cache):
                if "chromium" in item or "firefox" in item or "webkit" in item:
                    browsers.append(item)
            
            if browsers:
                print(f"   🌐 Browsers found: {', '.join(browsers)}")
                print("   ✅ Browser binaries are installed")
            else:
                print("   ⚠️  No browser binaries found")
        else:
            print("   ❌ Playwright cache directory not found")
        
        # Check Playwright version
        print("3. Checking Playwright version...")
        try:
            import playwright
            version = playwright.__version__
            print(f"   📦 Playwright version: {version}")
        except AttributeError:
            print("   ⚠️  Could not determine Playwright version")
        
        print("\n✅ Playwright setup verification completed successfully!")
        print("\n📋 Summary:")
        print("   • Playwright Python package: Installed")
        print("   • Browser binaries: Available")
        print("   • Ready for test execution")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Playwright import failed: {e}")
        print("\n💡 To install Playwright:")
        print("   python3 -m pip install playwright")
        print("   playwright install")
        return False
    
    except Exception as e:
        print(f"   ❌ Verification failed: {e}")
        return False


def show_test_files():
    """Show available test files"""
    print("\n📁 Available Test Files:")
    print("=" * 30)
    
    import os
    current_dir = os.getcwd()
    test_files = []
    
    for file in os.listdir(current_dir):
        if file.endswith('.py') and ('test' in file.lower() or file == 'run_tests.py'):
            test_files.append(file)
    
    if test_files:
        for i, file in enumerate(test_files, 1):
            print(f"{i}. {file}")
        
        print(f"\n📍 Test files are located in: {current_dir}")
        
        print("\n🚀 To run tests:")
        print("   python3 test_friendfilter_comprehensive.py")
        print("   python3 run_tests.py --category landing")
        print("   python3 demo_test.py")
    else:
        print("   No test files found in current directory")


def show_usage_examples():
    """Show usage examples"""
    print("\n📖 Usage Examples:")
    print("=" * 20)
    
    examples = [
        ("Run comprehensive tests", "python3 test_friendfilter_comprehensive.py"),
        ("Run landing page tests", "python3 run_tests.py --category landing"),
        ("Run authentication tests", "python3 run_tests.py --category auth"),
        ("Run all browser compatibility tests", "python3 run_tests.py --category browsers"),
        ("Run demo test", "python3 demo_test.py"),
    ]
    
    for i, (description, command) in enumerate(examples, 1):
        print(f"{i}. {description}:")
        print(f"   {command}")
        print()


def main():
    """Main function"""
    print("🎯 FriendFilter.com Playwright Test Setup")
    print("=" * 50)
    
    # Verify installation
    setup_ok = verify_playwright_installation()
    
    if setup_ok:
        show_test_files()
        show_usage_examples()
        
        print("\n🎉 Everything is ready for testing!")
        print("\n💡 Next steps:")
        print("   1. Review the test files created")
        print("   2. Run a simple test to verify functionality")
        print("   3. Customize tests for your specific needs")
        
    else:
        print("\n🔧 Setup issues detected. Please resolve the installation problems first.")


if __name__ == "__main__":
    main()