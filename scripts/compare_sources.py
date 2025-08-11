#!/usr/bin/env python3
"""
Compare email domain sources to extract differences and categorize domains.
Handles large files efficiently without loading everything into memory.
"""

import requests
import json
import os
from typing import Set, Dict, List

def download_source(url: str, output_file: str) -> None:
    """Download a source file if it doesn't exist locally."""
    if not os.path.exists(output_file):
        print(f"Downloading {url}...")
        response = requests.get(url)
        response.raise_for_status()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Saved to {output_file}")

def load_domains_from_file(file_path: str) -> Set[str]:
    """Load domains from a file, one per line, ignoring empty lines and comments."""
    domains = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                domains.add(line.lower())
    return domains

def main():
    # Create temp directory for downloads
    os.makedirs('temp', exist_ok=True)
    
    # Download sources
    disposable_url = "https://raw.githubusercontent.com/disposable-email-domains/disposable-email-domains/refs/heads/main/disposable_email_blocklist.conf"
    all_providers_url = "https://gist.githubusercontent.com/ammarshah/f5c2624d767f91a7cbdc4e54db8dd0bf/raw/660fd949eba09c0b86574d9d3aa0f2137161fc7c/all_email_provider_domains.txt"
    
    download_source(disposable_url, 'temp/disposable.txt')
    download_source(all_providers_url, 'temp/all_providers.txt')
    
    # Load domain sets
    print("Loading domain sets...")
    disposable_domains = load_domains_from_file('temp/disposable.txt')
    all_provider_domains = load_domains_from_file('temp/all_providers.txt')
    
    print(f"Disposable domains: {len(disposable_domains)}")
    print(f"All provider domains: {len(all_provider_domains)}")
    
    # Find domains in all_providers that are NOT in disposable
    free_paid_candidates = all_provider_domains - disposable_domains
    print(f"Free/Paid candidates (after removing disposable overlap): {len(free_paid_candidates)}")
    
    # Find overlapping domains (for verification)
    overlap = disposable_domains & all_provider_domains
    print(f"Overlapping domains: {len(overlap)}")
    
    # Save results
    os.makedirs('output', exist_ok=True)
    
    with open('output/disposable_domains.txt', 'w') as f:
        for domain in sorted(disposable_domains):
            f.write(f"{domain}\n")
    
    with open('output/free_paid_candidates.txt', 'w') as f:
        for domain in sorted(free_paid_candidates):
            f.write(f"{domain}\n")
    
    with open('output/overlap_analysis.txt', 'w') as f:
        f.write(f"Analysis Results:\n")
        f.write(f"Disposable domains: {len(disposable_domains)}\n")
        f.write(f"All provider domains: {len(all_provider_domains)}\n")
        f.write(f"Overlapping domains: {len(overlap)}\n")
        f.write(f"Free/Paid candidates: {len(free_paid_candidates)}\n\n")
        f.write("Sample overlapping domains:\n")
        for domain in sorted(list(overlap)[:20]):
            f.write(f"  {domain}\n")

if __name__ == "__main__":
    main()