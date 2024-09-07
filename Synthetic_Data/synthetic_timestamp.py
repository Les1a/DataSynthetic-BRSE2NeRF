import os
import argparse

def process_files_gs(folder_path):
    folder_path = folder_path + '/gs'
    # 获取文件夹下所有.png文件
    png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    png_files.sort()

    with open(os.path.join(folder_path, 'gs_timestamp_ns.txt'), 'w') as output_file:
        for png_file in png_files:
            # 构建文件的绝对路径
            file_path = os.path.join(folder_path, png_file)

            file_number = int(''.join(filter(str.isdigit, png_file)))

            new_number = int((file_number-1) * 1000 / 6 + 1000) * 1000
            formatted_number = '{:012d}'.format(new_number)

            # output_file.write(f"{file_path} {formatted_number}\n")
            output_file.write(f"{formatted_number}\n")


def process_files_rs(folder_path):
    folder_path = folder_path + '/rs'
    # 获取文件夹下所有.png文件
    png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    png_files.sort()

    with open(os.path.join(folder_path, 'rs_timestamp_ns.txt'), 'w') as output_file:
        for png_file in png_files:
            # 构建文件的绝对路径
            file_path = os.path.join(folder_path, png_file)

            file_number = int(''.join(filter(str.isdigit, png_file)))

            new_number = int((file_number-1)* 480 * 1000 / 6 + 1000) * 1000
            formatted_number = '{:012d}'.format(new_number)

            # output_file.write(f"{file_path} {formatted_number}\n")
            output_file.write(f"{formatted_number}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='folder path for timestamps.')
    parser.add_argument('--folder_path', '-path', type=str, default="./lego_unblink_sample", help='folder path.')

    args = parser.parse_args()
    folder_path = args.folder_path

    process_files_gs(folder_path)
    process_files_rs(folder_path)
