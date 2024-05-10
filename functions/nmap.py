import subprocess
import sys

def run_nmap(target):
    try:
        # Define the nmap command
        nmap_command = ['sudo', 'nmap', '-sS', '-sV', '--script', 'vulners', target]

        # Execute the command
        print(f"Running Nmap scan on {target}...")
        result = subprocess.run(nmap_command, capture_output=True, text=True)

        # Print the output
        print("Nmap scan completed. Results:")
        print(result.stdout)
    except Exception as e:
        print(f"An error occurred: {e}")
