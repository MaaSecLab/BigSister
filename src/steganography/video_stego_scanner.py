"""
video_stego_scanner.py

Video steganography through extraction of frames and individual scanning of each frame. 
Abnormal frames are flagged and if the number of flagged frames exceeds the threshold, 
the video is considered suspicious.
"""
#ffmpeg should be installed - write in readme
#additional tools to be implemented(binwalk, video metadata analysis)
#improve error handling
#testing to be done
#document

import os
import subprocess
from pathlib import Path
import tempfile   
import shutil  #fix?
from steganography.zsteg_scraper import run_zsteg  #check if works correctly
from steganography.steghide_scraper import SteghideScraper 


class VideoStegoScanner:
    def __init__(self, fps:float=3.0):
        self.fps=fps
        self.results={}

    def extract_frames(self, video_path:str) -> str:
        """
        Extracts frames from a video at a given frames per second (three) into a temporary directory.

        Arguments:
            video_path: Path to the input video file.

        Returns:
            tmpdir (str): Path to the temporary directory containing extracted frames.
        """
        video_path = str(video_path) #ensure compatibility
        temp_dir=tempfile.mkdtemp(prefix="video_frames_")

        print(f"[+] Extracting frames to: {temp_dir}")

        try:
            subprocess.run([
                "ffmpeg", "-i", video_path,
                "-vf", f"fps={self.fps}", f"{temp_dir}/frame_%04d.png",
                "-hide_banner", "-loglevel", "error"
            ], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Frame extraction failed: {e}")

        return temp_dir
    
    #TO DO: MAKE SUSPICIOUS LOGIC SMARTER, rn its only string matching
    def scan_frames(self, frame_dir:str) -> dict:
        """
        Scans each extracted frame for steganographic content using zsteg and steghide.

        Arguments:
            frame_dir: Directory containing extracted PNG frames.

        Returns:
            dict: Mapping of frame filename → {zsteg result, steghide result}
        """
        results={}

        for file in os.listdir(frame_dir):
            if not file.endswith(".png"):  #accept only png
                continue

            full_path = os.path.join(frame_dir, file)
            print(f"[*] Scanning frame: {file}")

            zsteg_result = run_zsteg(full_path)
            steghide_result = SteghideScraper().scrape(full_path)

            results[file] = {
                "zsteg": zsteg_result,
                "steghide": steghide_result
            }

        return results
        
    def scan_video(self, video_path: str, threshold: float = 0.05) -> dict:
        """
        The full pipeline to scan video for steganographic content.

        Arguments:
            video_path: Path to the input video file.
            threshold: Percentage of suspicious frames to flag video.

        Returns:
            dict with results, including:
                - 'suspicious' (boolean)
                - 'flagged_frames' (list)
                - 'total_frames' (int)
                - 'details' (dict of frame results)
        """
        temp_dir = self.extract_frames(video_path)
        try:
            results = self.scan_frames(temp_dir)
            total = len(results)
            flagged = []

            for frame, data in results.items():
                if ("detected" in data["zsteg"].lower()) or \
                    ("Steghide" in data["steghide"] and "data" in str(data["steghide"])):
                    flagged.append(frame)

            suspicious = len(flagged) / total > threshold if total else False

            return {
                "suspicious": suspicious,
                "flagged_frames": flagged,
                "total_frames": total,
                "details": results
            }
        finally:
            if "video_frames_" in temp_dir:
                print(f"[+] Cleaning up: {temp_dir}")
                shutil.rmtree(temp_dir)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scan video for hidden data in frames")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("-t", "--threshold", type=float, default=0.05, help="Suspicion threshold (0–1)")
    args = parser.parse_args()

    scanner = VideoStegoScanner()
    report = scanner.scan_video(args.video, threshold=args.threshold)

    print("\n🎯 Summary:")
    print("Suspicious:", report["suspicious"])
    print("Flagged frames:", len(report["flagged_frames"]), "/", report["total_frames"])

