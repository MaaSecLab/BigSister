import subprocess
import os
import re
from collections import defaultdict

def to_wsl_path(win_path: str) -> str:
    r"""
    Convert a Windows path (e.g. C:\Users\User\...) to a WSL path (/mnt/c/Users/User/...)
    """
    win_path = os.path.abspath(win_path)
    drive, path_rest = os.path.splitdrive(win_path)
    drive_letter = drive.strip(":").lower()
    unix_path = path_rest.replace("\\", "/")
    return f"/mnt/{drive_letter}{unix_path}"



def run_zsteg(image_path: str) -> str:
    """
    Run zsteg via WSL on the provided image path and return filtered output.

    Args:
        image_path (str): Full Windows path to the image file (from GUI).

    Returns:
        str: Filtered output from zsteg or an appropriate error message.
    """
    try:
        # Locate script
        script_path_win = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runzsteg.sh")

        # Sanity checks
        if not os.path.exists(script_path_win):
            return f"❌ Error: Bash script not found:\n{script_path_win}"
        if not os.path.exists(image_path):
            return f"❌ Error: Image file not found:\n{image_path}"

        # Convert both paths to WSL format
        script_path_wsl = to_wsl_path(script_path_win)
        image_path_wsl = to_wsl_path(image_path)

        # Build and run WSL command
        cmd = ["wsl", "bash", script_path_wsl, image_path_wsl]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120  # Increased timeout
        )

        if result.returncode != 0:
            return f"❌ Error from zsteg:\n{result.stderr.strip() or 'Unknown error'}"

        raw_output = result.stdout.strip()
        if not raw_output:
            return "✅ Zsteg finished but returned no output."

        # Parse & group zsteg output
        return parse_and_group_zsteg(raw_output)

    except subprocess.TimeoutExpired:
        return "❌ Error: zsteg analysis timed out. Try a smaller image or check WSL status."
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"


def parse_and_group_zsteg(output: str) -> str:
    """
    Filter and group duplicate-looking zsteg lines.

    Args:
        output (str): Raw output from zsteg.

    Returns:
        str: Grouped summary of findings.
    """
    grouped = defaultdict(set)
    pattern = re.compile(r"^(.*?)\s+\.\.\s+(file|text):\s*(.+)$")
    unparsed_lines = []

    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        match = pattern.match(line)
        if match:
            channel = match.group(1).strip()
            content = match.group(3).strip()
            grouped[content].add(channel)
        else:
            unparsed_lines.append(line)

    if not grouped and not unparsed_lines:
        return "✅ Zsteg completed. No hidden content detected."

    result = []
    for content, channels in sorted(grouped.items()):
        sorted_channels = sorted(channels)
        result.append(f"🔹 Detected: {content}")
        result.append(f"   ↳ Found in: {', '.join(sorted_channels)}")
        result.append("")

    if unparsed_lines:
        result.append("🔸 Unparsed lines:")
        result.extend(unparsed_lines)

    return "\n".join(result).strip()
