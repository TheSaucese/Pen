import subprocess
import sys

def run_sqlmap(target):
    try:
        # Define the sqlmap command
        sqlmap_command = ['sqlmap', '-u', target, '--batch']

        # Execute the command
        print(f"Running sqlmap on {target}...")
        result = subprocess.run(sqlmap_command, capture_output=True, text=True)

        # Print the output
        print("sqlmap scan completed. Results:")
        print(result.stdout)
    except Exception as e:
        print(f"An error occurred: {e}")

run_sqlmap(target_url)
