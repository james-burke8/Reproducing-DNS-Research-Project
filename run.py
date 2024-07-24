from itertools import islice
import dns.resolver
import subprocess
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import ipaddress
from resolver import *
from bailiwick import *

domains2 = [
    "stake.com",
    "roobet.com",
    "draftkings.com",
    "microsoft.com",
    "a-msedge.net", 
]

if __name__ == "__main__":
    with open('top-1m.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        domains = [next(reader)[0]for i in range(10000)]
        
    resolver_main(domains) 
    total_bailiwick_percentage = calculate_total_bailiwick_percentage(domains)
    partial_bailiwick_percentage = calculate_partial_bailiwick_percentage(domains)
    
    print(f"Total Bailiwick Percentage: {total_bailiwick_percentage}%")
    print(f"Partial Bailiwick Percentage: {partial_bailiwick_percentage}%")

    print(f"NS Errors: {len(error_domains.get('ns_errors'))}")
    print(f"Domain Errors: {len(error_domains.get('domain_errors'))}")

""""
Provided via OpenAI's ChatGPT:
The code provided by me (or any other OpenAI model) is generated on-the-fly and is not copyrighted or 
sourced from any specific external location. You're free to use, modify, and distribute the code as you see fit.
Licensing Requirements:
There are no specific licensing requirements for the code. 
You can consider it as being under a permissive license, like the MIT License or similar, 
which means you can use it for any purpose without any restrictions, and you're not 
required to include the original copyright notice or disclaimers.
"""
