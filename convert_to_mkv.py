import os
import subprocess
import argparse
import sys

def detect_gpu():
    try:
        nvidia_info = subprocess.check_output(["nvidia-smi", "-L"]).decode("utf-8")
        if "GPU" in nvidia_info:
            return "nvidia"
    except Exception:
        pass

    try:
        amd_info = subprocess.check_output(
            ["wmic", "path", "win32_VideoController", "get", "name"]
        ).decode("utf-8")
        if "AMD" in amd_info or "Radeon" in amd_info:
            return "amd"
    except Exception:
        pass

    return "cpu"

def check_ffmpeg():
    try:
        ffmpeg_version_info = subprocess.check_output(
            ["ffmpeg", "-version"], stderr=subprocess.STDOUT
        ).decode("utf-8")
        for line in ffmpeg_version_info.split("\n"):
            if "ffmpeg version" in line:
                return line
    except FileNotFoundError:
        return "FFmpeg not found in PATH"
    return "FFmpeg not found"

def get_original_bitrate(video_file):
    try:
        result = subprocess.check_output(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=bit_rate", "-of", "default=noprint_wrappers=1:nokey=1", video_file]
        ).decode("utf-8").strip()
        return f"{int(result) // 1000}k"
    except Exception as e:
        print(f"Error getting original bitrate: {e}")
        return None

parser = argparse.ArgumentParser(
    description="Convert video files to a specific format."
)
parser.add_argument(
    "-d",
    "--directory",
    type=str,
    required=True,
    help="Directory where the videos are located.",
)
parser.add_argument(
    "-i",
    "--input_formats",
    nargs="*",
    default=None,
    help="Input formats of the files to be converted (e.g., .mp4 .ts). If none are provided, all video files will be converted.",
)
parser.add_argument(
    "-o",
    "--output_format",
    type=str,
    default=".mkv",
    help="Output format of the converted files (default: .mkv).",
)
parser.add_argument(
    "-b",
    "--bitrate",
    type=str,
    default=None,
    help="Bitrate for the video (e.g., 600k). If not provided, the original bitrate is used.",
)
args = parser.parse_args()

ffmpeg_version = check_ffmpeg()
print(ffmpeg_version)

directory = args.directory

files_to_convert = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if not file.endswith(args.output_format):
            if args.input_formats is None or any(
                file.endswith(ext) for ext in args.input_formats
            ):
                files_to_convert.append(os.path.join(root, file))

total_files = len(files_to_convert)
print(f"Starting conversion of {total_files} files...")

gpu_type = detect_gpu()
print(f"Using {gpu_type.upper()} for processing.")

if gpu_type == "nvidia":
    video_encoder = "hevc_nvenc"
    preset = "slow"
elif gpu_type == "amd":
    video_encoder = "hevc_amf"
    preset = "slow"
else:
    video_encoder = "libx265"
    preset = "veryslow"

if total_files > 0:
    old_directory = os.path.join(directory, "old")
    if not os.path.exists(old_directory):
        os.mkdir(old_directory)

    for file in files_to_convert:
        full_name = file
        output_name = os.path.splitext(full_name)[0] + args.output_format
        print(f"Processing file: {os.path.basename(full_name)}")

        video_bitrate = args.bitrate if args.bitrate else get_original_bitrate(full_name)

        command = [
            "ffmpeg",
            "-i",
            full_name,
            "-c:v",
            video_encoder,
            "-b:v",
            video_bitrate,
            "-preset",
            preset,
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            output_name,
        ]
        print(f"Executed command: {' '.join(command)}")

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

        for line in process.stdout:
            print(line.strip())

        process.wait()
        print(f"\nFinished processing file: {os.path.basename(full_name)}")

        if os.path.getsize(output_name) == 0:
            print(f"Error: The file {output_name} was not created correctly.")
        else:
            old_local_directory = os.path.join(os.path.dirname(full_name), "old")
            if not os.path.exists(old_local_directory):
                os.mkdir(old_local_directory)

            os.rename(
                full_name, os.path.join(old_local_directory, os.path.basename(file))
            )

    print("Conversion completed!")
else:
    print("No files to convert found.")
