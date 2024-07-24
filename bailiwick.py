from itertools import islice
import dns.resolver
import subprocess
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import ipaddress

resolver = dns.resolver.Resolver()
resolver.nameservers = ['127.0.0.1']
resolver.port = 8053

def is_in_total_bailiwick(domain):
    try:
        result = resolver.resolve(domain, 'NS')
        name_servers = [ns.target.to_text().strip('.') for ns in result]
        for ns_domain in name_servers:
            if not ns_domain.endswith(domain):
                return False
        return True
    except Exception as e:
        print(f"Error checking bailiwick for {domain}: {e}")
        return None  
    
def is_in_partial_bailiwick(domain):
    try:
        result = resolver.resolve(domain, 'NS')
        name_servers = [ns.target.to_text().strip('.') for ns in result]
        for ns_domain in name_servers:
            if ns_domain.endswith(domain):
                return True
        return False
    except Exception as e:
        print(f"Error checking bailiwick for {domain}: {e}")
        return None  


def calculate_total_bailiwick_percentage(domains):
    total_processed_domains = 0  # Count only domains processed without errors
    in_bailiwick_count = 0

    for domain in domains:
        result = is_in_total_bailiwick(domain)
        if result is not None:  
            total_processed_domains += 1
            if result:
                in_bailiwick_count += 1

    if total_processed_domains == 0:
        return 0  # Prevent division by zero if all domains had errors
    percentage = (in_bailiwick_count / total_processed_domains) * 100
    return percentage

def calculate_partial_bailiwick_percentage(domains):
    total_processed_domains = 0 
    in_bailiwick_count = 0

    for domain in domains:
        result = is_in_partial_bailiwick(domain)
        if result is not None:  
            total_processed_domains += 1
            if result:
                in_bailiwick_count += 1

    if total_processed_domains == 0:
        return 0  # Prevent division by zero if all domains had errors
    percentage = (in_bailiwick_count / total_processed_domains) * 100
    return percentage