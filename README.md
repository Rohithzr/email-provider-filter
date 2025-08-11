# Email Provider Filter

A comprehensive, automatically updated dataset of email domains categorized by type. Perfect for implementing email validation and filtering in your applications.

## 📊 Dataset Overview

**141,580+ domains** across 3 categories, updated daily:

- **🗑️ Disposable**: 71,627 temporary/throwaway email domains  
- **📧 Free**: 69,931 free personal email providers
- **💳 Paid Personal**: 22 paid personal email services

## 🚀 Quick Start

### Download the Data

**Latest Release**: [Get the latest dataset](https://github.com/Rohithzr/email-provider-filter/releases/latest)

**Direct Links**:
- [📄 JSON Format](https://raw.githubusercontent.com/Rohithzr/email-provider-filter/main/output/email_domains.json) (most compact)
- [📊 CSV Format](https://raw.githubusercontent.com/Rohithzr/email-provider-filter/main/output/email_domains.csv) (spreadsheet-friendly)
- [📝 Individual Lists](https://github.com/Rohithzr/email-provider-filter/tree/main/output) (disposable.txt, free.txt, paid_personal.txt)

### Usage Example

```python
# Load and use the dataset
from examples.example_usage import EmailDomainFilter

# Initialize filter (loads from GitHub automatically)
filter = EmailDomainFilter("remote")

# Check if email is from business domain
is_business = filter.is_business_email("user@company.com")  # True
is_business = filter.is_business_email("user@gmail.com")    # False

# Apply filtering rules
should_block, reason = filter.should_block_email(
    "temp@10minutemail.com", 
    block_disposable=True
)
# Returns: (True, "Disposable email domain: 10minutemail.com")
```

[👉 See full example](examples/example_usage.py)

## 🎯 Use Cases

- **User Registration**: Block disposable emails during signup
- **Lead Validation**: Identify business vs personal emails  
- **Email Marketing**: Improve deliverability by filtering bad domains
- **Fraud Prevention**: Detect throwaway email usage patterns
- **Data Quality**: Clean and categorize existing email lists

## 📁 Data Sources

This dataset combines multiple reliable sources:

- [disposable-email-domains](https://github.com/disposable-email-domains/disposable-email-domains) - Community-verified disposable domains
- [disposable/disposable](https://github.com/disposable/disposable) - Large auto-generated list  
- [ihmpavel/free-email-domains-list](https://github.com/ihmpavel/free-email-domains-list) - Comprehensive free provider list
- Plus our own curated additions

## 🤖 Automation

- **Daily Updates**: GitHub Actions automatically refreshes data every day at 6 AM UTC
- **Smart Releases**: New versions only created when data actually changes
- **Deduplication**: Automatic removal of duplicates across all sources
- **Quality Control**: Allowlist prevents false positives

## 🧪 Testing

```bash
# Run tests to verify data quality
python3 tests/test_categorization.py

# Expected output: 
# 🎉 ALL TESTS PASSED! Domain categorization is working correctly.
```

## 🛠️ Development

### Setup
```bash
git clone https://github.com/Rohithzr/email-provider-filter.git
cd email-provider-filter
python3 scripts/aggregate.py  # Generate fresh dataset
```

### Project Structure
```
├── sources/           # Source configurations and custom lists
├── scripts/           # Data processing scripts  
├── output/            # Generated dataset files
├── tests/             # Quality assurance tests
├── examples/          # Usage examples and demos
└── .github/           # Automation workflows
```

## 🤝 Contributing

We welcome contributions! Help us improve the dataset:

- **🐛 Report Issues**: Found incorrect categorizations? [Open an issue](https://github.com/Rohithzr/email-provider-filter/issues)
- **📊 Add Data**: Know of new disposable services? [Submit domains](https://github.com/Rohithzr/email-provider-filter/issues/new/choose)
- **💻 Improve Code**: Enhance scripts or add features

[📖 Contributing Guidelines](CONTRIBUTING.md) | [📋 Code of Conduct](CODE_OF_CONDUCT.md)

## 📈 Why This Project?

Most existing solutions are either:
- **Incomplete**: Missing thousands of domains
- **Outdated**: Not regularly maintained  
- **Narrow**: Focus on only one category
- **Fragmented**: Scattered across multiple sources

This project solves all those problems by providing a **single, comprehensive, automatically updated** source.

## 📄 License

MIT License - Free for commercial and personal use.

## 🙏 Acknowledgments

Thanks to all the maintainers of the source repositories and contributors who help keep this dataset accurate and comprehensive.

---

**⭐ Star this repo** if it's useful for your project!