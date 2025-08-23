# Email Provider Filter

Email Provider Filter is a Python-based data aggregation system that categorizes email domains into disposable, free, and paid personal categories. It automatically downloads, processes, and maintains an up-to-date dataset of 141,000+ email domains with daily automated updates via GitHub Actions.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap, Build, and Test
- **Python Requirements**: Python 3.x (tested with 3.12+) and the `requests` module
- **Install Dependencies**: 
  ```bash
  python3 -m pip install --upgrade pip
  pip install requests
  ```
- **Generate Dataset**: 
  ```bash
  python3 scripts/aggregate.py
  ```
  - **Timing**: 0.8 seconds to complete. NEVER CANCEL. Set timeout to 30+ seconds for safety.
  - Downloads source data, deduplicates, categorizes, and generates output files
  - Creates files in `output/` directory (JSON, CSV, and individual text files)
  - Shows deprecation warning about datetime.utcnow() - this is expected and safe to ignore

- **Run Tests**: 
  ```bash
  python3 tests/test_categorization.py
  ```
  - **Timing**: 0.1 seconds to complete. NEVER CANCEL. Set timeout to 15+ seconds.
  - Validates domain categorization with known test cases
  - Expected output: "🎉 ALL TESTS PASSED! Domain categorization is working correctly."

### Example Usage and Validation
- **Local Dataset Usage**:
  ```bash
  python3 examples/example_usage.py
  ```
  - **Timing**: 0.14 seconds to complete. NEVER CANCEL. Set timeout to 15+ seconds.
  - Demonstrates email filtering, business email detection, and domain categorization
  - Shows usage with both local and remote data loading

- **Remote Dataset Usage**:
  ```bash
  python3 -c "from examples.example_usage import EmailDomainFilter; filter = EmailDomainFilter('remote'); print('Remote data loaded successfully')"
  ```
  - **Timing**: 3 seconds to complete. NEVER CANCEL. Set timeout to 15+ seconds.
  - Tests network connectivity and GitHub data access

## Validation

### CRITICAL Manual Validation Steps
After making any changes to the codebase, ALWAYS run these validation scenarios:

1. **End-to-End Data Generation and Testing**:
   ```bash
   python3 scripts/aggregate.py && python3 tests/test_categorization.py
   ```
   - Verifies complete data pipeline from source download to validation

2. **Business Email Detection Validation**:
   ```bash
   python3 -c "
   from examples.example_usage import EmailDomainFilter
   filter = EmailDomainFilter('local')
   # Test business emails (should return True)
   assert filter.is_business_email('user@company.com') == True
   assert filter.is_business_email('admin@microsoft.com') == True
   # Test non-business emails (should return False)  
   assert filter.is_business_email('user@gmail.com') == False
   assert filter.is_business_email('temp@10minutemail.com') == False
   print('✅ Business email detection working correctly')
   "
   ```

3. **Domain Categorization Accuracy**:
   ```bash
   python3 -c "
   from examples.example_usage import EmailDomainFilter
   from examples.example_usage import EmailCategory
   filter = EmailDomainFilter('local')
   # Test known categories
   assert filter.categorize_domain('10minutemail.com') == EmailCategory.DISPOSABLE
   assert filter.categorize_domain('gmail.com') == EmailCategory.FREE
   assert filter.categorize_domain('protonmail.com') == EmailCategory.PAID_PERSONAL
   assert filter.categorize_domain('company.com') == EmailCategory.BUSINESS
   print('✅ Domain categorization working correctly')
   "
   ```

4. **Output File Generation Validation**:
   ```bash
   python3 scripts/aggregate.py
   # Verify all expected output files exist
   ls -la output/email_domains.json output/email_domains.csv output/disposable.txt output/free.txt output/paid_personal.txt
   # Verify JSON structure
   python3 -c "import json; data=json.load(open('output/email_domains.json')); print(f'Total domains: {data[\"metadata\"][\"total_domains\"]}'); assert 'disposable' in data['domains']; assert 'free' in data['domains']; assert 'paid_personal' in data['domains']; print('✅ Output files valid')"
   ```

### File Compilation Check
- **Validate Python Syntax**:
  ```bash
  find . -name "*.py" -exec python3 -m py_compile {} \;
  ```
  - **Timing**: 0.5 seconds to complete. Should complete without errors.

## Common Tasks

### Repository Structure
```
├── sources/           # Source configurations and custom lists
│   ├── sources.json   # URLs and metadata for data sources
│   ├── allowlist.txt  # Domains to exclude from disposable category
│   ├── custom_disposable.txt  # Manual disposable domain additions
│   └── paid_personal.txt      # Paid personal email providers
├── scripts/           # Data processing scripts  
│   ├── aggregate.py   # Main aggregation script (primary build tool)
│   └── compare_sources.py  # Source comparison utilities
├── output/            # Generated dataset files (created by aggregate.py)
│   ├── email_domains.json    # Complete dataset with metadata
│   ├── email_domains.csv     # CSV format for spreadsheets
│   ├── disposable.txt        # Disposable domains only
│   ├── free.txt             # Free provider domains only
│   └── paid_personal.txt    # Paid personal provider domains only
├── tests/             # Quality assurance tests
│   └── test_categorization.py  # Domain classification tests
├── examples/          # Usage examples and demos
│   └── example_usage.py       # Complete usage demonstration
└── .github/           # Automation workflows
    └── workflows/update-domains.yml  # Daily update automation
```

### Key Files to Monitor
- **Always check `sources/sources.json` after modifying data sources** - contains URLs, counts, and metadata
- **Always run `python3 scripts/aggregate.py` after changing any source files** - regenerates all output data
- **Always verify `output/email_domains.json` structure after build** - contains metadata and domain counts
- **Check `.github/workflows/update-domains.yml`** - for automation pipeline changes

### Data Source Information
The project aggregates from multiple sources:
- **Disposable Email Sources**: 3 external URLs downloading ~75K domains
- **Free/Paid Provider Sources**: 2 external URLs downloading ~96K domains  
- **Custom Sources**: Local files for manual additions and paid personal providers
- **Allowlist**: Prevents false positives in disposable categorization

### Expected Dataset Size
- **Total Domains**: ~141,000+ domains
- **Disposable**: ~71,600 domains
- **Free**: ~69,900 domains
- **Paid Personal**: ~22 domains
- **Output Files**: JSON (~2.4MB), CSV (~3.4MB), Text files (~1MB each)

### GitHub Actions Automation
- **Trigger**: Daily at 6 AM UTC, on push to main, or manual trigger
- **Process**: Downloads sources, runs aggregation, tests data, commits changes, creates releases
- **Duration**: ~2-3 minutes total (most time spent on GitHub setup, actual processing is ~10 seconds)
- **Smart Releases**: Only creates new releases when domain data actually changes

### Network Dependencies
- **Required for build**: Internet access to download source files from GitHub and external repos
- **Offline usage**: After initial build, all functionality works offline using generated files
- **Remote usage**: Example code can fetch data directly from GitHub without local build

### Adding New Sources
1. Update `sources/sources.json` with new source URL and metadata
2. Run `python3 scripts/aggregate.py` to test integration
3. Run `python3 tests/test_categorization.py` to verify no conflicts
4. Add test cases to `tests/test_categorization.py` if needed

### Troubleshooting
- **"requests module not found"**: Run `pip install requests`
- **"Local data not found"**: Run `python3 scripts/aggregate.py` first
- **"Failed to load remote data"**: Check internet connectivity or use local data
- **Source download failures**: Individual source failures are logged but don't break the build
- **Empty output files**: Check source URLs in `sources/sources.json` are accessible
- **Temporary files accumulating**: The `temp/` directory stores downloaded source files - can be safely deleted
- **DeprecationWarning about datetime.utcnow()**: Expected and safe to ignore - code still works correctly

### Development Notes
- **Temp directory**: `python3 scripts/aggregate.py` creates a `temp/` directory with downloaded source files (~2.7MB total)
- **Clean builds**: Delete `temp/` and `output/` directories to force complete regeneration
- **Offline development**: After initial build, all functionality works without internet connection
- **File sizes**: Generated files are substantial (JSON: 2.4MB, CSV: 3.4MB) - normal for 141K+ domains
