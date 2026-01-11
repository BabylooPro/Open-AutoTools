# AutoIP

## Description

Displays network information including IP addresses, connectivity tests, speed tests, and more. Uses multiple external services (ipify, icanhazip, ident.me) for reliable IP detection. Connectivity tests check latency to Google DNS, CloudFlare DNS, Google, Cloudflare, and GitHub.

## Usage

```bash
autoip
autoip --speed
autoip --location
autoip --no-ip --test --speed
```

## Options

-   `--test, -t`: Run connectivity tests to popular services
-   `--speed, -s`: Run internet speed test
-   `--monitor, -m`: Monitor real-time network traffic
-   `--interval, -i`: Monitoring interval in seconds (default: 1)
-   `--ports, -p`: Check status of common ports
-   `--dns, -d`: Show DNS server configuration
-   `--location, -l`: Show IP geolocation information
-   `--no-ip, -n`: Hide IP addresses display

## Features

-   Local and public IP detection (IPv4 & IPv6) from multiple network interfaces
-   Internet speed testing (download, upload, ping) using speedtest
-   Network connectivity checks with latency measurements (in milliseconds)
-   Real-time traffic monitoring (upload/download speeds in KB/s)
-   Port scanning for common ports (80, 443, 22, 21, 25, 3306)
-   DNS server information (reads from system configuration)
-   IP geolocation (city, region, country, ISP)
-   Monitoring can be stopped with Ctrl+C

## Compatibility

-   Windows 10/11 ✓
-   macOS 15+ ✓
-   Linux ✗

## Examples

```bash
# Display basic network information
autoip

# Run speed test
autoip --speed

# Show IP location
autoip --location

# Run connectivity tests without showing IPs
autoip --no-ip --test

# Monitor network traffic
autoip --monitor --interval 5

# Check DNS and ports
autoip --dns --ports
```
