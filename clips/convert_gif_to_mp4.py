import os
import subprocess

# Root directory containing GIFs
input_root = "/data/obs/campaigns/teamx/quicklooks/mtg_fci"

# Directory where MP4s will be saved
output_root = "/data/obs/campaigns/teamx/quicklooks/mtg_fci_mp4"
os.makedirs(output_root, exist_ok=True)

# Output video settings
output_fps = 10

for dirpath, _, filenames in os.walk(input_root):
    for filename in filenames:
        if filename.lower().endswith(".gif"):
            gif_path = os.path.join(dirpath, filename)

            # Get relative path from input_root and use it to build output path
            rel_path = os.path.relpath(dirpath, input_root)
            output_dir = os.path.join(output_root, rel_path)
            os.makedirs(output_dir, exist_ok=True)

            mp4_filename = os.path.splitext(filename)[0] + ".mp4"
            mp4_path = os.path.join(output_dir, mp4_filename)

            if os.path.exists(mp4_path):
                print(f"🔁 Skipping existing MP4: {mp4_path}")
                continue

            print(f"🎞️ Converting: {gif_path} -> {mp4_path}")

            try:
                subprocess.run([
                    "ffmpeg",
                    "-y",  # overwrite output if needed
                    "-i", gif_path,
                    "-vf", f"fps={output_fps},pad=ceil(iw/2)*2:ceil(ih/2)*2",  # even dimensions
                    "-c:v", "libx264",
                    "-preset", "slow",         # compression trade-off: slower = smaller file
                    "-crf", "32",
                    "-pix_fmt", "yuv420p",
                    "-movflags", "faststart",
                    mp4_path
                ], check=True)
                print(f"✅ Saved MP4: {mp4_path}")
            except subprocess.CalledProcessError as e:
                print(f"❌ FFmpeg failed for {gif_path}: {e}")


#nohup 2409340