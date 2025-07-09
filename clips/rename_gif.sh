#!/bin/bash

# Directory containing the .gif files
target_dir="/data/obs/campaigns/teamx/quicklooks/Xband_rittenhorn"

# Loop through all matching .gif files
for file in "$target_dir"/rittner_horn_cd_Meteor50DX-143_KIT-IMKTRO_*.gif; do
    # Extract the date (yyyymmdd) from filename
    filename=$(basename "$file")
    if [[ $filename =~ _([0-9]{8})\.gif$ ]]; then
        date="${BASH_REMATCH[1]}"
        new_name="${date}_xband_rittenhorn.gif"
        mv "$file" "$target_dir/$new_name"
        echo "Renamed $filename -> $new_name"
    else
        echo "Skipped: $filename (no matching date format)"
    fi
done
echo "Renaming completed."