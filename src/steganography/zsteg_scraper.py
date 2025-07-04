import subprocess

def run_zsteg(image_path: str) -> str:
    """
    Run zsteg on the given image file and return the output.

    Args:
        image_path (str): Path to the image file to analyze.

    Returns:
        str: Output from zsteg command.
    """
    try:
        # Run zsteg command
        result = subprocess.run(['./run_zsteg.sh', image_path],
                                capture_output=True,
                                text=True,
                                check=True
                                )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running zsteg: {e.stderr.strip()}"

output = run_zsteg('path/to/your/image.png')
print(output)