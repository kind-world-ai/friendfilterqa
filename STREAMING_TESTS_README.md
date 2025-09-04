# Streaming Website E2E Tests

Automated end-to-end tests for AceStreamz.com admin panel using Playwright Python.

## 🚀 Quick Start

### Prerequisites
```bash
# Install Playwright
pip install playwright

# Install browser binaries
playwright install
```

### Run Tests
```bash
# Recommended: Run the working test
python3 test_streaming_simple.py

# Alternative: Run structured test
python3 test_streaming_admin.py

# Advanced: Run test with page objects
python3 test_streaming_improved.py
```

## 📁 Test Files

### Core Tests
- **`test_streaming_simple.py`** ✅ - Working simplified test (recommended)
- **`test_streaming_admin.py`** - Basic structured test
- **`test_streaming_improved.py`** - Enhanced test with page objects
- **`streaming_page_objects.py`** - Page object models for reusability

## 🧪 Test Coverage

### Admin Panel Workflow
1. **Login** - Admin authentication with credentials
2. **Backend Navigation** - Access admin backend
3. **User Management** - Edit user profiles (Joy Kumar)
4. **Account Management** - View account details (bitpixel coders)

### Test Credentials
- Email: `mike@nightcoders.com`
- Password: `rismoM-rywryp-gisge1`

## 🎯 Test Results

```
🚀 Starting streaming admin test...
✅ Navigated to admin panel
✅ Login completed
✅ Terms accepted
✅ Navigated to Backend
✅ Navigated to Users section
✅ User edit initiated
✅ Navigated to Accounts
✅ Account view opened
🎉 Test completed successfully!
```

## 🔧 Configuration

### Browser Options
```python
# Headless mode (for CI/CD)
browser = await p.chromium.launch(headless=True)

# Visible mode (for debugging)
browser = await p.chromium.launch(headless=False)
```

### Error Handling
- Automatic screenshot capture on failure: `test_failure.png`
- Detailed error logging with step-by-step progress

## 🚨 Troubleshooting

### Common Issues
- **Login Fails**: Check credentials are still valid
- **Element Not Found**: Website structure may have changed
- **Timeout Errors**: Increase wait times for slow networks

### Debug Mode
```bash
# Run with visible browser for debugging
python3 test_streaming_simple.py
```

## 📊 Usage Examples

### Basic Test Run
```bash
python3 test_streaming_simple.py
```

### Custom Browser
```python
# Use Firefox instead of Chromium
browser = await p.firefox.launch(headless=False)
```

## 🔍 Test Maintenance

### Updating Selectors
If website elements change, update selectors in:
- `test_streaming_simple.py` - Direct selectors
- `streaming_page_objects.py` - Page object methods

### Adding New Tests
1. Follow the pattern in `test_streaming_simple.py`
2. Add proper error handling and logging
3. Include screenshot capture on failure

---

**Created for AceStreamz.com admin panel testing**  
*Covers complete admin workflow from login to account management*
