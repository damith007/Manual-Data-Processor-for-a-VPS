import requests
import json
import zipfile
import io
import os
import re
import time
import sys

# Try to import libtorrent for actual downloading
try:
    import libtorrent as lt
except ImportError:
    print("Error: 'libtorrent' is not installed.")
    print("Please install it using: sudo apt install python3-libtorrent")
    lt = None

def download_torrent_content(torrent_source, save_path="."):
    """Uses libtorrent to download the actual files from a .torrent or magnet link."""
    if not lt:
        print("Skipping content download because libtorrent is missing.")
        return

    # Initialize session
    ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})
    
    if torrent_source.startswith('magnet:'):
        print("\nProcessing magnet link...")
        params = lt.parse_magnet_uri(torrent_source)
        params.save_path = save_path
        handle = ses.add_torrent(params)
    else:
        print(f"\nReading torrent file: {torrent_source}")
        info = lt.torrent_info(torrent_source)
        handle = ses.add_torrent({'ti': info, 'save_path': save_path})

    print(f"Starting download: {handle.status().name}")
    
    # Download loop
    try:
        while not handle.status().is_seeding:
            s = handle.status()
            state_str = ['queued', 'checking', 'downloading metadata', 
                         'downloading', 'finished', 'seeding', 'allocating']
            
            # Print progress to console
            progress = s.progress * 100
            out = f"\r{progress:.2f}% complete | Speed: {s.download_rate / 1000:.1f} kB/s | Peers: {s.num_peers} | Status: {state_str[s.state]}"
            sys.stdout.write(out)
            sys.stdout.flush()
            
            if s.state in [4, 5]: # Finished or Seeding
                break
                
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDownload stopped by user.")
        return
    
    print(f"\nDownload Complete! Files are in: {os.path.abspath(save_path)}")

def process_manual_data():
    print("==========================================")
    print("   Subz.lk Manual Data Processor (VPS)    ")
    print("==========================================")
    print("1. Copy the JSON response from your browser.")
    print("2. Right-click in PuTTY to paste.")
    print("3. Press ENTER, then press CTRL+D (Linux) to start.")
    print("------------------------------------------")
    
    # Reading multi-line input for the JSON block
    try:
        input_data = sys.stdin.read()
        if not input_data.strip():
            print("No data received.")
            return
        data = json.loads(input_data)
    except json.JSONDecodeError as e:
        print(f"\nError: Invalid JSON format. Make sure you copied the whole block.")
        print(f"Details: {e}")
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://subz.lk/'
    }

    try:
        # Check all possible keys for the torrent link
        torrent_url = data.get('torrent_720p') or data.get('torrent_link') or data.get('torrent_yts')
        sub_link = data.get('sinhala_sub_link')
        movie_title = data.get('title', 'movie').replace(" ", "_")
        
        # Clean title for folder naming
        movie_title = re.sub(r'[\\/*?:"<>|]', "", movie_title)

        # 1. Download and Extract Subtitles (Immediate)
        if sub_link:
            print(f"\n[1/3] Downloading Subtitles: {sub_link}")
            s_res = requests.get(sub_link, headers=headers, timeout=30)
            s_res.raise_for_status()
            with zipfile.ZipFile(io.BytesIO(s_res.content)) as z:
                for f in z.namelist():
                    if f.lower().endswith('.srt'):
                        filename = os.path.basename(f)
                        with z.open(f) as source, open(filename, "wb") as target:
                            target.write(source.read())
                        print(f"      Extracted: {filename}")

        # 2. Download/Prepare Torrent file
        torrent_path = None
        if torrent_url:
            print(f"[2/3] Preparing Torrent...")
            if torrent_url.startswith('magnet:'):
                torrent_path = torrent_url
            else:
                t_filename = f"{movie_title}.torrent"
                t_res = requests.get(torrent_url, headers=headers, timeout=30)
                with open(t_filename, 'wb') as f:
                    f.write(t_res.content)
                torrent_path = t_filename
                print(f"      Saved torrent file: {t_filename}")

        # 3. Start Content Download
        if torrent_path:
            print(f"[3/3] Starting BitTorrent download...")
            download_torrent_content(torrent_path)
        else:
            print("\nNo torrent link found in the provided JSON.")

    except Exception as e:
        print(f"\nAn error occurred during processing: {e}")

if __name__ == "__main__":
    process_manual_data()
