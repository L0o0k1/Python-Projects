import dns.resolver
# ===========================
# --> A Record
def dnsEnum(domain):
    print(f"Performing DNS enumeration for: {domain}\n")
    try: 
        aRec = dns.resolver.resolve(domain,'A')
        print("'A' Records: ")
        for record in aRec:
            print(record.to_text())
    except dns.resolver.NoAnswer:
        print("No A Record Found....")
    except dns.resolver.NXDOMAIN:
        print(f"Domain {domain} Does Not Exist!")
        return
    except Exception as e:
        print(f"Error Retriving A Record: {e}")
# ===========================
# --> MX Records
    try:
        mxRec = dns.resolver.resolve(domain,'MX')
        print("\nMX Records: ")
        for record in mxRec:
            print(f"Priority: {record.preference} Mail Server: {record.exchange.to_text()}")
    except dns.resolver.NoAnswer:
        print("No MX Records Found ...")
    except Exception as e:
        print(f"Error Retrieving MX records: {e}")
# ===========================
# --> NS Recors
    try:
        nsRec = dns.resolver.resolve(domain, 'NS')
        print("\nNS Records: ")
        for record in nsRec:
            print(record.to_text())
    except dns.resolver.NoAnswer:
        print("No NS records found")
    except Exception as e:
        print(f"Error Retrieving NS records: {e}")
# ===========================
# --> TXT Records
    try:
        txtRec = dns.resolver.resolve(domain, 'TXT')
        print("\nTXT Records: ")
        for record in txtRec:
            print(record.to_text())
    except dns.resolver.NoAnswer:
        print("No TXT records found ...")
    except Exception as e:
        print(f"Error Retrieving TXT records: {e}")
# ===========================
# --> SOA Records
    try:
        soaRec = dns.resolver.resolve(domain, 'SOA')
        print("\nSOA Records: ")
        for record in soaRec:
            print(record.to_text())
    except dns.resolver.NoAnswer:
        print("No SOA records found")
    except Exception as e:
        print(f"Error Retrieving SOA records: {e}")
# ===========================
# -->  CNAME Records
    try:
        cnameRec= dns.resolver.resolve(domain, 'CNAME')
        print("\nCNAME Records:")
        for record in cnameRec:
            print(record.to_text())
    except dns.resolver.NoAnswer:
        print("No CNAME records found")
    except Exception as e:
        print(f"Error retrieving CNAME records: {e}")

if __name__ == "__main__":
    domain = input("Enter the domain to enumerate: ")
    dnsEnum(domain)