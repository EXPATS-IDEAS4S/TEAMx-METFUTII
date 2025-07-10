import paramiko
import os

from credentials_kit import hostname, username, private_key_path
# === Configuration ===

remote_dir = "TEAMx/Parsivel/NER" #COL or NET
local_dir = "/data/obs/campaigns/teamx/lagonero/parsivel/unsorted"

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

    # List remote files
    file_list = sftp.listdir()
    print(f"Found {len(file_list)} files on remote server.")
    print(file_list)

    #filter the list to take only files that start with  'PARS2020L25'
    file_list = [f for f in file_list if f.startswith('PARS2020M25')]
    if not file_list:
        print("No files found that match the criteria.")
        sftp.close()
        transport.close()
        print("Connection closed.")

    # Download only missing files
    for filename in file_list:
        local_path = os.path.join(local_dir, filename)

        if os.path.exists(local_path):
            print(f"Skipping {filename} (already exists).")
            continue

        print(f"Downloading {filename}...")
        sftp.get(filename, local_path)
        print(f"Saved to {local_path}")

finally:
    sftp.close()
    transport.close()
    print("Connection closed.")
