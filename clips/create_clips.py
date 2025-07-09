import os
import subprocess
from PIL import Image

# Choose output format: "mp4" or "gif"
output_format = "mp4"  # ← Change to "gif" if you prefer GIFs

# Input and output paths
input_base_path = "/data/obs/campaigns/teamx/quicklooks/rittner_horn"
output_dir = "/data/obs/campaigns/teamx/quicklooks/Xband_rittenhorn"
os.makedirs(output_dir, exist_ok=True)

prefix = "rittner_horn_cd_Meteor50DX-143_KIT-IMKTRO_"
frame_duration_ms = 500
fps = 1000 // frame_duration_ms

for folder_name in sorted(os.listdir(input_base_path)):
    folder_path = os.path.join(input_base_path, folder_name)
    print(f"\n📂 Processing folder: {folder_path}")

    if not os.path.isdir(folder_path) or not (folder_name.isdigit() and len(folder_name) == 8):
        print(f"⚠️ Skipping: {folder_name}")
        continue

    matched_images = []
    for file_name in sorted(os.listdir(folder_path)):
        if file_name.startswith(prefix) and file_name.endswith(".png"):
            datetime_str = file_name[len(prefix):-4]
            if len(datetime_str) == 12 and datetime_str.isdigit():
                matched_images.append(file_name)

    if not matched_images:
        print(f"⚠️ No matching images in {folder_path}")
        continue

    print(f"📸 Found {len(matched_images)} matching images")

    if output_format == "gif":
        gif_filename = f"{folder_name}_xband_rittenhorn.gif"
        gif_path = os.path.join(output_dir, gif_filename)

        if os.path.exists(gif_path):
            print(f"🟡 GIF already exists, skipping: {gif_filename}")
            continue

        print(f"🎞️ Creating GIF: {gif_path}")
        frames = []
        for img_name in matched_images:
            img_path = os.path.join(folder_path, img_name)
            try:
                with Image.open(img_path) as im:
                    frames.append(im.convert("RGB"))
            except Exception as e:
                print(f"❌ Error loading {img_path}: {e}")

        if frames:
            try:
                frames[0].save(
                    gif_path,
                    save_all=True,
                    append_images=frames[1:],
                    duration=frame_duration_ms,
                    loop=0
                )
                print(f"✅ Created GIF: {gif_path}")
            except Exception as e:
                print(f"❌ Failed to save GIF: {e}")
        continue

    elif output_format == "mp4":
        # Create symlinked frames for ffmpeg
        temp_dir = os.path.join(folder_path, "ffmpeg_tmp")
        os.makedirs(temp_dir, exist_ok=True)

        for idx, img in enumerate(matched_images):
            src = os.path.join(folder_path, img)
            dst = os.path.join(temp_dir, f"frame_{idx:04d}.png")
            if not os.path.exists(dst):
                os.symlink(src, dst)

        mp4_filename = f"{folder_name}_xband_rittenhorn.mp4"
        mp4_path = os.path.join(output_dir, mp4_filename)

        if os.path.exists(mp4_path):
            print(f"🟡 MP4 already exists, skipping: {mp4_filename}")
        else:
            print(f"🎬 Creating MP4: {mp4_path}")
            try:
                subprocess.run([
                "ffmpeg",
                "-y",
                "-framerate", str(fps),
                "-i", os.path.join(temp_dir, "frame_%04d.png"),
                "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
                "-c:v", "libx264",
                "-preset", "slow",         # compression trade-off: slower = smaller file
                "-crf", "32",              # quality vs. file size (23 is default; try 28–30)
                "-pix_fmt", "yuv420p",
                "-movflags", "faststart",
                mp4_path
            ], check=True)
                print(f"✅ MP4 created at: {mp4_path}")
            except subprocess.CalledProcessError as e:
                print(f"❌ FFmpeg failed: {e}")

        # Clean up temp files
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)

    else:
        print(f"❌ Unknown output format: {output_format}")

#2366707

