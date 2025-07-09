# METFUTII Data Preparation Scripts

This repository contains scripts used for preparing data for the METFUTII course. The data originates from the TEAMx campaign and is processed to generate quicklooks, plots, and video clips.

## Repository Structure

- **download/**  
  Scripts for downloading TEAMx campaign data and generating quicklook images.

- **plots/**  
  Scripts to plot and visualize the quicklook images.

- **clips/**  
  Scripts to create video clips (GIF or MP4) from the quicklook images.

## Usage

Each folder contains scripts with instructions on how to run them. Generally, the workflow is:

1. Download and prepare data with scripts in `download_and_quicklooks`.
2. Visualize quicklook images using scripts in `plot_quicklooks`.
3. Generate video clips from images using scripts in `create_video_clips`.

## Requirements

- Python 3.x  
- [Pillow](https://python-pillow.org/) for image processing  
- [ffmpeg](https://ffmpeg.org/) installed for video creation  
- Additional Python libraries as specified in individual scripts

## Contact

For questions or issues, please contact the repository maintainer.

---
METFUTII Course | TEAMx Campaign Data Processing

## Environment Setup

This project uses a Conda environment. To recreate it:

```bash
conda env create -f environment.yml
conda activate quicklooks_downloader
