import subprocess
import os
import hashlib
import time

FFMPEG_PATH = "ffmpeg"

def download_youtube_video(url, output_path):
    print(f"--- Downloading Video ---")
    
    # Attempt 1: Aggressive Bypass (Best for GitHub Actions)
    command_bypass = [
        'python', '-m', 'yt_dlp', 
        '--no-check-certificate',
        '--no-cache-dir',
        '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        '--extractor-args', 'youtube:player_client=android,web', 
        '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 
        '--merge-output-format', 'mp4', '--output', output_path, url
    ]
    
    # Attempt 2: Simple/Compatible (Best for Local/Windows)
    command_simple = [
        'python', '-m', 'yt_dlp', 
        '--no-check-certificate',
        '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 
        '--merge-output-format', 'mp4', '--output', output_path, url
    ]
    
    try:
        print(f"Attempting download with bypass parameters...")
        subprocess.run(command_bypass, check=True)
    except subprocess.CalledProcessError:
        print(f"Bypass download failed. Retrying with simpler parameters...")
        subprocess.run(command_simple, check=True)
    
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

def process_video(video_path, output_video_path, vocal_mask=False, harmonic_alter=False):
    abs_video = os.path.abspath(video_path)
    abs_output = os.path.abspath(output_video_path)
    abs_output_audio = os.path.abspath("modified_audio.m4a")
    temp_orig_audio = os.path.abspath("temp_orig.m4a")
    temp_new_audio = os.path.abspath("temp_new.m4a")
    log_file = os.path.abspath("ffmpeg_log.txt")

    try:
        with open(log_file, "w") as f_log:
            # 1. Extract baseline audio
            print(f"--- Step 1: Extracting Original Audio ---")
            subprocess.run([FFMPEG_PATH, '-y', '-i', abs_video, '-vn', '-acodec', 'aac', '-ab', '192k', temp_orig_audio], 
                           check=True, stdout=subprocess.DEVNULL, stderr=f_log)
            orig_hash = get_file_hash(temp_orig_audio)
            print(f"Original Audio Hash: {orig_hash}")

            # 2. Transform and Re-encode Video with Anti-Copyright Filters
            print(f"--- Step 2: Modifying Video & Audio (Expert Bypass) ---")
            
            # Base filters (Safe Core 5% Shift)
            audio_filters = 'asetrate=44100*1.05,aresample=44100,atempo=1.05'
            
            # Optional: Harmonic Alteration (Low-frequency mutation)
            if harmonic_alter:
                print("   [+] Applying Harmonic Alteration (Voice Mutation)")
                audio_filters += ',equalizer=f=120:width_type=q:w=1:g=5,equalizer=f=3000:width_type=h:w=1000:g=3'
            
            # Optional: Vocal Masking (Subliminal distortion)
            if vocal_mask:
                print("   [+] Applying Vocal Masking (Anti-Transcription)")
                audio_filters += ',apulsator=hz=0.05:amount=0.1,vibrato=f=0.5:d=0.1'
            
            # Final touch for all: Subtle echo/compand
            audio_filters += ',aecho=0.8:0.88:20:0.1,compand=0.3|0.3:1|1:-90/-60|-60/-40|-40/-30|-20/-20:6:0:-90:0.2'
            
            video_filters = 'scale=iw/0.92:ih/0.92,crop=iw*0.92:ih*0.92,rotate=0.01,hue=s=1.05,eq=brightness=0.05:contrast=1.08,vignette=PI/8,noise=alls=2:allf=t+u'
            
            transform_cmd = [
                FFMPEG_PATH, '-y', '-i', abs_video,
                '-vf', video_filters,
                '-af', audio_filters,
                '-g', '60', # GOP Disturbance for binary mutation
                '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22',
                '-c:a', 'aac', '-b:a', '128k',
                abs_output
            ]
            subprocess.run(transform_cmd, check=True, stdout=subprocess.DEVNULL, stderr=f_log)

            # 3. Generate standalone modified audio
            print(f"--- Step 3: Generating Modified Audio ---")
            abs_output_audio = os.path.abspath("modified_audio.m4a")
            audio_cmd = [
                FFMPEG_PATH, '-y', '-i', abs_video,
                '-vn', '-af', audio_filters,
                '-acodec', 'aac', '-ab', '192k',
                abs_output_audio
            ]
            subprocess.run(audio_cmd, check=True, stdout=subprocess.DEVNULL, stderr=f_log)

            # 4. Inject Unique Metadata Jitter
            print(f"--- Step 4: Injecting Metadata Fingerprints ---")
            import uuid
            uid1, uid2, uid3 = str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())
            
            # For MP4
            final_video = abs_output.replace(".mp4", "_final.mp4")
            meta_cmd_v = [
                FFMPEG_PATH, '-y', '-i', abs_output,
                '-metadata', f'comment={uid1}',
                '-metadata', f'title={uid2}',
                '-metadata', f'artist={uid3}',
                '-c', 'copy', final_video
            ]
            subprocess.run(meta_cmd_v, check=True, stdout=subprocess.DEVNULL, stderr=f_log)
            os.replace(final_video, abs_output)
            
            # For M4A/AAC
            final_audio = abs_output_audio.replace(".m4a", "_final.m4a")
            meta_cmd_a = [
                FFMPEG_PATH, '-y', '-i', abs_output_audio,
                '-metadata', f'comment={uid1}',
                '-metadata', f'title={uid2}',
                '-metadata', f'artist={uid3}',
                '-c', 'copy', final_audio
            ]
            subprocess.run(meta_cmd_a, check=True, stdout=subprocess.DEVNULL, stderr=f_log)
            os.replace(final_audio, abs_output_audio)

            # 5. Verify
            print(f"--- Step 5: Verifying Hash Change ---")
            new_hash = get_file_hash(abs_output_audio)
            print(f"Modified Audio Hash: {new_hash}")

            if orig_hash != new_hash and new_hash != "NOT_FOUND":
                print("\n✅ Fingerprint changed successfully!")
                print(f"Original: {orig_hash}")
                print(f"New:      {new_hash}")
            else:
                print("\n⚠️ Hash verification failed.")

    finally:
        # Cleanup (Preserve log for debugging)
        for f in [temp_orig_audio, temp_new_audio]:
            if os.path.exists(f):
                try: os.remove(f)
                except: pass

def main():
    parser = argparse.ArgumentParser(description="Advanced Video Fingerprint Modifier")
    parser.add_argument("--url", help="YouTube Video URL")
    parser.add_argument("--vocal-mask", action="store_true", help="Apply subliminal vocal masking (Anti-Transcription)")
    parser.add_argument("--harmonic-alter", action="store_true", help="Apply harmonic tonal mutation (Voice DNA Change)")
    args = parser.parse_args()

    original_video_path = "original_video.mp4"
    modified_video_path = "modified_video.mp4"
    
    if args.url:
        # If a URL is provided, we delete ALL old media files to prevent using old audio/video
        files_to_clean = [
            original_video_path, 
            modified_video_path, 
            "temp_orig.m4a", 
            "temp_new.m4a", 
            "original_audio.m4a",
            "modified_audio.m4a",
            "modified_audio.mp3",
            "temp_orig.mp3"
        ]
        for f in files_to_clean:
            if os.path.exists(f):
                print(f"Cleaning up previous file: {f}")
                try: os.remove(f)
                except: pass
                
        actual_video_path = download_youtube_video(args.url, original_video_path)
    else:
        if os.path.exists(original_video_path):
            actual_video_path = os.path.abspath(original_video_path)
            print(f"Using existing video: {actual_video_path}")
        else:
            print("Error: No URL provided and no existing original_video.mp4 found.")
            return
    
    if os.path.exists(actual_video_path):
        process_video(actual_video_path, modified_video_path, vocal_mask=args.vocal_mask, harmonic_alter=args.harmonic_alter)
    else:
        print("❌ Error: Video file not found.")

if __name__ == "__main__":
    main()
