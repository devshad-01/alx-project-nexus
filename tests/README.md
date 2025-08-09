# Tests Directory

This directory contains all testing files and results for the ALX Project Nexus API.

## Structure:

### `api_tests/`
Contains API testing scripts and tools:

- `comprehensive_api_test.py` - Complete API endpoint testing
- `quick_test_registration.py` - Quick registration endpoint test  
- `test_api_complete.py` - API completeness verification
- `test_api_comprehensive.py` - Comprehensive API functionality tests
- `*_backup.py` - Backup versions of test files
- `*_fixed.py` - Fixed/updated versions of test files

### `results/`
Contains test execution results and logs:

- `api_test_results_*.json` - JSON test result files
- `django.log` - Django application logs
- `*.log` - Various log files from test runs

## Usage:

### Running API Tests:
```bash
# From project root, activate environment first
source scripts/activate_env.sh

# Run comprehensive API test
python tests/api_tests/comprehensive_api_test.py

# Run quick registration test
python tests/api_tests/quick_test_registration.py
```

### Viewing Results:
```bash
# View latest test results
cat tests/results/api_test_results_*.json | tail -1 | python -m json.tool

# View Django logs
tail -f tests/results/django.log
```

## Note:
All test files and results are excluded from version control via `.gitignore` as they are for development purposes only.
