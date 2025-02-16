import socket
import requests
import json
import ipaddress
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

# GET PUBLIC IP ADDRESS USING IPIFY API
def get_public_ip():
    """GET PUBLIC IP ADDRESS USING IPIFY API"""
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except requests.RequestException:
        # FALLBACK TO ANOTHER SERVICE IF IPIFY FAILS
        try:
            response = requests.get('https://api.ipapi.com/api/check')
            return response.json()['ip']
        except:
            return None

# GET LOCAL IP ADDRESS
def get_local_ip():
    """GET LOCAL IP ADDRESS"""
    try:
        # GET DEFAULT INTERFACE
        gateways = netifaces.gateways()
        default_interface = gateways['default'][netifaces.AF_INET][1]
        
        # GET IP FROM DEFAULT INTERFACE
        addrs = netifaces.ifaddresses(default_interface)
        return addrs[netifaces.AF_INET][0]['addr']
    except:
        # FALLBACK METHOD
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return None

# GET IP INFORMATION USING IPAPI.CO
def get_ip_info(ip=None):
    """GET IP INFORMATION USING IPAPI.CO
    
    Args:
        ip (str, optional): IP address to get info for. If None, uses current IP.
        
    Returns:
        dict: Dictionary containing IP information
        
    Raises:
        ValueError: If IP is invalid or private
    """
    if ip:
        # VALIDATE IP
        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.is_private:
                raise ValueError("Cannot get info for private IP addresses")
        except ValueError as e:
            raise ValueError(f"Invalid IP address: {str(e)}")
    
    try:
        # USE IPAPI.CO FOR IP INFO
        url = f'https://ipapi.co/{ip}/json' if ip else 'https://ipapi.co/json'
        response = requests.get(url)
        data = response.json()
        
        if 'error' in data:
            raise ValueError(f"Error getting IP info: {data['error']}")
            
        return data
    except requests.RequestException as e:
        raise ValueError(f"Error connecting to IP info service: {str(e)}")

# MAIN FUNCTION TO RUN IP TOOLS
def run(test=False, speed=False, monitor=False, interval=1, ports=False, dns=False, location=False, no_ip=False):
    """MAIN FUNCTION TO RUN IP TOOLS
    
    Args:
        test (bool): Run connectivity tests
        speed (bool): Run speed test
        monitor (bool): Monitor network traffic
        interval (int): Monitoring interval in seconds
        ports (bool): Check common ports status
        dns (bool): Show DNS servers
        location (bool): Show IP location info
        no_ip (bool): Hide IP addresses
    """
    output = []
    
    # GET IP ADDRESSES IF NOT HIDDEN
    if not no_ip:
        local_ips = get_local_ips()
        public_ips = get_public_ips()
        
        output.append("\nLocal IPs:")
        if local_ips['ipv4']:
            for ip in local_ips['ipv4']:
                output.append(f"IPv4: {ip}")
        else:
            output.append("IPv4: Not available")
            
        if local_ips['ipv6']:
            for ip in local_ips['ipv6']:
                output.append(f"IPv6: {ip}")
        else:
            output.append("IPv6: Not available")
        
        output.append("\nPublic IPs:")
        output.append(f"IPv4: {public_ips['ipv4'] or 'Not available'}")
        output.append(f"IPv6: {public_ips['ipv6'] or 'Not available'}")

    # RUN CONNECTIVITY TESTS IF REQUESTED
    if test:
        output.append("\nConnectivity Tests:")
        results = test_connectivity()
        for name, success, latency in results:
            status = f"✓ {latency}ms" if success else "✗ Failed"
            output.append(f"{name:<15} {status}")
    
    # RUN SPEED TEST IF REQUESTED
    if speed:
        output.append("\nRunning speed test...")
        if run_speedtest():
            output.append("Speed test completed successfully")
        else:
            output.append("Speed test failed")
    
    # DISPLAY LOCATION INFO IF REQUESTED
    if location:
        try:
            loc = get_ip_info()
            output.append("\nLocation Info:")
            output.append(f"City: {loc.get('city', 'Unknown')}")
            output.append(f"Region: {loc.get('region', 'Unknown')}")
            output.append(f"Country: {loc.get('country', 'Unknown')}")
            output.append(f"ISP: {loc.get('org', 'Unknown')}")
        except Exception as e:
            output.append(f"\nLocation lookup failed: {str(e)}")

    # DISPLAY DNS SERVERS IF REQUESTED
    if dns:
        output.append("\nDNS Servers:")
        try:
            with open('/etc/resolv.conf', 'r') as f:
                for line in f:
                    if 'nameserver' in line:
                        output.append(f"DNS: {line.split()[1]}")
        except:
            output.append("Could not read DNS configuration")

    # CHECK COMMON PORTS IF REQUESTED
    if ports:
        common_ports = [80, 443, 22, 21, 25, 3306]
        output.append("\nCommon Ports Status (localhost):")
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            status = "Open" if result == 0 else "Closed"
            output.append(f"Port {port}: {status}")
            sock.close()

    # MONITOR NETWORK TRAFFIC IF REQUESTED
    if monitor:
        output.append("\nNetwork Monitor (Press Ctrl+C to stop):")
        try:
            prev_bytes_sent = psutil.net_io_counters().bytes_sent
            prev_bytes_recv = psutil.net_io_counters().bytes_recv
            while True:
                time.sleep(interval)
                bytes_sent = psutil.net_io_counters().bytes_sent
                bytes_recv = psutil.net_io_counters().bytes_recv
                
                # CALCULATE UPLOAD AND DOWNLOAD SPEEDS
                upload_speed = (bytes_sent - prev_bytes_sent) / (1024 * interval)
                download_speed = (bytes_recv - prev_bytes_recv) / (1024 * interval)
                
                output.append(f"\rUp: {upload_speed:.2f} KB/s | Down: {download_speed:.2f} KB/s")
                
                prev_bytes_sent = bytes_sent
                prev_bytes_recv = bytes_recv
        except KeyboardInterrupt:
            output.append("\nMonitoring stopped")
    
    return "\n".join(output) 
