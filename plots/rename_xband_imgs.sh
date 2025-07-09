#!/bin/bash

# Base directory to start search
base_dir="/data/obs/campaigns/teamx/quicklooks/rittner_horn"

# Find all matching PNG files with the incorrect IMTRO in the name
find "$base_dir" -type f -name "rittner_horn_cd_Meteor50DX-143_KIT-IMTRO_*.png" | while read -r old_file; do
    # Construct new filename by replacing IMTRO with IMKTRO
    new_file="${old_file/IMTRO/IMKTRO}"
    
    # Rename the file
    echo "Renaming:"
    echo "  $old_file"
    echo "    → $new_file"
    mv "$old_file" "$new_file"
done
