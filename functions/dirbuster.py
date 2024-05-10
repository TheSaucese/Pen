import subprocess

def run_feroxbuster(target_url):
    try:
        # Replace 'feroxbuster' with the actual command to run Feroxbuster on your system
        # Include any options or parameters as needed
        process = subprocess.Popen(['feroxbuster','--filter-status','404','--silent', '-u', target_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Capture stdout and stderr
        stdout, stderr = process.communicate()

        # Check for errors
        if process.returncode != 0:
            print("Error running Feroxbuster:")
            print(stderr)
        else:
            # Print Feroxbuster output
            print("Feroxbuster Output:")
            return stdout
    
    except FileNotFoundError:
        print("Feroxbuster not found. Make sure it is installed and accessible in your system path.")

# Example usage
#target_url = "http://example.com"
#run_feroxbuster(target_url)
