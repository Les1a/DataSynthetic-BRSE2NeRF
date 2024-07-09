import json
import os
import argparse


def update_file_path(json_data):
    for frame in json_data["frames"]:
        file_path = frame['file_path']
        if file_path.endswith('.png'):
            new_file_path = file_path.split('/')[1].zfill(10)
            new_file_path = f'train/{new_file_path}'

            # 更新file_path
            frame['file_path'] = new_file_path

        frame["file_path"] = frame["file_path"].replace("train", "gs")


def update_file_path_and_save(frames, output_folder):
    transformed_data = []

    for i, frame in enumerate(frames["frames"]):
        file_path = frame["file_path"]

        # 判断文件名数据是否除以480余1
        if (i+1) % 480 == 1:
            # 构建新的文件名和对应的 filepath
            new_file_name = f"rs_{i // 480 + 1:03d}.png"
            new_file_path = os.path.join('rs', new_file_name)

            # 创建新的帧数据，保持原有格式
            new_frame = {
                "file_path": new_file_path,
                "transform_matrix": frame["transform_matrix"]
            }

            # 添加到新的数据组
            transformed_data.append(new_frame)

    output_json_path = os.path.join(output_folder, "transforms_train_rs.json")
    with open(output_json_path, 'w') as output_json_file:
        json.dump({"camera_angle_x": frames["camera_angle_x"], "frames": transformed_data}, output_json_file, indent=4)


def run(path_ori, path_out):
    with open(path_ori, 'r') as json_file:
        data = json.load(json_file)

    update_file_path(data)

    with open(path_ori, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    with open(path_ori, 'r') as json_file:
        data = json.load(json_file)
    update_file_path_and_save(data, path_out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='json path.')
    parser.add_argument('--json_file_path', '-js', type=str, default="./lego_unblink_sample/transforms_train_gs.json", help='original JSON file.')
    parser.add_argument('--output_folder', '-o', type=str, default="./lego_unblink_sample", help='output folder.')

    args = parser.parse_args()

    json_file_path = args.json_file_path
    output_folder = args.output_folder

    run(json_file_path, output_folder)

    '''with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    update_file_path(data)

    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    update_file_path_and_save(data, output_folder)'''
