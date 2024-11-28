import os
import subprocess

def combine_flows(folder_path, output_file):
    # try in tiemstamp order
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")

    files_to_combine = [
        os.path.join(folder_path, filename)
        for filename in os.listdir(folder_path)
        if filename.endswith('.flow')  
    ]
    input_files = " ".join(files_to_combine)
    output_file_path = os.path.join(folder_path, output_file)

    command = f"cat {input_files} > {output_file_path}"
    print(command)
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Combined flows saved to {output_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error combining flows: {e}")

def subtract_flows(file1, file2, output_file):
    pass


if __name__ == "__main__":
    print('running...')
    combine_flows('old_tests', 'combined2.flow')