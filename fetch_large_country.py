#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Specialized script for fetching large countries with parallel page requests
"""

import csv
import json
import sys
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

def fetch_github_external_badges(user_id):
    """Fetch GitHub external badges (Microsoft-issued) for a user"""
    url = f"https://www.credly.com/api/v1/users/{user_id}/external_badges/open_badges/public?page=1&page_size=48"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Filter only GitHub badges issued by Microsoft
        github_badges = []
        for badge in data.get('data', []):
            external_badge = badge.get('external_badge', {})
            badge_name = external_badge.get('badge_name', '')
            issuer_name = external_badge.get('issuer_name', '')
            
            # Check if it's a GitHub certification issued by Microsoft
            if issuer_name == 'Microsoft' and 'GitHub' in badge_name:
                github_badges.append(badge)
        
        return len(github_badges)
    except Exception:
        # If external badges endpoint fails, return 0 (user may have no external badges)
        return 0

def fetch_page(country, page):
    """Fetch a single page for a country"""
    url = f"https://www.credly.com/api/v1/directory?organization_id=63074953-290b-4dce-86ce-ea04b4187219&sort=alphabetical&filter%5Blocation_name%5D={country.replace(' ', '%20')}&page={page}&format=json"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Get total_pages from metadata
        metadata = data.get('metadata', {})
        total_pages = metadata.get('total_pages', 0)
        
        # For each user, add external badges count
        users = data.get('data', [])
        for user in users:
            user_id = user.get('id')
            if user_id:
                external_count = fetch_github_external_badges(user_id)
                user['badge_count'] = user.get('badge_count', 0) + external_count
        
        return (page, users, total_pages)
    except Exception as e:
        print(f"  Error on page {page}: {e}")
        return (page, [], 0)

def fetch_country_parallel(country, max_workers=20):
    """Fetch all pages for a country in parallel"""
    print(f"Fetching {country} with parallel requests...")
    
    # First, get the total number of pages
    _, _, total_pages = fetch_page(country, 1)
    
    if total_pages == 0:
        print(f"No data found for {country}")
        return []
    
    print(f"Total pages: {total_pages}")
    
    all_users = []
    
    # Fetch all pages in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_page, country, page): page 
                   for page in range(1, total_pages + 1)}
        
        completed = 0
        for future in as_completed(futures):
            page, users, _ = future.result()
            all_users.extend(users)
            completed += 1
            
            if completed % 100 == 0:
                print(f"  Progress: {completed}/{total_pages} pages ({len(all_users)} users)")
    
    print(f"✓ Completed: {len(all_users)} users from {total_pages} pages")
    return all_users

def save_to_csv(country, users, output_dir='datasource'):
    """Save users to CSV file"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    file_suffix = country.lower().replace(' ', '-')
    output_file = f"{output_dir}/github-certs-{file_suffix}.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['first_name', 'middle_name', 'last_name', 'badge_count', 'profile_url'])
        
        for user in users:
            writer.writerow([
                user.get('first_name', ''),
                user.get('middle_name', ''),
                user.get('last_name', ''),
                user.get('badge_count', 0),
                user.get('url', '')
            ])
    
    print(f"Saved to {output_file}")
    return output_file

def main():
    """Main execution"""
    if len(sys.argv) < 2:
        print("Usage: ./fetch_large_country.py <country_name>")
        print("Example: ./fetch_large_country.py India")
        sys.exit(1)
    
    country = sys.argv[1]
    
    print("=" * 80)
    print(f"Fetching large country: {country}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    # Fetch with parallel requests (20 concurrent pages)
    users = fetch_country_parallel(country, max_workers=20)
    
    if users:
        save_to_csv(country, users)
        print()
        print("=" * 80)
        print(f"✅ Success! Downloaded {len(users)} users")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        sys.exit(0)
    else:
        print("❌ No users found")
        sys.exit(1)

if __name__ == "__main__":
    main()
