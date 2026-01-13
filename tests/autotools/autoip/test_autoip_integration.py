import pytest
from unittest.mock import patch, Mock
from click.testing import CliRunner
from autotools.cli import autoip

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

# INTEGRATION TESTS

# TEST FOR BASIC CLI FUNCTIONALITY
@patch('autotools.autoip.core.get_local_ips')
@patch('autotools.autoip.core.get_public_ips')
def test_autoip_cli_basic(mock_public_ips, mock_local_ips):
    mock_local_ips.return_value = {'ipv4': ['192.168.1.100'], 'ipv6': ['fe80::1']}
    mock_public_ips.return_value = {'ipv4': '1.2.3.4', 'ipv6': None}
    runner = CliRunner()
    result = runner.invoke(autoip)
    assert result.exit_code == 0
    assert "192.168.1.100" in result.output
    assert "1.2.3.4" in result.output
    assert "fe80::1" in result.output

# TEST FOR CONNECTIVITY TEST
@patch('autotools.autoip.core.test_connectivity')
def test_autoip_cli_test(mock_test):
    mock_test.return_value = [('Google DNS', True, 20), ('CloudFlare', False, None)]
    runner = CliRunner()
    result = runner.invoke(autoip, ['--test'])
    assert result.exit_code == 0
    assert "Google DNS" in result.output
    assert "CloudFlare" in result.output
    assert "OK 20ms" in result.output
    assert "X Failed" in result.output

# TEST FOR SPEED TEST
@patch('autotools.autoip.core.run_speedtest')
def test_autoip_cli_speed(mock_speed):
    mock_speed.return_value = True
    runner = CliRunner()
    result = runner.invoke(autoip, ['--speed'])
    assert result.exit_code == 0
    assert "Running speed test" in result.output
    assert "completed successfully" in result.output

# TEST FOR LOCATION INFO DISPLAY
@patch('autotools.autoip.core.get_ip_info')
def test_autoip_cli_location(mock_get_info):
    mock_get_info.return_value = MOCK_IP_INFO
    runner = CliRunner()
    result = runner.invoke(autoip, ['--location'])
    assert result.exit_code == 0
    assert "Mountain View" in result.output
    assert "California" in result.output
    assert "Google LLC" in result.output

# TEST FOR HELP DISPLAY
def test_autoip_cli_help():
    runner = CliRunner()
    result = runner.invoke(autoip, ['--help'])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output
    assert "--test" in result.output
    assert "--speed" in result.output
    assert "--location" in result.output 
