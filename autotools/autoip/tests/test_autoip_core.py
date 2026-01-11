import pytest
from unittest.mock import patch, Mock, MagicMock
from autotools.autoip.core import get_public_ip, get_local_ip, get_ip_info

# MOCK DATA FOR IP INFO RETRIEVAL
MOCK_IP_INFO = {
    'ip': '8.8.8.8',
    'city': 'Mountain View',
    'region': 'California',
    'country': 'US',
    'loc': '37.4056,-122.0775',
    'org': 'Google LLC',
    'timezone': 'America/Los_Angeles'
}

# UNIT TESTS

# TEST FOR PUBLIC IP RETRIEVAL
@patch('requests.get')
def test_get_public_ip(mock_get):
    mock_get.return_value.text = "1.2.3.4"
    ip = get_public_ip()
    assert ip == "1.2.3.4"
    mock_get.assert_called_once()

# TEST FOR LOCAL IP RETRIEVAL
@patch('socket.socket')
@patch('netifaces.gateways')
@patch('netifaces.ifaddresses')
def test_get_local_ip(mock_ifaddresses, mock_gateways, mock_socket):
    mock_gateways.return_value = {'default': {2: ('192.168.1.1', 'eth0')}}
    mock_ifaddresses.return_value = {2: [{'addr': '192.168.1.100'}]}
    ip = get_local_ip()
    assert ip == "192.168.1.100"

# TEST FOR IP INFO RETRIEVAL
@patch('requests.get')
def test_get_ip_info(mock_get):
    mock_get.return_value.json.return_value = MOCK_IP_INFO
    info = get_ip_info()
    assert isinstance(info, dict)
    assert info == MOCK_IP_INFO

# TEST FOR IP INFO WITH SPECIFIC IP
@patch('requests.get')
def test_get_ip_info_with_ip(mock_get):
    mock_get.return_value.json.return_value = MOCK_IP_INFO
    test_ip = "8.8.8.8"
    info = get_ip_info(test_ip)
    assert isinstance(info, dict)
    assert info['ip'] == test_ip
    assert 'Google' in info['org']

# TEST FOR IP INFO WITH INVALID IP
def test_get_ip_info_invalid():
    with pytest.raises(ValueError): get_ip_info("invalid.ip.address")

# TEST FOR IP INFO WITH PRIVATE IP
def test_get_ip_info_private():
    private_ips = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
    for ip in private_ips:
        with pytest.raises(ValueError): get_ip_info(ip)

# TEST FOR GET PUBLIC IP WITH FALLBACK
@patch('requests.get')
def test_get_public_ip_fallback(mock_get):
    import requests
    mock_get.side_effect = [ requests.RequestException("First service failed"), MagicMock(json=lambda: {'ip': '1.2.3.4'})]
    ip = get_public_ip()
    assert ip == "1.2.3.4"

# TEST FOR GET PUBLIC IP ALL FAIL
@patch('requests.get')
def test_get_public_ip_all_fail(mock_get):
    import requests
    mock_get.side_effect = requests.RequestException("All services failed")
    ip = get_public_ip()
    assert ip is None

# TEST FOR GET LOCAL IP WITH FALLBACK
@patch('socket.socket')
@patch('netifaces.gateways')
@patch('netifaces.ifaddresses')
def test_get_local_ip_fallback(mock_ifaddresses, mock_gateways, mock_socket):
    mock_gateways.side_effect = KeyError("No gateway")
    mock_socket_instance = MagicMock()
    mock_socket_instance.getsockname.return_value = ('192.168.1.100', 0)
    mock_socket.return_value = mock_socket_instance
    ip = get_local_ip()
    assert ip == "192.168.1.100"

# TEST FOR GET LOCAL IP ALL FAIL
@patch('socket.socket')
@patch('netifaces.gateways')
@patch('netifaces.ifaddresses')
def test_get_local_ip_all_fail(mock_ifaddresses, mock_gateways, mock_socket):
    mock_gateways.side_effect = KeyError("No gateway")
    mock_socket.side_effect = OSError("Socket error")
    ip = get_local_ip()
    assert ip is None

# TEST FOR GET IP INFO WITH ERROR IN RESPONSE
@patch('requests.get')
def test_get_ip_info_with_error(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {'error': 'Invalid IP'}
    mock_get.return_value = mock_response
    with pytest.raises(ValueError, match="Error getting IP info"): get_ip_info("8.8.8.8")

# TEST FOR GET IP INFO WITH REQUEST EXCEPTION
@patch('requests.get')
def test_get_ip_info_request_exception(mock_get):
    import requests
    mock_get.side_effect = requests.RequestException("Connection error")
    with pytest.raises(ValueError, match="Error connecting to IP info service"): get_ip_info("8.8.8.8")

# TEST FOR GET PUBLIC IPS WITH IPV4 FAILURE
@patch('requests.get')
def test_get_public_ips_ipv4_failure(mock_get):
    import requests
    from autotools.autoip.core import get_public_ips
    mock_get.side_effect = requests.RequestException("Service unavailable")
    ips = get_public_ips()
    assert ips['ipv4'] is None
    assert ips['ipv6'] is None

# TEST FOR GET PUBLIC IPS PARTIAL SUCCESS
@patch('requests.get')
def test_get_public_ips_partial_success(mock_get):
    import requests
    from autotools.autoip.core import get_public_ips

    def side_effect(*args, **kwargs):
        url = args[0]
        if 'api.ipify.org' in url or 'ipv4.icanhazip.com' in url or 'v4.ident.me' in url:
            mock = MagicMock()
            mock.text = "1.2.3.4"
            return mock
        raise requests.RequestException("Service unavailable")

    mock_get.side_effect = side_effect    
    ips = get_public_ips()
    assert ips['ipv4'] == "1.2.3.4"
    assert ips['ipv6'] is None

# TEST FOR GET PUBLIC IPS WITH EMPTY STRING
@patch('requests.get')
def test_get_public_ips_empty_string(mock_get):
    from autotools.autoip.core import get_public_ips
    mock_response = MagicMock()
    mock_text = MagicMock()
    mock_text.strip.return_value = ""
    mock_response.text = mock_text
    mock_get.return_value = mock_response
    ips = get_public_ips()
    assert ips['ipv4'] == ""

# TEST FOR GET PUBLIC IPS WITH IPV6 SUCCESS
@patch('requests.get')
def test_get_public_ips_ipv6_success(mock_get):
    import requests
    from autotools.autoip.core import get_public_ips

    def side_effect(*args, **kwargs):
        url = args[0]
        if 'api6.ipify.org' in url or 'ipv6.icanhazip.com' in url or 'v6.ident.me' in url:
            mock = MagicMock()
            mock.text = "2001:db8::1"
            return mock
        raise requests.RequestException("Service unavailable")

    mock_get.side_effect = side_effect
    ips = get_public_ips()
    assert ips['ipv4'] is None
    assert ips['ipv6'] == "2001:db8::1"

# TEST FOR GET LOCAL IPS
@patch('netifaces.interfaces')
@patch('netifaces.ifaddresses')
def test_get_local_ips(mock_ifaddresses, mock_interfaces):
    from autotools.autoip.core import get_local_ips
    mock_interfaces.return_value = ['eth0', 'lo']
    mock_ifaddresses.side_effect = [{2: [{'addr': '192.168.1.100'}], 30: [{'addr': 'fe80::1'}]}, {2: [{'addr': '127.0.0.1'}]}]
    ips = get_local_ips()
    assert '192.168.1.100' in ips['ipv4']
    assert '127.0.0.1' not in ips['ipv4']

# TEST FOR RUN SPEEDTEST FAILURE
@patch('speedtest.Speedtest')
def test_run_speedtest_failure(mock_speedtest):
    from autotools.autoip.core import run_speedtest
    mock_st = MagicMock()
    mock_st.get_best_server.side_effect = Exception("Speedtest error")
    mock_speedtest.return_value = mock_st
    result = run_speedtest()
    assert result is False

# TEST FOR RUN SPEEDTEST SUCCESS
@patch('speedtest.Speedtest')
def test_run_speedtest_success(mock_speedtest):
    from autotools.autoip.core import run_speedtest
    mock_st = MagicMock()
    mock_st.get_best_server.return_value = None
    mock_st.download.return_value = 50_000_000
    mock_st.upload.return_value = 10_000_000
    mock_st.results.ping = 20.5
    mock_speedtest.return_value = mock_st
    result = run_speedtest()
    assert result is True

# TEST FOR TEST CONNECTIVITY SUCCESS
@patch('socket.create_connection')
def test_test_connectivity_success(mock_connect):
    from autotools.autoip.core import test_connectivity
    mock_socket = MagicMock()
    mock_connect.return_value = mock_socket
    results = test_connectivity()
    assert len(results) == 5
    assert all(name in [r[0] for r in results] for name in ['Google DNS', 'CloudFlare DNS', 'Google', 'Cloudflare', 'GitHub'])

# TEST FOR TEST CONNECTIVITY FAILURE
@patch('socket.create_connection')
def test_test_connectivity_failure(mock_connect):
    from autotools.autoip.core import test_connectivity
    mock_connect.side_effect = OSError("Connection failed")
    results = test_connectivity()
    assert len(results) == 5
    assert all(not r[1] for r in results)

# TEST FOR RUN FUNCTION WITH VARIOUS OPTIONS
@patch('autotools.autoip.core._display_ip_addresses')
@patch('autotools.autoip.core._display_connectivity_tests')
@patch('autotools.autoip.core._display_location_info')
@patch('autotools.autoip.core._display_dns_servers')
@patch('autotools.autoip.core._display_ports_status')
@patch('autotools.autoip.core.run_speedtest')
def test_run_with_all_options(mock_speed, mock_ports, mock_dns, mock_location, mock_test, mock_ip):
    from autotools.autoip.core import run
    mock_speed.return_value = True
    run(test=True, speed=True, location=True, dns=True, ports=True, no_ip=False)
    assert mock_ip.called
    assert mock_test.called
    assert mock_location.called
    assert mock_dns.called
    assert mock_ports.called
    assert mock_speed.called

# TEST FOR RUN FUNCTION WITH NO IP
@patch('autotools.autoip.core._display_ip_addresses')
def test_run_with_no_ip(mock_ip):
    from autotools.autoip.core import run
    run(no_ip=True)
    assert not mock_ip.called

# TEST FOR DISPLAY IP ADDRESSES WITH NO IPV4
@patch('autotools.autoip.core.get_local_ips')
@patch('autotools.autoip.core.get_public_ips')
def test_display_ip_addresses_no_ipv4(mock_public, mock_local):
    from autotools.autoip.core import _display_ip_addresses
    mock_local.return_value = {'ipv4': [], 'ipv6': ['fe80::1']}
    mock_public.return_value = {'ipv4': None, 'ipv6': None}
    output = []
    _display_ip_addresses(output)
    assert "Not available" in "\n".join(output)

# TEST FOR DISPLAY IP ADDRESSES WITH NO IPV6
@patch('autotools.autoip.core.get_local_ips')
@patch('autotools.autoip.core.get_public_ips')
def test_display_ip_addresses_no_ipv6(mock_public, mock_local):
    from autotools.autoip.core import _display_ip_addresses
    mock_local.return_value = {'ipv4': ['192.168.1.100'], 'ipv6': []}
    mock_public.return_value = {'ipv4': '1.2.3.4', 'ipv6': None}
    output = []
    _display_ip_addresses(output)
    assert "IPv6: Not available" in "\n".join(output)

# TEST FOR DISPLAY LOCATION INFO WITH EXCEPTION
@patch('autotools.autoip.core.get_ip_info')
def test_display_location_info_exception(mock_get_info):
    from autotools.autoip.core import _display_location_info
    mock_get_info.side_effect = Exception("Location lookup failed")
    output = []
    _display_location_info(output)
    assert "Location lookup failed" in "\n".join(output)

# TEST FOR DISPLAY DNS SERVERS
@patch('builtins.open', create=True)
def test_display_dns_servers(mock_open):
    from autotools.autoip.core import _display_dns_servers
    mock_open.return_value.__enter__.return_value = ["nameserver 8.8.8.8\n", "nameserver 1.1.1.1\n", "# comment\n"]
    output = []
    _display_dns_servers(output)
    assert "8.8.8.8" in "\n".join(output)
    assert "1.1.1.1" in "\n".join(output)

# TEST FOR DISPLAY DNS SERVERS WITH ERROR
@patch('builtins.open', create=True)
def test_display_dns_servers_error(mock_open):
    from autotools.autoip.core import _display_dns_servers
    mock_open.side_effect = OSError("File not found")
    output = []
    _display_dns_servers(output)
    assert "Could not read DNS configuration" in "\n".join(output)

# TEST FOR DISPLAY PORTS STATUS
@patch('socket.socket')
def test_display_ports_status(mock_socket):
    from autotools.autoip.core import _display_ports_status
    mock_sock = MagicMock()
    mock_sock.connect_ex.return_value = 0
    mock_socket.return_value = mock_sock
    output = []
    _display_ports_status(output)
    assert "Common Ports Status" in "\n".join(output)
    assert "Port 80:" in "\n".join(output)

# TEST FOR MONITOR NETWORK TRAFFIC
@patch('time.sleep')
@patch('psutil.net_io_counters')
def test_monitor_network_traffic(mock_net_io, mock_sleep):
    from autotools.autoip.core import _monitor_network_traffic
    mock_io_counter = MagicMock(bytes_sent=1000, bytes_recv=2000)
    mock_net_io.return_value = mock_io_counter
    mock_sleep.side_effect = KeyboardInterrupt()
    output = []
    _monitor_network_traffic(output, 1)
    assert "Network Monitor" in "\n".join(output)
    assert "Monitoring stopped" in "\n".join(output)

# TEST FOR RUN FUNCTION WITH MONITOR
@patch('autotools.autoip.core._monitor_network_traffic')
def test_run_with_monitor(mock_monitor):
    from autotools.autoip.core import run
    run(monitor=True, interval=1, no_ip=True)
    assert mock_monitor.called

# TEST FOR RUN FUNCTION WITH SPEED TEST FAILURE
@patch('autotools.autoip.core.run_speedtest')
def test_run_with_speed_test_failure(mock_speed):
    from autotools.autoip.core import run
    mock_speed.return_value = False
    result = run(speed=True, no_ip=True)
    assert "Speed test failed" in result

# TEST FOR EXTRACT IPV4 ADDRESSES
def test_extract_ipv4_addresses():
    import netifaces
    from autotools.autoip.core import _extract_ipv4_addresses
    addrs = {netifaces.AF_INET: [{'addr': '192.168.1.100'}, {'addr': '127.0.0.1'}, {'addr': '10.0.0.1'}]}
    result = _extract_ipv4_addresses(addrs)
    assert '192.168.1.100' in result
    assert '10.0.0.1' in result
    assert '127.0.0.1' not in result

# TEST FOR EXTRACT IPV4 ADDRESSES NO AF_INET
def test_extract_ipv4_addresses_no_af_inet():
    from autotools.autoip.core import _extract_ipv4_addresses
    addrs = {}
    result = _extract_ipv4_addresses(addrs)
    assert result == []

# TEST FOR EXTRACT IPV6 ADDRESSES
def test_extract_ipv6_addresses():
    import netifaces
    from autotools.autoip.core import _extract_ipv6_addresses
    addrs = {netifaces.AF_INET6: [{'addr': '2001:db8::1'}, {'addr': 'fe80::1'}, {'addr': '2001:db8::2%eth0'}]}
    result = _extract_ipv6_addresses(addrs)
    assert '2001:db8::1' in result
    assert '2001:db8::2' in result
    assert 'fe80::1' not in result

# TEST FOR EXTRACT IPV6 ADDRESSES NO AF_INET6
def test_extract_ipv6_addresses_no_af_inet6():
    from autotools.autoip.core import _extract_ipv6_addresses
    addrs = {}
    result = _extract_ipv6_addresses(addrs)
    assert result == [] 
