import subprocess
import os
import hashlib
import time

FFMPEG_PATH = "ffmpeg"

def download_youtube_video(url, output_path):
    print(f"--- Downloading Video ---")
    command = [
        'python', '-m', 'yt_dlp', 
        '--no-check-certificate',
        '--no-cache-dir',
        '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        '--extractor-args', 'youtube:player_client=android,web', 
        '--client-name', 'android',
        '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 
        '--merge-output-format', 'mp4', '--output', output_path, url
    ]
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, check=True)
    
    if os.path.exists(output_path):
        return os.path.abspath(output_path)
    
    import glob
    files = glob.glob(output_path + "*")
    if files:
        actual_path = os.path.abspath(files[0])
        print(f"Detected actual path: {actual_path}")
        return actual_path
    
    raise FileNotFoundError(f"Could not find downloaded video at {output_path}")

def get_file_hash(file_path):
    if not os.path.exists(file_path):
        return "NOT_FOUND"
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def process_video(video_path, output_video_path):
    abs_video = os.path.abspath(video_path)
    abs_output = os.path.abspath(output_video_path)
    abs_output_audio = os.path.abspath("modified_audio.mp3")
    temp_orig_audio = os.path.abspath("temp_orig.mp3")
    temp_new_audio = os.path.abspath("temp_new.mp3")
    log_file = os.path.abspath("ffmpeg_log.txt")

    try:
        with open(log_file, "w") as f_log:
            # 1. Extract baseline audio
            print(f"--- Step 1: Extracting Original Audio ---")
            subprocess.run([FFMPEG_PATH, '-y', '-i', abs_video, '-vn', '-acodec', 'libmp3lame', '-ab', '192k', temp_orig_audio], 
                           check=True, stdout=subprocess.DEVNULL, stderr=f_log)
            orig_hash = get_file_hash(temp_orig_audio)
            print(f"Original Audio Hash: {orig_hash}")

            # 2. Transform and Re-encode Video with Anti-Copyright Filters
            print(f"--- Step 2: Modifying Video & Audio (Extreme Bypass) ---")
            # Stronger Audio Filters:
            # - atempo=1.05: Speed up
            # - asetrate=44100*1.005,aresample=44100: Pitch shift
            # - chorus=0.5:0.9:50:0.4:0.25:2: Subtle chorus
            # - tremolo=f=3:d=0.1: Subtle volume modulation
            # - apulsator=hz=0.05:amount=0.03: Digital watermark (phase oscillation)
            # - firequalizer: High frequency digital noise
            # - volume='1.0+0.02*sin(2*PI*t/1)': Changes volume EVERY SECOND dynamically
            audio_filters = (
                'atempo=1.05,asetrate=44100*1.008,aresample=44100,'
                'chorus=0.5:0.9:50:0.4:0.25:2,tremolo=f=3:d=0.1,'
                'apulsator=hz=0.05:amount=0.03,'
                'firequalizer=gain="if(gt(f,15000),rd(1,5),0)",'
                'volume=\'1.0+0.02*sin(2*PI*t/1.0)\':eval=frame'
            )
            video_filters = 'scale=iw*1.05:-1,crop=iw/1.05:ih/1.05,eq=brightness=0.02:contrast=1.05'
            
            transform_cmd = [
                FFMPEG_PATH, '-y', '-i', abs_video,
                '-vf', video_filters,
                '-af', audio_filters,
                '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22',
                '-c:a', 'aac', '-b:a', '128k',
                abs_output
            ]
            subprocess.run(transform_cmd, check=True, stdout=subprocess.DEVNULL, stderr=f_log)

            # 3. Generate standalone modified MP3 with same extreme bypass
            print(f"--- Step 3: Generating Modified MP3 ---")
            audio_cmd = [
                FFMPEG_PATH, '-y', '-i', abs_video,
                '-vn', '-af', audio_filters,
                '-acodec', 'libmp3lame', '-ab', '192k',
                abs_output_audio
            ]
            subprocess.run(audio_cmd, check=True, stdout=subprocess.DEVNULL, stderr=f_log)

            # 4. Verify the change
            print(f"--- Step 4: Verifying Fingerprint Change ---")
            new_hash = get_file_hash(abs_output_audio)
            print(f"Modified Audio Hash: {new_hash}")

            if orig_hash != new_hash and new_hash != "NOT_FOUND":
                print("\n✅ Fingerprint changed successfully!")
                print(f"Original: {orig_hash}")
                print(f"New:      {new_hash}")
            else:
                print("\n⚠️ Fingerprint unchanged.")

    finally:
        # Cleanup
        for f in [temp_orig_audio, temp_new_audio, log_file]:
            if os.path.exists(f):
                try: os.remove(f)
                except: pass

def main():
    video_url = input("Enter YouTube video URL (or press Enter to use existing original_video.mp4): ")
    original_video_path = "original_video.mp4"
    modified_video_path = "modified_video.mp4"
    
    if video_url.strip():
        # If a URL is provided, we delete ALL old media files to prevent using old audio/video
        files_to_clean = [
            original_video_path, 
            modified_video_path, 
            "temp_orig.mp3", 
            "temp_new.mp3", 
            "original_audio.mp3",
            "modified_audio.mp3"
        ]
        for f in files_to_clean:
            if os.path.exists(f):
                print(f"Cleaning up previous file: {f}")
                try: os.remove(f)
                except: pass
                
        actual_video_path = download_youtube_video(video_url, original_video_path)
    else:
        if os.path.exists(original_video_path):
            actual_video_path = os.path.abspath(original_video_path)
            print(f"Using existing video: {actual_video_path}")
        else:
            print("Error: No URL provided and no existing original_video.mp4 found.")
            return
    
    process_video(actual_video_path, modified_video_path)

if __name__ == "__main__":
    main()
