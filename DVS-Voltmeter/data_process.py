import os
import argparse


def pre_process(folder_path):
    i = 0
    file_content = []
    file_list = os.listdir(folder_path)
    flie_list = file_list.sort()
    for filename in file_list:
        if filename.endswith('png') or filename.endswith('jpg'):
            file_path = os.path.join(folder_path, filename)

            timestamp = str(int((int(filename[-10:-4])-1) * 1e6 * 1 / 6e3 + 1000)).zfill(12)

            file_content.append(f"{file_path} {timestamp}\n")
            i += 1

    output_file_path = folder_path + '/info.txt'
    with open(output_file_path, 'w') as file:
        file.writelines(file_content)

    print(f"File '{output_file_path}' has been created")


if __name__ == '__main__':

    root_path = './data_samples/interp'

    '''for i in range(4, 27):
        root_path = './data_samples/interp/Cropped/sub' + str(i).zfill(2)'''
    '''for folder_name in os.listdir(root_path):
        if not folder_name.startswith('_'):
            pre_process(os.path.join(root_path, folder_name))
'''

    '''i = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('png') or filename.endswith('jpg'):
            file_path = os.path.join(folder_path, filename)
            timestamp = str(i * 16667 + 1000).zfill(12)
            file_content.append(f"{file_path} {timestamp}\n")
            i += 1

    output_file_path = folder_path + 'info.txt'
    with open(output_file_path, 'w') as file:
        file.writelines(file_content)

    print(f"File '{output_file_path}' has been created")'''
    parser = argparse.ArgumentParser(description='data path for synthetic.')
    parser.add_argument('--folder_path', '-path', type=str, default="../Synthetic_Data/lego_unblink/gs", help='folder path.')

    args = parser.parse_args()
    folder_path = args.folder_path

    pre_process(folder_path)

    
