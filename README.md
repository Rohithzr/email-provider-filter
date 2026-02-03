# Email Provider Filter

[![Update Domains](https://github.com/Rohithzr/email-provider-filter/actions/workflows/update-domains.yml/badge.svg)](https://github.com/Rohithzr/email-provider-filter/actions/workflows/update-domains.yml)
[![Latest Release](https://img.shields.io/github/v/release/Rohithzr/email-provider-filter)](https://github.com/Rohithzr/email-provider-filter/releases/latest)
[![Domains](https://img.shields.io/badge/domains-148%2C000%2B-blue)](output/email_domains.json)
[![Updated](https://img.shields.io/badge/updated-daily-brightgreen)](#-automation)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)
[![Live Lookup](https://img.shields.io/badge/Live_Lookup-Try_it-ff69b4)](https://rohithzr.github.io/email-provider-filter/)

148,000+ email domains classified as disposable, free, or paid — updated daily, zero dependencies to consume.

## Dataset Overview

**148,654 domains** across 3 categories, updated daily:

| Category | Count | Description |
|----------|------:|-------------|
| Disposable | 79,832 | Temporary/throwaway email domains |
| Free | 68,662 | Free personal email providers |
| Paid Personal | 160 | Paid personal email services |

## Quick Start

### Quick Check (one-liner)

```python
import json, urllib.request
domains = json.loads(urllib.request.urlopen(
    "https://cdn.jsdelivr.net/gh/Rohithzr/email-provider-filter@main/output/email_domains.json"
).read())
is_disposable = "tempmail.com" in domains["domains"]["disposable"]
```

### Download the Data

**Latest Release**: [Get the latest dataset](https://github.com/Rohithzr/email-provider-filter/releases/latest)

**Direct Links**:
- [JSON Format](https://raw.githubusercontent.com/Rohithzr/email-provider-filter/main/output/email_domains.json) (most compact)
- [CSV Format](https://raw.githubusercontent.com/Rohithzr/email-provider-filter/main/output/email_domains.csv) (spreadsheet-friendly)
- [Individual Lists](https://github.com/Rohithzr/email-provider-filter/tree/main/output) (disposable.txt, free.txt, paid_personal.txt)

### CDN Access

Use [jsDelivr](https://www.jsdelivr.com/) for fast, cached access from anywhere:

| File | jsDelivr URL |
|------|-------------|
| JSON | `https://cdn.jsdelivr.net/gh/Rohithzr/email-provider-filter@main/output/email_domains.json` |
| CSV | `https://cdn.jsdelivr.net/gh/Rohithzr/email-provider-filter@main/output/email_domains.csv` |
| Disposable | `https://cdn.jsdelivr.net/gh/Rohithzr/email-provider-filter@main/output/disposable.txt` |
| Free | `https://cdn.jsdelivr.net/gh/Rohithzr/email-provider-filter@main/output/free.txt` |
| Paid Personal | `https://cdn.jsdelivr.net/gh/Rohithzr/email-provider-filter@main/output/paid_personal.txt` |

> **Note**: jsDelivr caches files for ~24 hours. For real-time updates, use the `raw.githubusercontent.com` URLs above.

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

[See full example](examples/example_usage.py)

## Use Cases

- **User Registration**: Block disposable emails during signup
- **Lead Validation**: Identify business vs personal emails
- **Email Marketing**: Improve deliverability by filtering bad domains
- **Fraud Prevention**: Detect throwaway email usage patterns
- **Data Quality**: Clean and categorize existing email lists

## How It Compares

| Feature | This Project | disposable-email-domains | mailchecker | burner-email-providers |
|---------|:------------:|:------------------------:|:-----------:|:----------------------:|
| Total Domains | **148,000+** | ~4,500 | ~35,000 | ~100,000 |
| Categories | 3 (disposable, free, paid) | 1 (disposable only) | 1 (disposable only) | 1 (disposable only) |
| Free Provider Detection | Yes | No | No | No |
| Auto-Updated | Daily | Community PRs | Manual | Weekly |
| Output Formats | JSON, CSV, TXT | TXT | Library-only | JSON |
| Business Email Detection | Yes | No | No | No |
| Live Lookup Tool | [Yes](https://rohithzr.github.io/email-provider-filter/) | No | No | No |

## Data Sources

This dataset combines multiple reliable sources:

- [disposable-email-domains](https://github.com/disposable-email-domains/disposable-email-domains) - Community-verified disposable domains
- [disposable/disposable](https://github.com/disposable/disposable) - Large auto-generated list
- [groundcat/disposable-email-domain-list](https://github.com/groundcat/disposable-email-domain-list) - MX-validated disposable domains
- [ihmpavel/free-email-domains-list](https://github.com/ihmpavel/free-email-domains-list) - Comprehensive free provider list
- Plus our own curated additions

<details>
<summary><strong>Source Overlap & Contribution Stats</strong></summary>

Run `python3 scripts/aggregate.py` to generate `output/source_stats.json` with per-source breakdowns:

| Source | Raw Domains | Unique Contribution | Overlap |
|--------|------------:|-------------------:|--------:|
| ihmpavel-free-domains | 96,649 | 96,649 | 0 |
| disposable-massive | 72,209 | 45,527 | 26,682 |
| groundcat-disposable | 27,120 | 6,352 | 20,768 |
| all-email-providers | 6,104 | 3 | 6,101 |
| disposable-email-domains | 5,156 | 19 | 5,137 |
| unkn0w-disposable | 3,617 | 77 | 3,540 |
| paid-personal | 160 | 27 | 133 |
| custom-disposable | 20 | 3 | 17 |

*Run `python3 scripts/aggregate.py` to regenerate with latest data.*

</details>

## Automation

- **Daily Updates**: GitHub Actions automatically refreshes data every day at 6 AM UTC
- **Smart Releases**: New versions only created when data actually changes
- **Deduplication**: Automatic removal of duplicates across all sources
- **Quality Control**: Allowlist prevents false positives

## Testing

```bash
# Run tests to verify data quality
python3 tests/test_categorization.py

# Expected output:
# ALL TESTS PASSED! Domain categorization is working correctly.
```

## Development

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
├── docs/              # GitHub Pages live lookup tool
└── .github/           # Automation workflows
```

## Contributing

We welcome contributions! Help us improve the dataset:

- **Report Issues**: Found incorrect categorizations? [Open an issue](https://github.com/Rohithzr/email-provider-filter/issues)
- **Add Data**: Know of new disposable services? [Submit domains](https://github.com/Rohithzr/email-provider-filter/issues/new/choose)
- **Improve Code**: Enhance scripts or add features

[Contributing Guidelines](CONTRIBUTING.md) | [Code of Conduct](CODE_OF_CONDUCT.md)

## Why This Project?

Most existing solutions are either:
- **Incomplete**: Missing thousands of domains
- **Outdated**: Not regularly maintained
- **Narrow**: Focus on only one category
- **Fragmented**: Scattered across multiple sources

This project solves all those problems by providing a **single, comprehensive, automatically updated** source.

## License

MIT License - Free for commercial and personal use.

## Acknowledgments

Thanks to the maintainers of every source repository that makes this project possible:

- [@disposable-email-domains](https://github.com/disposable-email-domains) — community-curated disposable domain list
- [@disposable](https://github.com/disposable) — massive auto-generated disposable domain collection
- [@groundcat](https://github.com/groundcat) — MX-validated disposable domain list
- [@unkn0w](https://github.com/unkn0w) — disposable domain list for newsletter spam prevention
- [@ihmpavel](https://github.com/ihmpavel) — comprehensive free email domains list
- [@ammarshah](https://github.com/ammarshah) — aggregated email provider domains gist

And to every contributor who reports issues, suggests sources, and helps keep this dataset accurate.

---

**Star this repo** if it's useful for your project!
