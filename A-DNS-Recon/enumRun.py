import dns.resolver
import dns.reversename

def revLookUp(ip_address):
    try:
        reverse_name = dns.reversename.from_address(ip_address)
        ptr_records = dns.resolver.resolve(reverse_name, 'PTR')
        print(f"\nReverse DNS (PTR) Records for {ip_address}:")
        for record in ptr_records:
            print(record.to_text())
    except dns.resolver.NoAnswer:
        print(f"No PTR records found for {ip_address}")
    except dns.resolver.NXDOMAIN:
        print(f"Reverse DNS lookup failed for {ip_address}")
    except Exception as e:
        print(f"Error performing reverse DNS lookup for {ip_address}: {e}")

def getRecords(domain, record_type):
    try:
        records = dns.resolver.resolve(domain, record_type)
        print(f"\n{record_type} Records:")
        for record in records:
            if record_type == "MX":
                print(f"Priority: {record.preference}, Mail Server: {record.exchange.to_text()}")
            else:
                print(record.to_text())
    except dns.resolver.NoAnswer:
        print(f"No {record_type} records found")
    except dns.resolver.NXDOMAIN:
        print(f"Domain {domain} does not exist!")
    except Exception as e:
        print(f"Error retrieving {record_type} records: {e}")

def dnsEnum(domain):
    print(f"Performing DNS enumeration for: {domain}\n")
    for record_type in ["A", "MX", "NS", "TXT", "SOA", "CNAME"]:
        getRecords(domain, record_type)

if __name__ == "__main__":
    domain = input("Enter the domain to enumerate: ")
    dnsEnum(domain)
    ip_address = input("Enter the IP address for reverse lookup: ")
    revLookUp(ip_address)
