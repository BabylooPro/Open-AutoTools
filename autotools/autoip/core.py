import socket
import requests
import json
import ipaddress
import netifaces
import time
import speedtest
import psutil

# EXTRACTS IPV4 ADDRESSES FROM INTERFACE ADDRESSES
def _extract_ipv4_addresses(addrs):
    ipv4_list = []
    if netifaces.AF_INET in addrs:
        for addr in addrs[netifaces.AF_INET]:
            if 'addr' in addr and not addr['addr'].startswith('127.'):
                ipv4_list.append(addr['addr'])
    return ipv4_list

# EXTRACTS IPV6 ADDRESSES FROM INTERFACE ADDRESSES
def _extract_ipv6_addresses(addrs):
    ipv6_list = []
    if netifaces.AF_INET6 in addrs:
        for addr in addrs[netifaces.AF_INET6]:
            if 'addr' in addr and not addr['addr'].startswith('fe80:'):
                clean_addr = addr['addr'].split('%')[0]
                ipv6_list.append(clean_addr)
    return ipv6_list

# RETRIEVES ALL LOCAL IP ADDRESSES (IPV4 AND IPV6) FROM NETWORK INTERFACES
def get_local_ips():
    ips = {'ipv4': [], 'ipv6': []}

    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        ips['ipv4'].extend(_extract_ipv4_addresses(addrs))
        ips['ipv6'].extend(_extract_ipv6_addresses(addrs))

    return ips

# RETRIEVES PUBLIC IP ADDRESSES (IPV4 AND IPV6) FROM EXTERNAL SERVICES
def get_public_ips():
    ips = {'ipv4': None, 'ipv6': None}
    ipv4_services = ['https://api.ipify.org', 'https://ipv4.icanhazip.com', 'https://v4.ident.me']
    ipv6_services = ['https://api6.ipify.org', 'https://ipv6.icanhazip.com', 'https://v6.ident.me']

    for service in ipv4_services:
        try:
            ips['ipv4'] = requests.get(service, timeout=2).text.strip()
            if ips['ipv4']: break
        except (requests.RequestException, requests.Timeout, requests.ConnectionError):
            continue
    
    for service in ipv6_services:
        try:
            ips['ipv6'] = requests.get(service, timeout=2).text.strip()
            if ips['ipv6']: break
        except (requests.RequestException, requests.Timeout, requests.ConnectionError):
            continue

    return ips

# TESTS NETWORK CONNECTIVITY TO COMMON HOSTS
def test_connectivity():
    results = []
    test_hosts = {
        'Google DNS': ('8.8.8.8', 53),
        'CloudFlare DNS': ('1.1.1.1', 53),
        'Google': ('google.com', 443),
        'Cloudflare': ('cloudflare.com', 443),
        'GitHub': ('github.com', 443),
    }

    for name, (host, port) in test_hosts.items():
        try:
            start = time.time()
            s = socket.create_connection((host, port), timeout=2)
            latency = round((time.time() - start) * 1000, 2)
            s.close()
            results.append((name, True, latency))
        except OSError:
            results.append((name, False, None))

    return results

# RUNS INTERNET SPEED TEST AND DISPLAYS RESULTS INCLUDING PING
def run_speedtest():
    print("\nRunning speed test (this may take a minute)...")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        print("Testing download speed...")
        download_speed = st.download() / 1_000_000 # CONVERT TO MBPS

        print("Testing upload speed...")
        upload_speed = st.upload() / 1_000_000 # CONVERT TO MBPS

        print("Testing ping...")
        ping = st.results.ping
        
        print("\nSpeed Test Results:")
        print(f"Download: {download_speed:.2f} Mbps")
        print(f"Upload: {upload_speed:.2f} Mbps")
        print(f"Ping: {ping:.0f} ms")
        
        return True
    except Exception as e:
        print(f"\nSpeed test failed: {str(e)}")
        return False

# GETS PUBLIC IP ADDRESS USING EXTERNAL API SERVICES
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except requests.RequestException:
        try:
            response = requests.get('https://api.ipapi.com/api/check')
            return response.json()['ip']
        except (requests.RequestException, KeyError, ValueError):
            return None

# GETS LOCAL IP ADDRESS OF DEFAULT NETWORK INTERFACE
def get_local_ip():
    try:
        gateways = netifaces.gateways()
        default_interface = gateways['default'][netifaces.AF_INET][1]
        addrs = netifaces.ifaddresses(default_interface)
        return addrs[netifaces.AF_INET][0]['addr']
    except (KeyError, IndexError, OSError):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except OSError:
            return None

# RETRIEVES DETAILED INFORMATION ABOUT AN IP ADDRESS
def get_ip_info(ip=None):
    if ip:
        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.is_private:
                raise ValueError("Cannot get info for private IP addresses")
        except ValueError as e:
            raise ValueError(f"Invalid IP address: {str(e)}")

    try:
        url = f'https://ipapi.co/{ip}/json' if ip else 'https://ipapi.co/json'
        response = requests.get(url)
        data = response.json()

        if 'error' in data: raise ValueError(f"Error getting IP info: {data['error']}")

        return data
    except requests.RequestException as e:
        raise ValueError(f"Error connecting to IP info service: {str(e)}")

# DISPLAYS LOCAL AND PUBLIC IP ADDRESSES
def _display_ip_addresses(output):
    local_ips = get_local_ips()
    public_ips = get_public_ips()
    output.append("\nLocal IPs:")

    if local_ips['ipv4']:
        for ip in local_ips['ipv4']: output.append(f"IPv4: {ip}")
    else:
        output.append("IPv4: Not available")
        
    if local_ips['ipv6']:
        for ip in local_ips['ipv6']: output.append(f"IPv6: {ip}")
    else:
        output.append("IPv6: Not available")
    
    output.append("\nPublic IPs:")
    output.append(f"IPv4: {public_ips['ipv4'] or 'Not available'}")
    output.append(f"IPv6: {public_ips['ipv6'] or 'Not available'}")

# DISPLAYS CONNECTIVITY TEST RESULTS
def _display_connectivity_tests(output):
    output.append("\nConnectivity Tests:")
    results = test_connectivity()
    for name, success, latency in results:
        status = f"OK {latency}ms" if success else "X Failed"
        output.append(f"{name:<15} {status}")

# DISPLAYS LOCATION INFORMATION
def _display_location_info(output):
    try:
        loc = get_ip_info()
        output.append("\nLocation Info:")
        output.append(f"City: {loc.get('city', 'Unknown')}")
        output.append(f"Region: {loc.get('region', 'Unknown')}")
        output.append(f"Country: {loc.get('country', 'Unknown')}")
        output.append(f"ISP: {loc.get('org', 'Unknown')}")
    except Exception as e:
        output.append(f"\nLocation lookup failed: {str(e)}")

# DISPLAYS DNS SERVER INFORMATION
def _display_dns_servers(output):
    output.append("\nDNS Servers:")
    try:
        with open('/etc/resolv.conf', 'r') as f:
            for line in f:
                if 'nameserver' in line: output.append(f"DNS: {line.split()[1]}")
    except OSError:
        output.append("Could not read DNS configuration")

# CHECKS AND DISPLAYS COMMON PORTS STATUS
def _display_ports_status(output):
    common_ports = [80, 443, 22, 21, 25, 3306]
    output.append("\nCommon Ports Status (localhost):")

    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        status = "Open" if result == 0 else "Closed"
        output.append(f"Port {port}: {status}")
        sock.close()

# MONITORS NETWORK TRAFFIC
def _monitor_network_traffic(output, interval):
    output.append("\nNetwork Monitor (Press Ctrl+C to stop):")
    try:
        prev_bytes_sent = psutil.net_io_counters().bytes_sent
        prev_bytes_recv = psutil.net_io_counters().bytes_recv

        while True:
            time.sleep(interval)
            bytes_sent = psutil.net_io_counters().bytes_sent
            bytes_recv = psutil.net_io_counters().bytes_recv

            upload_speed = (bytes_sent - prev_bytes_sent) / (1024 * interval)
            download_speed = (bytes_recv - prev_bytes_recv) / (1024 * interval)
            
            output.append(f"\rUp: {upload_speed:.2f} KB/s | Down: {download_speed:.2f} KB/s")
            
            prev_bytes_sent = bytes_sent
            prev_bytes_recv = bytes_recv

    except KeyboardInterrupt:
        output.append("\nMonitoring stopped")

# MAIN FUNCTION TO RUN NETWORK DIAGNOSTICS AND DISPLAY RESULTS
def run(test=False, speed=False, monitor=False, interval=1, ports=False, dns=False, location=False, no_ip=False):
    output = []

    if not no_ip: _display_ip_addresses(output)
    if test: _display_connectivity_tests(output)
    if location: _display_location_info(output)
    if dns: _display_dns_servers(output)
    if ports: _display_ports_status(output)
    if monitor: _monitor_network_traffic(output, interval)

    if speed:
        output.append("\nRunning speed test...")
        if run_speedtest(): output.append("Speed test completed successfully")
        else: output.append("Speed test failed")

    return "\n".join(output) 
