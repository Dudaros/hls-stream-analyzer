import requests
from urllib.parse import urljoin
import re

class HLSAnalyzer:
    """
    A professional-grade analyzer for HLS (HTTP Live Streaming) manifests.
    Demonstrates handling of Adaptive Bitrate Streaming (ABS) logic.
    """
    def __init__(self, master_url):
        self.master_url = master_url
        self.raw_content = ""

    def analyze(self):
        print(f"--- HLS Analysis for: {self.master_url[:60]}... ---")
        try:
            r = requests.get(self.master_url, timeout=10)
            r.raise_for_status()
            self.raw_content = r.text
            
            # Step 1: Detect if it's actually a Master Manifest
            if "#EXT-X-STREAM-INF" not in self.raw_content:
                print("[!] This appears to be a Media Playlist (single resolution), not a Master Manifest.")
                return

            # Step 2: Extract Resolution, Bandwidth, and Path
            # This regex handles the standard HLS tag format
            pattern = re.compile(r'#EXT-X-STREAM-INF:.*BANDWIDTH=(\d+)(?:.*RESOLUTION=(\d+x\d+))?.*\n(.*?)$', re.MULTILINE)
            variants = pattern.findall(self.raw_content)

            print(f"{'RESOLUTION':<15} | {'BITRATE (Mbps)':<15} | {'FULL SOURCE URL'}")
            print("-" * 100)

            for bandwidth, res, path in variants:
                res_label = res if res else "Audio/Other"
                mbps = round(int(bandwidth) / 1_000_000, 2)
                
                # Logic: Convert relative paths to absolute URLs
                full_url = urljoin(self.master_url, path.strip())
                
                print(f"{res_label:<15} | {mbps:<15} | {full_url[:60]}...")

        except Exception as e:
            print(f"[ERROR] Failed to parse stream: {e}")

if __name__ == "__main__":
    # Test this with the .m3u8 link you found in your Network tab
    test_url = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
    analyzer = HLSAnalyzer(test_url)
    analyzer.analyze()
