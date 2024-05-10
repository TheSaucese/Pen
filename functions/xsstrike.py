import subprocess
import re

def clean_output(output):
    # Remove ANSI escape codes
    clean_output = re.sub(r'\x1b\[[0-9;]*m', '', output)
    return clean_output

def run_xsstrike(url, crawl=False):
    # Construct the command
    command = ["./functions/xsstrike/xsstrike.py", "-u", url]
    if crawl:
        command.append("--crawl")

    try:
        # Execute the command
        output_bytes = subprocess.check_output(command, stderr=subprocess.STDOUT)
        # Decode the output bytes to string
        output = output_bytes.decode('utf-8')
        # Clean the output from ANSI escape codes
        clean_output_str = clean_output(output)
        return clean_output_str
    except subprocess.CalledProcessError as e:
        # Handle errors
        return f"Error: {e.output}"

# Example usage
#url = "https://brutelogic.com.br/xss.php"
#crawl = True
#result = run_xsstrike(url, crawl)
#print(result)
