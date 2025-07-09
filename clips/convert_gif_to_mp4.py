import os
from moviepy.editor import VideoFileClip

# Root directory containing GIFs (adjust as needed)
root_dir = "/data/obs/campaigns/teamx/quicklooks/Xband_rittenhorn"

# MP4 output settings
output_fps = 10  # Adjust if needed

# Recursively walk through the directory
for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.lower().endswith(".gif"):
            gif_path = os.path.join(dirpath, filename)
            mp4_filename = os.path.splitext(filename)[0] + ".mp4"
            mp4_path = os.path.join(dirpath, mp4_filename)

            # Skip if MP4 already exists
            if os.path.exists(mp4_path):
                print(f"🔁 Skipping existing MP4: {mp4_path}")
                continue

            try:
                print(f"🎞️ Converting: {gif_path} -> {mp4_path}")
                clip = VideoFileClip(gif_path)
                clip.write_videofile(mp4_path, fps=output_fps, codec='libx264', audio=False)
                clip.close()
                print(f"✅ Saved MP4: {mp4_path}")
            except Exception as e:
                print(f"❌ Failed to convert {gif_path}: {e}")
