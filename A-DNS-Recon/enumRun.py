import dns.resolver
import dns.reversename
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DNSLookup:
    @staticmethod
    def rev_look_up(ip_address):
        try:
            reverse_name = dns.reversename.from_address(ip_address)
            ptr_records = dns.resolver.resolve(reverse_name, 'PTR')
            logging.info(f"\nReverse DNS (PTR) Records for {ip_address}:")
            for record in ptr_records:
                logging.info(record.to_text())
        except dns.resolver.NoAnswer:
            logging.warning(f"No PTR records found for {ip_address}")
        except dns.resolver.NXDOMAIN:
            logging.error(f"Reverse DNS lookup failed for {ip_address}")
        except Exception as e:
            logging.error(f"Error performing reverse DNS lookup for {ip_address}: {e}")

    @staticmethod
    def get_records(domain, record_type):
        try:
            records = dns.resolver.resolve(domain, record_type)
            logging.info(f"\n{record_type} Records for {domain}:")
            for record in records:
                if record_type == "MX":
                    logging.info(f"Priority: {record.preference}, Mail Server: {record.exchange.to_text()}")
                else:
                    logging.info(record.to_text())
        except dns.resolver.NoAnswer:
            logging.warning(f"No {record_type} records found for {domain}")
        except dns.resolver.NXDOMAIN:
            logging.error(f"Domain {domain} does not exist!")
        except Exception as e:
            logging.error(f"Error retrieving {record_type} records for {domain}: {e}")

    @staticmethod
    def dns_enum(domain):
        logging.info(f"Performing DNS enumeration for: {domain}\n")
        for record_type in ["A", "MX", "NS", "TXT", "SOA", "CNAME", "AAAA", "SRV"]:
            DNSLookup.get_records(domain, record_type)

def is_valid_ip(ip):
    pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){3}$')
    return pattern.match(ip) is not None

def is_valid_domain(domain):
    pattern = re.compile(r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$')
    return pattern.match(domain) is not None

if __name__ == "__main__":
    domain = input("Enter the domain to enumerate: ")
    if is_valid_domain(domain):
        DNSLookup.dns_enum(domain)
    else:
        logging.error("Invalid domain format.")

    ip_address = input("Enter the IP address for reverse lookup: ")
    if is_valid_ip(ip_address):
        DNSLookup.rev_look_up(ip_address)
    else:
        logging