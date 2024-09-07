import os
import shutil

# 源文件夹路径
source_folder = "./interp/chair_1_spiralup_blink"
# 目标文件夹根路径
target_folder_root = "./interp/"

# 每个子文件夹包含的图像数
images_per_folder = 480

# 创建目标文件夹
for i in range(1, 61):
    target_folder = f"{target_folder_root}blink_{str(i).zfill(3)}"
    os.makedirs(target_folder, exist_ok=True)

# 移动图像到目标文件夹
count = 0
target_folder = None

for filename in sorted(os.listdir(source_folder)):
    if filename.endswith(".png"):
        count += 1
        if count == 1 or count % images_per_folder == 1:
            folder_index = (count - 1) // images_per_folder + 1
            target_folder = f"{target_folder_root}blink_{str(folder_index).zfill(3)}"
        source_path = os.path.join(source_folder, filename)
        target_path = os.path.join(target_folder, filename)
        shutil.move(source_path, target_path)

print("Done!")
