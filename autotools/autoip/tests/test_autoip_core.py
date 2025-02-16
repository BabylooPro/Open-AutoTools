import pytest
from unittest.mock import patch, Mock
from autotools.autoip.core import get_public_ip, get_local_ip, get_ip_info

# MOCK DATA
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
    """TEST PUBLIC IP RETRIEVAL"""
    mock_get.return_value.text = "1.2.3.4"
    ip = get_public_ip()
    assert ip == "1.2.3.4"
    mock_get.assert_called_once()

# TEST FOR LOCAL IP RETRIEVAL
@patch('socket.socket')
@patch('netifaces.gateways')
@patch('netifaces.ifaddresses')
def test_get_local_ip(mock_ifaddresses, mock_gateways, mock_socket):
    """TEST LOCAL IP RETRIEVAL"""
    # MOCK NETIFACES
    mock_gateways.return_value = {'default': {2: ('192.168.1.1', 'eth0')}}
    mock_ifaddresses.return_value = {2: [{'addr': '192.168.1.100'}]}
    
    ip = get_local_ip()
    assert ip == "192.168.1.100"

# TEST FOR IP INFO RETRIEVAL
@patch('requests.get')
def test_get_ip_info(mock_get):
    """TEST IP INFO RETRIEVAL"""
    mock_get.return_value.json.return_value = MOCK_IP_INFO
    info = get_ip_info()
    assert isinstance(info, dict)
    assert info == MOCK_IP_INFO

# TEST FOR IP INFO WITH SPECIFIC IP
@patch('requests.get')
def test_get_ip_info_with_ip(mock_get):
    """TEST IP INFO WITH SPECIFIC IP"""
    mock_get.return_value.json.return_value = MOCK_IP_INFO
    test_ip = "8.8.8.8"  # GOOGLE DNS
    info = get_ip_info(test_ip)
    assert isinstance(info, dict)
    assert info['ip'] == test_ip
    assert 'Google' in info['org']

# TEST FOR IP INFO WITH INVALID IP
def test_get_ip_info_invalid():
    """TEST IP INFO WITH INVALID IP"""
    with pytest.raises(ValueError):
        get_ip_info("invalid.ip.address")

# TEST FOR IP INFO WITH PRIVATE IP
def test_get_ip_info_private():
    """TEST IP INFO WITH PRIVATE IP"""
    private_ips = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
    for ip in private_ips:
        with pytest.raises(ValueError):
            get_ip_info(ip) 
