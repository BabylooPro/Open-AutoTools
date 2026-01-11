import socket
import requests
import json
import ipaddress
import netifaces
import time
import speedtest
import psutil

# RETRIEVES ALL LOCAL IP ADDRESSES (IPV4 AND IPV6) FROM NETWORK INTERFACES
def get_local_ips():
    ips = {'ipv4': [], 'ipv6': []}

    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)

        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                if 'addr' in addr and not addr['addr'].startswith('127.'):
                    ips['ipv4'].append(addr['addr'])

        if netifaces.AF_INET6 in addrs:
            for addr in addrs[netifaces.AF_INET6]:
                if 'addr' in addr and not addr['addr'].startswith('fe80:'):
                    clean_addr = addr['addr'].split('%')[0]
                    ips['ipv6'].append(clean_addr)

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
        except:
            continue
    
    for service in ipv6_services:
        try:
            ips['ipv6'] = requests.get(service, timeout=2).text.strip()
            if ips['ipv6']: break
        except:
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
        except:
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
        except:
            return None

# GETS LOCAL IP ADDRESS OF DEFAULT NETWORK INTERFACE
def get_local_ip():
    try:
        gateways = netifaces.gateways()
        default_interface = gateways['default'][netifaces.AF_INET][1]
        addrs = netifaces.ifaddresses(default_interface)
        return addrs[netifaces.AF_INET][0]['addr']
    except:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
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

# MAIN FUNCTION TO RUN NETWORK DIAGNOSTICS AND DISPLAY RESULTS
def run(test=False, speed=False, monitor=False, interval=1, ports=False, dns=False, location=False, no_ip=False):
    output = []

    # DISPLAYS LOCAL AND PUBLIC IP ADDRESSES (UNLESS NO_IP IS SET)
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

    # RUNS CONNECTIVITY TESTS IF TEST FLAG IS SET
    if test:
        output.append("\nConnectivity Tests:")
        results = test_connectivity()
        for name, success, latency in results:
            status = f"✓ {latency}ms" if success else "✗ Failed"
            output.append(f"{name:<15} {status}")

    # RUNS SPEED TEST IF SPEED FLAG IS SET
    if speed:
        output.append("\nRunning speed test...")
        if run_speedtest():
            output.append("Speed test completed successfully")
        else: output.append("Speed test failed")

    # SHOWS LOCATION INFO IF LOCATION FLAG IS SET
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

    # DISPLAYS DNS SERVERS IF DNS FLAG IS SET
    if dns:
        output.append("\nDNS Servers:")
        try:
            with open('/etc/resolv.conf', 'r') as f:
                for line in f:
                    if 'nameserver' in line:
                        output.append(f"DNS: {line.split()[1]}")
        except:
            output.append("Could not read DNS configuration")

    # CHECKS COMMON PORTS STATUS IF PORTS FLAG IS SET
    if ports:
        common_ports = [80, 443, 22, 21, 25, 3306]
        output.append("\nCommon Ports Status (localhost):")

        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            status = "Open" if result == 0 else "Closed"
            output.append(f"Port {port}: {status}")
            sock.close()

    # MONITORS NETWORK TRAFFIC IF MONITOR FLAG IS SET
    if monitor:
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

    return "\n".join(output) 
