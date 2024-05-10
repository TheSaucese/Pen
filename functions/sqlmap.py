import subprocess

def run_sqlmap(target_url):
    try:
        # Replace 'sqlmap' with the actual command to run SQLMap on your system
        # Include any options or parameters as needed
        process = subprocess.Popen(['sqlmap', '-u', target_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Capture stdout and stderr
        stdout, stderr = process.communicate()

        # Check for errors
        if process.returncode != 0:
            print("Error running SQLMap:")
            print(stderr)
        else:
            # Print SQLMap output
            print("SQLMap Output:")
            print(stdout)
            return stdout
    
    except FileNotFoundError:
        print("SQLMap not found. Make sure it is installed and accessible in your system path.")

# Example usage
target_url = "http://10.10.68.98/"
run_sqlmap(target_url)
