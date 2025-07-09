import paramiko
import os

# === Configuration ===
hostname = "datashare.atmohub.kit.edu"
username = "corradini"
private_key_path = os.path.expanduser("~/.ssh/id_rsa_kit")
remote_dir = "TEAMx/Parsivel/COL"
local_dir = "/your/local/folder"  # <-- change this!

# Ensure local directory exists
os.makedirs(local_dir, exist_ok=True)

# Load private key
key = paramiko.RSAKey.from_private_key_file(private_key_path)

# Connect via SFTP
transport = paramiko.Transport((hostname, 22))
transport.connect(username=username, pkey=key)
sftp = paramiko.SFTPClient.from_transport(transport)

try:
    # Navigate to remote folder
    sftp.chdir(remote_dir)
    print(f"Connected to {remote_dir} on {hostname}")

    # List files
    file_list = sftp.listdir()
    print(f"Found {len(file_list)} files.")

    # Download each file
    for filename in file_list:
        remote_path = f"{remote_dir}/{filename}"
        local_path = os.path.join(local_dir, filename)

        print(f"Downloading {filename}...")
        sftp.get(filename, local_path)
        print(f"Saved to {local_path}")

finally:
    sftp.close()
    transport.close()
    print("Connection closed.")
