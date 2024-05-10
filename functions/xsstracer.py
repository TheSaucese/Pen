#!/usr/bin/env python3

import socket
import sys
import http.client
from urllib.parse import urlparse

def test_http(target, path, port):
    result_string = ""
    buffer1 = f"TRACE {path} HTTP/1.1"
    buffer2 = "Test: <script>alert(1);</script>"
    buffer3 = f"Host: {target}"

    buffer4 = f"GET {path} HTTP/1.1"

    result_string += f"Testing HTTP on port {port}\n"
    result_string += "Cross-Site Tracer v1.3 \n"
    result_string += f"Target: {target}:{port}\n"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((target, port))
    s.settimeout(1.0)

    if result == 0:
        s.send((buffer1 + "\n").encode())
        s.send((buffer2 + "\n").encode())
        s.send((buffer3 + "\n\n").encode())
        data1 = s.recv(1024).decode()
        s.close()

        script = "alert"
        xframe = "X-Frame-Options"

        # TEST FOR XST
        if script.lower() in data1.lower():
            result_string += "Site vulnerable to Cross-Site Tracing!\n"
        else:
            result_string += "Site not vulnerable to Cross-Site Tracing!\n"

        # TEST FOR HOST HEADER INJECTION
        frame_inject = "crowdshield"
        buffer1 = f"GET {path} HTTP/1.1"
        buffer2 = "Host: http://crowdshield.com"

        s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s3.connect_ex((target, port))
        s3.settimeout(1.0)
        s3.send((buffer1 + "\n").encode())
        s3.send((buffer2 + "\n\n").encode())
        data3 = s3.recv(1024).decode()
        s3.close()

        if frame_inject.lower() in data3.lower():
            result_string += "Site vulnerable to Host Header Injection!\n"
        else:
            result_string += "Site not vulnerable to Host Header Injection!\n"

        # TEST FOR CLICKJACKING AND CFS
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s2.connect_ex((target, port))
        s2.settimeout(1.0)
        s2.send((buffer4 + "\n").encode())
        s2.send((buffer3 + "\n\n").encode())
        data2 = s2.recv(1024).decode()
        s2.close()

        if xframe.lower() in data2.lower():
            result_string += "Site not vulnerable to Cross-Frame Scripting!\n"
            result_string += "Site not vulnerable to Clickjacking!\n"
        else:
            result_string += "Site vulnerable to Cross-Frame Scripting!\n"
            result_string += "Site vulnerable to Clickjacking!\n"
    else:
        result_string += f"Port {port} is closed!\n"

    return result_string

def test_https(target, path, port):
    result_string = ""
    result_string += f"Testing HTTPS on port {port}\n"
    headers = {
        'User-Agent': 'XSS Tracer v1.3',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    try:
        conn = http.client.HTTPSConnection(target)
        conn.request("GET", path, "", headers)
        response = conn.getresponse()
        data = response.read().decode()

        result_string += f"Response: {response.status} {response.reason}\n"

        script = "alert"
        xframe = "X-Frame-Options"

        # TEST FOR XST
        if script.lower() in data.lower():
            result_string += "Site vulnerable to Cross-Site Tracing!\n"
        else:
            result_string += "Site not vulnerable to Cross-Site Tracing!\n"

        # TEST FOR HOST HEADER INJECTION
        frame_inject = "crowdshield"
        headers_injection = {
            'User-Agent': 'XSS Tracer',
            'Host': 'http://crowdshield.com'
        }

        conn.request("GET", path, "", headers_injection)
        response_injection = conn.getresponse()
        data_injection = response_injection.read().decode()

        if frame_inject.lower() in data_injection.lower():
            result_string += "Site vulnerable to Host Header Injection!\n"
        else:
            result_string += "Site not vulnerable to Host Header Injection!\n"

        # TEST FOR CLICKJACKING AND CFS
        conn.request("GET", path, "", headers)
        response_clickjack = conn.getresponse()
        data_clickjack = response_clickjack.read().decode()

        if xframe.lower() in data_clickjack.lower():
            result_string += "Site not vulnerable to Cross-Frame Scripting!\n"
            result_string += "Site not vulnerable to Clickjacking!\n"
        else:
            result_string += "Site vulnerable to Cross-Frame Scripting!\n"
            result_string += "Site vulnerable to Clickjacking!\n"

    except Exception as e:
        result_string += f"Error testing HTTPS: {e}\n"

    return result_string

def run_xsstracer(target):
    result_string = ""

    url = urlparse(target)
    target = url.hostname if url.hostname else target.split('/')[0]  # SET TARGET
    path = url.path if url.path else "/"  # SET PATH, default to root if not provided
    ports = [80, 443]  # HTTP and HTTPS ports

    for port in ports:
        if port == 443:
            result_string += test_https(target, path, port)
        else:
            result_string += test_http(target, path, port)

    print(result_string)
    return result_string

