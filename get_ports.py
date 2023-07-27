import subprocess

def get_open_ports(target_url):
    # Remove the "https://" or "http://" prefix from the target URL
    if target_url.startswith("https://"):
        target_url = target_url[len("https://"):]
    elif target_url.startswith("http://"):
        target_url = target_url[len("http://"):]

    try:
        # Run nmap command and capture the output
        nmap_command = ['nmap', target_url]
        result = subprocess.check_output(nmap_command, universal_newlines=True)

        # Parse the nmap output to extract open ports and services
        open_ports = {}
        for line in result.splitlines():
            if "tcp" in line and "open" in line:
                parts = line.split()
                port = parts[0].split("/")[0]
                service = parts[2]
                open_ports[port] = service

        return open_ports

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running nmap: {e}")
        return {}