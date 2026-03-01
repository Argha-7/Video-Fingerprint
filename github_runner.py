import os
import sys
from modify_fingerprint import download_youtube_video, process_video

def run_workflow():
    if len(sys.argv) < 2:
        print("Error: No video URL provided.")
        sys.exit(1)
        
    video_url = sys.argv[1]
    original_video = "original_video.mp4"
    modified_video = "modified_video.mp4"
    
    print(f"Starting workflow for: {video_url}")
    
    # Pre-cleanup
    for f in [original_video, modified_video, "temp_orig.mp3", "temp_new.mp3"]:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass
            
    try:
        actual_path = download_youtube_video(video_url, original_video)
        process_video(actual_path, modified_video)
        print("Workflow completed successfully.")
    except Exception as e:
        print(f"Workflow failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_workflow()
