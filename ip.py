import subprocess
import socket

def get_website_info(target_url):
    try:
        # Get the IP address of the website using DNS lookup
        ip_address = socket.gethostbyname(target_url)

        # Get the server name and its IP address using the nslookup command
        result = subprocess.check_output(['nslookup', target_url], universal_newlines=True)

        server_start = result.find('Server:') + len('Server:')
        server_end = result.find('\n', server_start)
        server = result[server_start:server_end].strip()

        server_ip_start = result.find('Address:', server_end) + len('Address:')
        server_ip_end = result.find('\n', server_ip_start)
        server_ip = result[server_ip_start:server_ip_end].strip()

        return ip_address, server, server_ip

    except (socket.gaierror, subprocess.CalledProcessError) as e:
        print(f"Error occurred: {e}")
        return None, None, None

if __name__ == "__main__":
    target_url = input("Enter the target URL: ")
    ip_address, server, server_ip = get_website_info(target_url)

    if ip_address and server and server_ip:
        print(f"IP Address of {target_url}: {ip_address}")
        print(f"Server Name: {server}")
        print(f"Server IP Address: {server_ip}")
    else:
        print("Failed to retrieve website information.")