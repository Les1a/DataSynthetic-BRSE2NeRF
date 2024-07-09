from PIL import Image
import numpy as np
import os
import argparse


def rename(input_folder):
    for file in os.listdir(input_folder):
        if len(file) <= 10 and not os.path.exists(os.path.join(input_folder, file.zfill(10))):
            os.rename(os.path.join(input_folder, file), os.path.join(input_folder, file.zfill(10)))

    '''import json

    # 读取JSON文件
    with open(input_folder.replace('train', 'transforms_train.json'), 'r') as json_file:
        data = json.load(json_file)

    # 遍历每个frame
    for frame in data['frames']:
        file_path = frame['file_path']
        if file_path.endswith('.png'):
            new_file_path = file_path.split('\\')[1].zfill(10)
            new_file_path = f'train\\{new_file_path}'

            # 更新file_path
            frame['file_path'] = new_file_path
    with open(input_folder.replace('train', 'transforms_train.json'), 'w') as json_file:
        json.dump(data, json_file, indent=4)
'''


def create_RS(input_folder):
    # 获取文件夹中的文件列表
    files = os.listdir(input_folder)
    output_folder = input_folder.replace('gs', 'rs')

    files.sort()
    total_images = len(files)

    first_image = Image.open(os.path.join(input_folder, files[0]))
    width, height = first_image.size
    images_per_row = height

    for i in range(int(total_images / images_per_row)):
        # 初始化一个空的列表，用于存储每行的像素数据
        row_pixels = []

        # 计算当前rolling shutter图片的起始和结束索引
        start_idx = i * images_per_row
        end_idx = (i + 1) * images_per_row

        if end_idx > total_images:
            end_idx = total_images

        for k in range(start_idx, end_idx):
            img = Image.open(os.path.join(input_folder, files[k]))

            # 获取第j行的像素
            row = img.crop((0, k - start_idx, width, k - start_idx + 1))

            row_pixels.append(row)

        # 创建一个新的图像，拼接每行的像素为一张新的图像
        new_image = Image.new('RGBA', (width, height))
        for l_idx, img in enumerate(row_pixels):
            new_image.paste(img, (0, l_idx))

        # 保存新的rolling shutter图片
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        new_image.save(os.path.join(output_folder, f'rs_{str(i + 1).zfill(3)}.png'))
        print(f'rs image {str(i + 1).zfill(3)} done!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gs path.')
    parser.add_argument('--input_gs', '-i', type=str, default="./room_2/gs", help='original gs file.')

    args = parser.parse_args()

    input_folder = args.input_gs

    rename(input_folder)
    create_RS(input_folder)
