import os
import shutil


def move_files(src_dir, dest_dir, prefix, start_num, end_num):
    for i in range(start_num, end_num + 1):
        src_path = os.path.join(src_dir, f"{prefix}_{i:03d}")
        dest_path = dest_dir

        if os.path.exists(src_path):
            for root, dirs, files in os.walk(src_path):
                for file in files:
                    src_file_path = os.path.join(root, file)
                    dest_file_path = os.path.join(dest_path, file)
                    shutil.move(src_file_path, dest_file_path)
                    print(f"Moved {src_file_path} to {dest_file_path}")

            print(f"All files from {src_path} moved to {dest_path}")
        else:
            print(f"Source directory {src_path} not found.")


if __name__ == "__main__":
    src_directory = "./chair_1_spiralup_unblink/gs"
    dest_directory = "./chair_unblink/gs"
    prefix = "unblink"
    start_number = 1
    end_number = 60

    move_files(src_directory, dest_directory, prefix, start_number, end_number)
