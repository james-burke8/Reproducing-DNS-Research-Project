from itertools import islice
import dns.resolver
import subprocess
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import ipaddress
import json

resolver = dns.resolver.Resolver()
resolver.nameservers = ['127.0.0.1']
resolver.port = 8053

error_domains = {"ns_errors": {}, "domain_errors": {}}

def reverse_ip(ip_address):
    parts = ip_address.split('.')
    reversed_parts = parts[::-1]
    reversed_ip = '.'.join(reversed_parts)
    return reversed_ip

def get_ns_records(domain):
    try:
        result = resolver.resolve(domain, 'NS')
        name_servers = []
        for data in result:
            name_servers.append(data.to_text())
        return name_servers
    except Exception as e:
        error_domains["ns_errors"][domain] = str(e)
        return []

def get_ip_addresses(ns_name):
    try:
        result = resolver.resolve(ns_name, 'A')
        ip_addresses = []
        for data in result:
            ip_addresses.append(data.to_text())
        return ip_addresses
    except Exception as e:
        error_domains["domain_errors"][ns_name] = str(e)
        return []


def query_ip_for_asn(ip_address):
    """Query ASN for a given IP address."""
    try:
        query_name = f'{reverse_ip(ip_address)}.origin.asn.cymru.com'
        txt_records = resolver.resolve(query_name, 'TXT')
        return txt_records[0].to_text().strip('"').split(' ')[0]
    except Exception as e:
        print(f"Error querying ASN for IP {ip_address}: {e}")
        return None

def query_asn_for_company(asn):
    """Query the company name for a given ASN."""
    try:
        query_name = f'AS{asn}.asn.cymru.com'
        txt_records = resolver.resolve(query_name, 'TXT')
        return txt_records[0].to_text().strip('"').split(' | ')[-1]
    except Exception as e:
        print(f"Error querying company for ASN {asn}: {e}")
        return None

def process_domain(domain):
    """Process a single domain to get its NS records, IPs, ASNs, and company names."""
    ns_info = {}
    error_occurred = False  
    for ns in get_ns_records(domain):
        ips = get_ip_addresses(ns)
        if not ips: 
            error_occurred = True
        ns_info[ns] = {'IPs': ips, 'ASNs': {}}
        for ip in ips:
            asn = query_ip_for_asn(ip)
            company = None
            if asn:
                company = query_asn_for_company(asn)
            ns_info[ns]['ASNs'][ip] = {"ASN": asn, "Company": company}
    return {domain: ns_info}, error_occurred


def resolver_main(domains):
    """Main function to process a list of domains and save the results to a JSON file."""
    results = {}
    error_free_domains = {}  
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(process_domain, domain) for domain in domains]
        for future in as_completed(futures):
            domain_data, error_occurred = future.result()
            if not error_occurred:
                error_free_domains.update(domain_data)
            results.update(domain_data)
    with open('error_free_domains.json', 'w') as f:
        json.dump(error_free_domains, f, indent=4)


def calculate_metrics_from_json(data):
    affected_by_company = {}  # Dictionary to hold counts of domains affected by each company
    exclusively_hosted_by_company = {}  # Dictionary to hold counts of domains exclusively hosted by each company

    for domain, ns_info in data.items():
        unique_companies = {asn_info["Company"] for ns in ns_info.values() for ip, asn_info in ns["ASNs"].items() if "Company" in asn_info}

        # Count domains affected by each company
        for company in unique_companies:
            affected_by_company[company] = affected_by_company.get(company, 0) + 1

        # Check if the domain is exclusively hosted by a single company
        if len(unique_companies) == 1:
            company = next(iter(unique_companies))  # Get the single company hosting this domain
            exclusively_hosted_by_company[company] = exclusively_hosted_by_company.get(company, 0) + 1

    total_domains = len(data)
    percent_affected = {company: (count / total_domains) * 100 for company, count in affected_by_company.items()}
    percent_unreachable = {company: (count / total_domains) * 100 for company, count in exclusively_hosted_by_company.items()}

    return percent_affected, percent_unreachable
