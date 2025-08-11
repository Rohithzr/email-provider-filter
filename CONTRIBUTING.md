# Contributing to Email Provider Filter

Thank you for your interest in contributing! This project aims to provide a comprehensive, accurate dataset of email domain classifications.

## How You Can Help

### 🐛 Report Issues
- Found a domain that's incorrectly categorized? 
- Discovered missing disposable email services?
- Use our [issue templates](.github/ISSUE_TEMPLATE) to report problems

### 📊 Contribute Data
- Submit new domains you've discovered
- Suggest reliable data sources
- Help verify existing classifications

### 💻 Improve Code
- Enhance the aggregation scripts
- Add new output formats
- Improve documentation

## Getting Started

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a new branch for your changes
4. **Test** your changes by running:
   ```bash
   python3 scripts/aggregate.py
   python3 tests/test_categorization.py
   ```
5. **Submit** a pull request

## Data Contribution Guidelines

### Adding New Domains
- **One domain per line** in the appropriate source file
- **Verify** domains are actually disposable/free/paid before submitting
- **Provide evidence** of your testing in the PR description

### Suggesting New Sources
- Must be publicly accessible
- Should be maintained/updated regularly  
- Include the URL and description of the source
- Explain why it's valuable to include

## Code Guidelines

- **Keep it simple** - readable code is maintainable code
- **Add comments** for complex logic
- **Test your changes** before submitting
- **Follow existing patterns** in the codebase

## Quality Standards

- All domains must be verified before inclusion
- False positives should be minimized using the allowlist
- Sources should be reputable and maintained
- Changes should not break existing functionality

## Questions?

- Check existing [issues](https://github.com/Rohithzr/email-provider-filter/issues)
- Create a new issue for discussion
- Be patient and respectful in all interactions

We appreciate every contribution, no matter how small! 🙏