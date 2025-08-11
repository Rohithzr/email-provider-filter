#!/usr/bin/env python3
"""
Test script to verify email domain categorization works correctly.
"""

import json
import csv
import os
from typing import Dict, Set

def load_domain_data() -> Dict[str, Set[str]]:
    """Load domain data from output files."""
    
    # Get the project root directory (parent of tests/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    # Load from JSON (most reliable)
    if os.path.exists('output/email_domains.json'):
        with open('output/email_domains.json', 'r') as f:
            data = json.load(f)
            return {
                'disposable': set(data['domains']['disposable']),
                'free': set(data['domains']['free']),
                'paid_personal': set(data['domains']['paid_personal'])
            }
    
    # Fallback to individual files
    categories = {}
    for category in ['disposable', 'free', 'paid_personal']:
        file_path = f'output/{category}.txt'
        domains = set()
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        domains.add(line.lower())
        categories[category] = domains
    
    return categories

def test_categorization():
    """Test domain categorization with known examples."""
    
    print("Loading domain data...")
    categories = load_domain_data()
    
    # Test cases with expected categories
    test_cases = [
        # Disposable emails
        ('10minutemail.com', 'disposable'),
        ('mailinator.com', 'disposable'),
        ('emailhook.site', 'disposable'),
        ('guerrillamail.com', 'disposable'),
        ('temp-mail.org', 'disposable'),
        
        # Free emails  
        ('gmail.com', 'free'),
        ('yahoo.com', 'free'),
        ('hotmail.com', 'free'),
        ('outlook.com', 'free'),
        ('aol.com', 'free'),
        
        # Paid personal
        ('protonmail.com', 'paid_personal'),
        ('fastmail.com', 'paid_personal'),
        ('hey.com', 'paid_personal'),
        ('tutanota.com', 'paid_personal'),
        
        # Should not be in any category (business domains)
        ('google.com', None),
        ('microsoft.com', None),
        ('propulsionhq.com', None),
    ]
    
    print(f"\nTesting {len(test_cases)} domain classifications...")
    print("-" * 60)
    
    passed = 0
    failed = 0
    
    for domain, expected_category in test_cases:
        # Find which category the domain belongs to
        actual_category = None
        for category, domains in categories.items():
            if domain.lower() in domains:
                actual_category = category
                break
        
        # Test result
        if actual_category == expected_category:
            status = "✅ PASS"
            passed += 1
        else:
            status = "❌ FAIL"
            failed += 1
        
        expected_str = expected_category or "not categorized"
        actual_str = actual_category or "not categorized"
        
        print(f"{status} | {domain:<20} | Expected: {expected_str:<15} | Actual: {actual_str}")
    
    print("-" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    # Summary statistics
    print(f"\nDataset Statistics:")
    print(f"- Disposable domains: {len(categories['disposable']):,}")
    print(f"- Free domains: {len(categories['free']):,}")
    print(f"- Paid personal domains: {len(categories['paid_personal']):,}")
    print(f"- Total domains: {sum(len(domains) for domains in categories.values()):,}")
    
    return passed, failed

def test_no_overlaps():
    """Test that there are no overlapping domains between categories."""
    
    print(f"\nTesting for overlapping domains between categories...")
    categories = load_domain_data()
    
    overlaps = []
    category_names = list(categories.keys())
    
    for i, cat1 in enumerate(category_names):
        for cat2 in category_names[i+1:]:
            overlap = categories[cat1] & categories[cat2]
            if overlap:
                overlaps.append((cat1, cat2, overlap))
    
    if overlaps:
        print("❌ OVERLAP DETECTED:")
        for cat1, cat2, domains in overlaps:
            print(f"  {cat1} ∩ {cat2}: {len(domains)} domains")
            for domain in sorted(list(domains)[:5]):  # Show first 5
                print(f"    - {domain}")
            if len(domains) > 5:
                print(f"    ... and {len(domains) - 5} more")
        return False
    else:
        print("✅ No overlapping domains found")
        return True

if __name__ == "__main__":
    print("Email Provider Filter - Domain Categorization Test")
    print("=" * 60)
    
    if not os.path.exists('output/email_domains.json'):
        print("❌ Output files not found. Run 'python scripts/aggregate.py' first.")
        exit(1)
    
    # Run categorization tests
    passed, failed = test_categorization()
    
    # Test for overlaps
    no_overlaps = test_no_overlaps()
    
    # Overall result
    print("\n" + "=" * 60)
    if failed == 0 and no_overlaps:
        print("🎉 ALL TESTS PASSED! Domain categorization is working correctly.")
        exit(0)
    else:
        print("⚠️  Some tests failed. Please review the categorization logic.")
        exit(1)