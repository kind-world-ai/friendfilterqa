#!/usr/bin/env python3
"""
FriendFilter.com Test Runner
Simplified script to run specific test categories or all tests
"""

import argparse
import sys
from test_friendfilter_comprehensive import *


def run_specific_tests(test_category):
    """Run tests for a specific category"""
    test_mapping = {
        "landing": TestLandingPage,
        "auth": TestUserAuthentication,
        "pricing": TestPricingPage,
        "dashboard": TestDashboardFunctionality,
        "extension": TestExtensionFeatures,
        "forms": TestFormValidation,
        "performance": TestPerformanceAndSEO,
        "accessibility": TestAccessibility,
        "browsers": TestCrossBrowserCompatibility,
        "errors": TestErrorHandling
    }
    
    if test_category not in test_mapping:
        print(f"❌ Unknown test category: {test_category}")
        print(f"Available categories: {', '.join(test_mapping.keys())}")
        return
    
    test_class = test_mapping[test_category]
    print(f"🧪 Running {test_class.__name__} tests...")
    
    test_instance = test_class()
    test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
    
    passed = 0
    failed = 0
    
    for method_name in test_methods:
        try:
            print(f"  ▶️  {method_name}")
            method = getattr(test_instance, method_name)
            method()
            print(f"  ✅ {method_name} - PASSED")
            passed += 1
        except Exception as e:
            print(f"  ❌ {method_name} - FAILED: {str(e)}")
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")


def main():
    parser = argparse.ArgumentParser(description="Run FriendFilter.com Playwright tests")
    parser.add_argument(
        "--category", 
        choices=["landing", "auth", "pricing", "dashboard", "extension", "forms", 
                "performance", "accessibility", "browsers", "errors", "all"],
        default="all",
        help="Test category to run"
    )
    parser.add_argument("--headless", action="store_true", help="Run tests in headless mode")
    
    args = parser.parse_args()
    
    print("🚀 FriendFilter.com Test Runner")
    print("=" * 40)
    
    if args.category == "all":
        results = run_comprehensive_tests()
        return
    
    run_specific_tests(args.category)


if __name__ == "__main__":
    main()