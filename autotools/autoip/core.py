import socket
import requests
import netifaces
import time
import speedtest
import psutil

def get_local_ips():
    """GET LOCAL IPS"""
    ips = {'ipv4': [], 'ipv6': []} # INITIALIZE WITH EMPTY LISTS
    
    # GET LOCAL IPS
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        
        # GET IPV4
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                if 'addr' in addr and not addr['addr'].startswith('127.'):
                    ips['ipv4'].append(addr['addr'])
        
        # GET IPV6
        if netifaces.AF_INET6 in addrs:
            for addr in addrs[netifaces.AF_INET6]:
                if 'addr' in addr and not addr['addr'].startswith('fe80:'):
                    # REMOVE SCOPE ID IF PRESENT
                    clean_addr = addr['addr'].split('%')[0]
                    ips['ipv6'].append(clean_addr)
    
    return ips

def get_public_ips():
    """GET PUBLIC IPS"""
    ips = {'ipv4': None, 'ipv6': None} # INITIALIZE WITH NONE
    
    # TEST MULTIPLE IPV4 SERVICES
    ipv4_services = [
        'https://api.ipify.org',
        'https://ipv4.icanhazip.com',
        'https://v4.ident.me'
    ]
    
    # GET PUBLIC IPV4
    for service in ipv4_services:
        try:
            ips['ipv4'] = requests.get(service, timeout=2).text.strip()
            if ips['ipv4']: break
        except:
            continue
    
    # TEST MULTIPLE IPV6 SERVICES
    ipv6_services = [
        'https://api6.ipify.org',
        'https://ipv6.icanhazip.com',
        'https://v6.ident.me'
    ]
    
    # GET PUBLIC IPV6
    for service in ipv6_services:
        try:
            ips['ipv6'] = requests.get(service, timeout=2).text.strip()
            if ips['ipv6']: break
        except:
            continue

    return ips

# TEST CONNECTIVITY TO POPULAR SERVICES
def test_connectivity():
    """TEST CONNECTIVITY TO POPULAR SERVICES"""
    
    # TEST HOSTS
    test_hosts = {
        'Google DNS': ('8.8.8.8', 53),
        'CloudFlare DNS': ('1.1.1.1', 53),
        'Google': ('google.com', 443),
        'Cloudflare': ('cloudflare.com', 443),
        'GitHub': ('github.com', 443),
    }
    
    results = [] # INITIALIZE WITH EMPTY LIST
    
    # TEST EACH HOST
    for name, (host, port) in test_hosts.items():
        try:
            start = time.time()
            s = socket.create_connection((host, port), timeout=2)
            latency = round((time.time() - start) * 1000, 2)
            s.close()
            results.append((name, True, latency))
        except:
            results.append((name, False, None))
    
    return results

# RUN INTERNET SPEED TEST
def run_speedtest():
    """RUN INTERNET SPEED TEST"""
    print("\nRunning speed test (this may take a minute)...")
    
    # RUN SPEED TEST
    try:
        # GET BEST SERVER
        st = speedtest.Speedtest()
        st.get_best_server()
        
        # TEST DOWNLOAD
        print("Testing download speed...")
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        
        # TEST UPLOAD
        print("Testing upload speed...")
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        
        # GET PING
        ping = st.results.ping
        
        print("\nSpeed Test Results:")
        print(f"Download: {download_speed:.2f} Mbps")
        print(f"Upload: {upload_speed:.2f} Mbps")
        print(f"Ping: {ping:.0f} ms")
        
        return True
    except Exception as e:
        print(f"\nSpeed test failed: {str(e)}")
        return False

def run(test=False, speed=False, monitor=False, ports=False, dns=False, location=False, no_ip=False):
    """MAIN FUNCTION"""
    # GET LOCAL AND PUBLIC IPS
    local = get_local_ips()
    public = get_public_ips()
    
    # DISPLAY IPS IF NOT HIDDEN
    if not no_ip:
        print("\nLocal IPs:")
        if local['ipv4']:
            for ip in local['ipv4']:
                print(f"IPv4: {ip}")
        else:
            print("IPv4: Not available")
            
        if local['ipv6']:
            for ip in local['ipv6']:
                print(f"IPv6: {ip}")
        else:
            print("IPv6: Not available")
        
        print("\nPublic IPs:")
        print(f"IPv4: {public['ipv4'] or 'Not available'}")
        print(f"IPv6: {public['ipv6'] or 'Not available'}")

    # RUN CONNECTIVITY TESTS IF REQUESTED
    if test:
        print("\nConnectivity Tests:")
        results = test_connectivity()
        for name, success, latency in results:
            status = f"✓ {latency}ms" if success else "✗ Failed"
            print(f"{name:<15} {status}")
    
    # RUN SPEED TEST IF REQUESTED
    if speed:
        run_speedtest()
    
    # DISPLAY LOCATION INFO IF REQUESTED
    if location:
        try:
            loc = requests.get('https://ipapi.co/json/').json()
            print("\nLocation Info:")
            print(f"City: {loc.get('city', 'Unknown')}")
            print(f"Region: {loc.get('region', 'Unknown')}")
            print(f"Country: {loc.get('country_name', 'Unknown')}")
            print(f"ISP: {loc.get('org', 'Unknown')}")
        except:
            print("\nLocation lookup failed")

    # DISPLAY DNS SERVERS IF REQUESTED
    if dns:
        print("\nDNS Servers:")
        try:
            with open('/etc/resolv.conf', 'r') as f:
                for line in f:
                    if 'nameserver' in line:
                        print(f"DNS: {line.split()[1]}")
        except:
            print("Could not read DNS configuration")

    # CHECK COMMON PORTS IF REQUESTED
    if ports:
        common_ports = [80, 443, 22, 21, 25, 3306]
        print("\nCommon Ports Status (localhost):")
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            status = "Open" if result == 0 else "Closed"
            print(f"Port {port}: {status}")
            sock.close()

    # MONITOR NETWORK TRAFFIC IF REQUESTED
    if monitor:
        print("\nNetwork Monitor (Press Ctrl+C to stop):")
        try:
            prev_bytes_sent = psutil.net_io_counters().bytes_sent
            prev_bytes_recv = psutil.net_io_counters().bytes_recv
            while True:
                time.sleep(1)
                bytes_sent = psutil.net_io_counters().bytes_sent
                bytes_recv = psutil.net_io_counters().bytes_recv
                
                upload_speed = (bytes_sent - prev_bytes_sent) / 1024  # KB/s
                download_speed = (bytes_recv - prev_bytes_recv) / 1024  # KB/s
                
                print(f"\rUp: {upload_speed:.2f} KB/s | Down: {download_speed:.2f} KB/s", end='')
                
                prev_bytes_sent = bytes_sent
                prev_bytes_recv = bytes_recv
        except KeyboardInterrupt:
            print("\nMonitoring stopped") 
