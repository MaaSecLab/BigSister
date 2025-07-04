import subprocess
import os
import shutil

def run_zsteg(image_path: str) -> str:
    """
    Run zsteg on the given image file and return the output.

    Args:
        image_path (str): Path to the image file to analyze.

    Returns:
        str: Output from zsteg command.
    """
    try:
        # Check if image file exists
        if not os.path.exists(image_path):
            return f"Error: Image file '{image_path}' not found"
        
        # Check if zsteg is installed
        if not shutil.which('zsteg'):
            return "Error: zsteg is not installed. Install with: gem install zsteg"
        
        # Get the absolute path to the shell script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, 'runzsteg.sh')
        
        # Check if the script exists
        if not os.path.exists(script_path):
            return f"Error: Script '{script_path}' not found"
        
        # Make sure the script is executable
        os.chmod(script_path, 0o755)
        
        # Run the shell script with the image path
        result = subprocess.run([script_path, image_path],
                                capture_output=True,
                                text=True,
                                timeout=60  # Add timeout to prevent hanging
                                )
        print(result)
        
        if result.returncode != 0:
            return f"Error: {result.stderr.strip() if result.stderr else 'Unknown error occurred'}"
        
        return result.stdout
        
    except subprocess.TimeoutExpired:
        return "Error: zsteg analysis timed out"
    except subprocess.CalledProcessError as e:
        return f"Error running zsteg: {e.stderr.strip() if e.stderr else str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Remove the hardcoded execution for modularity
output = run_zsteg('/home/lambda/Downloads/OSINT_Challenges/Hoot_Hoot/hoothoot.png')
print(output)