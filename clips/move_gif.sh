#!/bin/bash

# Set base and destination paths
base_path="/data/obs/campaigns/teamx/quicklooks/rittner_horn"
dest_path="/data/obs/campaigns/teamx/quicklooks/Xband_rittenhorn"

# Create destination folder if it doesn't exist
mkdir -p "$dest_path"

# Loop over subdirectories with 8-digit date names
for dir in "$base_path"/*; do
    if [[ -d "$dir" && $(basename "$dir") =~ ^[0-9]{8}$ ]]; then
        # Find and move all .gif files to the destination folder
        find "$dir" -maxdepth 1 -type f -name '*.gif' -exec mv {} "$dest_path" \;
    fi
done

echo "All .gif files moved to $dest_path"
