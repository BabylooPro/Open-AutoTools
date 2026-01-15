import sys
import os
import re
from typing import Any

# ENSURE TEXT IS SAFE TO WRITE TO THE CURRENT STDOUT ENCODING
# SOME WINDOWS TERMINALS USE LEGACY ENCODINGS THAT CANNOT ENCODE CERTAIN CHARACTERS
def safe_text(text: Any) -> Any:
    if not isinstance(text, str): return text

    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"

    try:
        text.encode(encoding)
        return text
    except Exception:
        try: return text.encode(encoding, errors="replace").decode(encoding)
        except Exception: return text.encode("ascii", errors="replace").decode("ascii")

# DETECTS IF RUNNING IN A CI/CD ENVIRONMENT
def is_ci_environment():
    ci_vars = ['CI', 'GITHUB_ACTIONS', 'GITLAB_CI', 'JENKINS_URL', 'TRAVIS', 'CIRCLECI', 'APPVEYOR', 'BUILDKITE', 'TEAMCITY']
    return any(os.getenv(var) for var in ci_vars)

# MASKS IPV4 ADDRESSES (EXAMPLE: 192.168.1.1 -> xxx.xxx.xxx.xxx)
def mask_ipv4(ip: str) -> str:
    if not ip or not isinstance(ip, str): return ip
    parts = ip.split('.')
    if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts): return 'xxx.xxx.xxx.xxx'
    return ip

# MASKS IPV6 ADDRESSES (EXAMPLE: 2001:0db8::1 -> xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx)
def mask_ipv6(ip: str) -> str:
    if not ip or not isinstance(ip, str): return ip
    clean_ip = ip.split('%')[0]
    if ':' in clean_ip: return 'xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx'
    return ip

# MASKS ALL IP ADDRESSES IN A STRING
def mask_ips_in_text(text: str) -> str:
    if not isinstance(text, str): return text
    
    # MASK IPV4 ADDRESSES FIRST
    ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    text = re.sub(ipv4_pattern, lambda m: mask_ipv4(m.group()) if all(0 <= int(p) <= 255 for p in m.group().split('.')) else m.group(), text)
    
    # MASK IPV6 ADDRESSES - HANDLE ALL FORMATS INCLUDING COMPRESSED
    # COMPRESSED AT START: ::1, ::8a2e:370:7334
    ipv6_compressed_start = r'(?<![0-9a-fA-F:])::(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}(?![0-9a-fA-F:])'
    text = re.sub(ipv6_compressed_start, lambda m: mask_ipv6(m.group()), text)
    
    # COMPRESSED WITH :: IN MIDDLE: 2001:db8::1, 2001:db8::8a2e:370:7334
    # FLEXIBLE PATTERN: ANY NUMBER OF HEX GROUPS BEFORE ::, THEN ::, THEN ANY NUMBER AFTER
    ipv6_compressed_mid = r'(?<![0-9a-fA-F:])[0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4})+::[0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4})*(?![0-9a-fA-F:])'
    text = re.sub(ipv6_compressed_mid, lambda m: mask_ipv6(m.group()), text)
    
    # COMPRESSED AT END: 2001:db8::
    ipv6_compressed_end = r'(?<![0-9a-fA-F:])[0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4})+::(?![0-9a-fA-F:])'
    text = re.sub(ipv6_compressed_end, lambda m: mask_ipv6(m.group()), text)
    
    # FULL FORMAT: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
    ipv6_full = r'(?<![0-9a-fA-F:])(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}(?![0-9a-fA-F:])'
    text = re.sub(ipv6_full, lambda m: mask_ipv6(m.group()), text)
    
    return text

# MASKS SENSITIVE INFORMATION IN TEXT (IPS, LOCATION DATA, ETC.)
def mask_sensitive_info(text: str, mask_ips: bool = True) -> str:
    if not isinstance(text, str): return text    
    if mask_ips: text = mask_ips_in_text(text)
    coord_pattern = r'-?\d+\.\d+,-?\d+\.\d+'
    text = re.sub(coord_pattern, '[REDACTED]', text)
    return text
