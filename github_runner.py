import os
import sys
from modify_fingerprint import download_youtube_video, process_video

def run_workflow():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--vocal-mask", action="store_true")
    parser.add_argument("--harmonic-alter", action="store_true")
    args = parser.parse_args()
    
    video_url = args.url
    original_video = "original_video.mp4"
    modified_video = "modified_video.mp4"
    
    print(f"Starting workflow for: {video_url}")
    print(f"Bypass Options: Vocal Mask={args.vocal_mask}, Harmonic Alter={args.harmonic_alter}")
    
    # Pre-cleanup
    for f in [original_video, modified_video, "modified_audio.m4a", "temp_orig.m4a", "temp_new.m4a"]:
        if os.path.exists(f): 
            try: os.remove(f)
            except: pass
            
    try:
        actual_path = download_youtube_video(video_url, original_video)
        process_video(actual_path, modified_video, vocal_mask=args.vocal_mask, harmonic_alter=args.harmonic_alter)
        print("Workflow completed successfully.")
    except Exception as e:
        print(f"Workflow failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_workflow()
