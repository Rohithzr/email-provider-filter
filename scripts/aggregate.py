#!/usr/bin/env python3
"""
Main aggregation script to combine all sources and generate final output files.
"""

import requests
import json
import os
from typing import Set, Dict, List, Tuple
from datetime import datetime

def load_domains_from_file(file_path: str) -> Set[str]:
    """Load domains from a file, one per line, ignoring empty lines and comments."""
    domains = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    domains.add(line.lower())
    return domains

def download_source(url: str, output_file: str) -> None:
    """Download a source file."""
    print(f"Downloading {url}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"Saved to {output_file}")

def categorize_domains() -> Tuple[Set[str], Set[str], Set[str]]:
    """Categorize domains into disposable, free, and paid personal."""
    
    # Create temp directory
    os.makedirs('temp', exist_ok=True)
    
    # Load sources configuration
    with open('sources/sources.json', 'r') as f:
        sources = json.load(f)
    
    # Download and load disposable domains
    disposable_url = sources['disposable'][0]['url']
    download_source(disposable_url, 'temp/disposable.txt')
    disposable_domains = load_domains_from_file('temp/disposable.txt')
    
    # Add our custom disposable domains
    custom_disposable = load_domains_from_file('sources/custom_disposable.txt')
    disposable_domains.update(custom_disposable)
    
    # Load paid personal domains
    paid_personal_domains = load_domains_from_file('sources/paid_personal.txt')
    
    # Download all provider domains
    all_providers_url = sources['free_paid'][0]['url']
    download_source(all_providers_url, 'temp/all_providers.txt')
    all_provider_domains = load_domains_from_file('temp/all_providers.txt')
    
    # Load allowlist
    allowlist = load_domains_from_file('sources/allowlist.txt')
    
    # Remove disposable, paid personal, and allowlisted domains from all_providers
    free_domains = all_provider_domains - disposable_domains - paid_personal_domains - allowlist
    
    return disposable_domains, free_domains, paid_personal_domains

def generate_outputs(disposable: Set[str], free: Set[str], paid_personal: Set[str]) -> None:
    """Generate final output files in multiple formats."""
    
    os.makedirs('output', exist_ok=True)
    
    # Combined data structure
    data = {
        'metadata': {
            'generated': datetime.utcnow().isoformat() + 'Z',
            'total_domains': len(disposable) + len(free) + len(paid_personal),
            'categories': {
                'disposable': len(disposable),
                'free': len(free),
                'paid_personal': len(paid_personal)
            }
        },
        'domains': {
            'disposable': sorted(list(disposable)),
            'free': sorted(list(free)),
            'paid_personal': sorted(list(paid_personal))
        }
    }
    
    # JSON output (most compact)
    with open('output/email_domains.json', 'w') as f:
        json.dump(data, f, separators=(',', ':'))
    
    # CSV output for easy consumption
    import csv
    with open('output/email_domains.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['domain', 'category'])
        
        for domain in sorted(disposable):
            writer.writerow([domain, 'disposable'])
        for domain in sorted(free):
            writer.writerow([domain, 'free'])
        for domain in sorted(paid_personal):
            writer.writerow([domain, 'paid_personal'])
    
    # Individual category files for convenience
    with open('output/disposable.txt', 'w') as f:
        for domain in sorted(disposable):
            f.write(f"{domain}\n")
    
    with open('output/free.txt', 'w') as f:
        for domain in sorted(free):
            f.write(f"{domain}\n")
    
    with open('output/paid_personal.txt', 'w') as f:
        for domain in sorted(paid_personal):
            f.write(f"{domain}\n")
    
    print(f"Generated outputs:")
    print(f"  - Disposable: {len(disposable)} domains")
    print(f"  - Free: {len(free)} domains") 
    print(f"  - Paid Personal: {len(paid_personal)} domains")
    print(f"  - Total: {len(disposable) + len(free) + len(paid_personal)} domains")

def main():
    print("Starting email domain aggregation...")
    
    disposable, free, paid_personal = categorize_domains()
    generate_outputs(disposable, free, paid_personal)
    
    print("Aggregation complete!")

if __name__ == "__main__":
    main()