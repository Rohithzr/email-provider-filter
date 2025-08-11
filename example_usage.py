#!/usr/bin/env python3
"""
Example usage of the Email Provider Filter data for implementing email validation.
"""

import json
import requests
from typing import Dict, Set, Optional
from enum import Enum

class EmailCategory(Enum):
    DISPOSABLE = "disposable"
    FREE = "free" 
    PAID_PERSONAL = "paid_personal"
    BUSINESS = "business"  # Not in our lists (assumed business)

class EmailDomainFilter:
    """Email domain filter using the consolidated domain lists."""
    
    def __init__(self, data_source: str = "local"):
        """
        Initialize the filter.
        
        Args:
            data_source: "local" to load from local files, "remote" to fetch from GitHub
        """
        self.categories: Dict[str, Set[str]] = {}
        
        if data_source == "local":
            self._load_local_data()
        else:
            self._load_remote_data()
    
    def _load_local_data(self):
        """Load domain data from local JSON file."""
        try:
            with open('output/email_domains.json', 'r') as f:
                data = json.load(f)
                self.categories = {
                    'disposable': set(data['domains']['disposable']),
                    'free': set(data['domains']['free']),
                    'paid_personal': set(data['domains']['paid_personal'])
                }
                print(f"Loaded {sum(len(domains) for domains in self.categories.values())} domains from local data")
        except FileNotFoundError:
            print("Local data not found. Run 'python scripts/aggregate.py' first or use data_source='remote'")
            raise
    
    def _load_remote_data(self):
        """Load domain data from GitHub repository."""
        url = "https://raw.githubusercontent.com/Rohithzr/email-provider-filter/main/output/email_domains.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.categories = {
                'disposable': set(data['domains']['disposable']),
                'free': set(data['domains']['free']),
                'paid_personal': set(data['domains']['paid_personal'])
            }
            print(f"Loaded {sum(len(domains) for domains in self.categories.values())} domains from remote data")
        except requests.RequestException as e:
            print(f"Failed to load remote data: {e}")
            raise
    
    def categorize_domain(self, domain: str) -> EmailCategory:
        """
        Categorize an email domain.
        
        Args:
            domain: Email domain to categorize (e.g., 'gmail.com')
            
        Returns:
            EmailCategory enum value
        """
        domain = domain.lower().strip()
        
        if domain in self.categories['disposable']:
            return EmailCategory.DISPOSABLE
        elif domain in self.categories['free']:
            return EmailCategory.FREE
        elif domain in self.categories['paid_personal']:
            return EmailCategory.PAID_PERSONAL
        else:
            return EmailCategory.BUSINESS
    
    def is_business_email(self, email: str) -> bool:
        """
        Check if an email is likely from a business domain.
        
        Args:
            email: Full email address
            
        Returns:
            True if likely business email, False otherwise
        """
        try:
            domain = email.split('@')[1].lower()
            category = self.categorize_domain(domain)
            return category == EmailCategory.BUSINESS
        except (IndexError, AttributeError):
            return False
    
    def should_block_email(self, email: str, block_disposable: bool = True, 
                          block_free: bool = False, block_paid_personal: bool = False) -> tuple[bool, str]:
        """
        Determine if an email should be blocked based on filtering rules.
        
        Args:
            email: Full email address
            block_disposable: Block disposable email addresses
            block_free: Block free email providers  
            block_paid_personal: Block paid personal email providers
            
        Returns:
            Tuple of (should_block: bool, reason: str)
        """
        try:
            domain = email.split('@')[1].lower()
            category = self.categorize_domain(domain)
            
            if category == EmailCategory.DISPOSABLE and block_disposable:
                return True, f"Disposable email domain: {domain}"
            elif category == EmailCategory.FREE and block_free:
                return True, f"Free email provider: {domain}"  
            elif category == EmailCategory.PAID_PERSONAL and block_paid_personal:
                return True, f"Paid personal email provider: {domain}"
            else:
                return False, f"Allowed email domain: {domain} ({category.value})"
        except (IndexError, AttributeError):
            return True, "Invalid email format"

# Example usage and test cases
def main():
    """Example usage of the EmailDomainFilter."""
    
    print("Email Provider Filter - Example Usage")
    print("=" * 50)
    
    # Initialize filter (try local first, fallback to remote)
    try:
        filter = EmailDomainFilter("local")
    except FileNotFoundError:
        print("Local data not found, fetching from GitHub...")
        filter = EmailDomainFilter("remote")
    
    # Test email addresses
    test_emails = [
        # Business emails (should be allowed)
        "john@propulsionhq.com",
        "sarah@microsoft.com", 
        "admin@startup.io",
        
        # Free emails
        "user@gmail.com",
        "person@yahoo.com",
        "someone@hotmail.com",
        
        # Paid personal
        "secure@protonmail.com",
        "fast@fastmail.com",
        
        # Disposable
        "temp@10minutemail.com",
        "fake@mailinator.com",
        "test@emailhook.site",
        
        # Invalid
        "invalid-email",
        "",
    ]
    
    print(f"\n1. Domain Categorization:")
    print("-" * 30)
    for email in test_emails:
        if '@' in email:
            domain = email.split('@')[1]
            category = filter.categorize_domain(domain)
            print(f"{domain:<20} → {category.value}")
    
    print(f"\n2. Business Email Detection:")
    print("-" * 30) 
    for email in test_emails:
        is_business = filter.is_business_email(email)
        status = "✅ Business" if is_business else "❌ Not business"
        print(f"{email:<25} → {status}")
    
    print(f"\n3. Email Filtering Examples:")
    print("-" * 30)
    
    # Different filtering scenarios
    scenarios = [
        ("Block only disposable", True, False, False),
        ("Block disposable + free", True, True, False), 
        ("Block all non-business", True, True, True),
    ]
    
    for scenario_name, block_disp, block_free, block_paid in scenarios:
        print(f"\nScenario: {scenario_name}")
        for email in test_emails[:8]:  # Test first 8 emails
            should_block, reason = filter.should_block_email(
                email, block_disp, block_free, block_paid
            )
            status = "🚫 BLOCK" if should_block else "✅ ALLOW"
            print(f"  {email:<25} → {status:<10} ({reason})")

if __name__ == "__main__":
    main()