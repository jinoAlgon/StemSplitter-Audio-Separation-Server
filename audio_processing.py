import os
import zipfile
import io
import subprocess as sp
from pathlib import Path

def separate(input_path, output_path):
    
    model = "htdemucs"
    mp3 = True
    mp3_rate = 320
    float32 = False  # output as float32 wavs, unsused if 'mp3' is True.
    int24 = False    # output as int24 wavs, unused if 'mp3' is True.
    
    # Command to run the Audio separation
    cmd = ["python3", "-m", "demucs.separate", "-o", output_path, "-n", model]
    
    if mp3:
        cmd += ["--mp3", f"--mp3-bitrate={mp3_rate}"]
    if float32:
        cmd += ["--float32"]
    if int24:
        cmd += ["--int24"]
    
    cmd.append(input_path)  # input file to the command

    # Executing the command
    try:
        sp.run(cmd, check=True)
    except sp.CalledProcessError:
        raise RuntimeError("Command failed, something went wrong.")


def create_zip(output_path, base_filename):
    """
    Create a zip archive of all separated files and return it as an in-memory byte stream.
    """
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for root, _, files in os.walk(output_path):
            for file in files:
                full_file_path = os.path.join(root, file)
                print(f"Adding {full_file_path} to zip")  
                zf.write(full_file_path, arcname=os.path.relpath(full_file_path, output_path))
    memory_file.seek(0)
    return memory_file
