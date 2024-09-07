#!/bin/bash

# 步骤1：确定处理的blender模型 确定运行目录
echo "Step 1: Generating "
file_name=${1:-"tanabata_rgb"}
cd /mnt/sdb/kjxia/syn
echo "Step 1 completed, processing ${file_name}"

# 步骤2：移动imgs和poses至指定目录
echo "Step 2: Moving imgs and poses to the specified directory..."
# mkdir "./Synthetic_Data/${file_name}"
if mv "../blender_outputs/${file_name}" "./Synthetic_Data/" &&
   mv "./Synthetic_Data/${file_name}/train/" "./Synthetic_Data/${file_name}/gs/" &&
   mv "./Synthetic_Data/${file_name}/transforms_train.json" "./Synthetic_Data/${file_name}/transforms_train_gs.json"; then
    echo "Step 2 completed."
else
    echo "Step 2 failed. Exiting."
    exit 1
fi

# 步骤3：创建rs并保存至sample/rs
echo "Step 3: Creating rs and saving to sample/rs..."
if python3 "./Synthetic_Data/create_RS.py" -i "./Synthetic_Data/${file_name}/gs"; then
    echo "Step 3 completed."
else
    echo "Step 3 failed. Exiting."
    exit 1
fi

# 步骤4：整合json_path，处理gspose，生成rspose保存至sample
echo "Step 4: Integrating json_path, processing gspose, and saving to sample..."
if python3 "./Synthetic_Data/json_path.py" -js "./Synthetic_Data/${file_name}/transforms_train_gs.json" -o "./Synthetic_Data/${file_name}"; then
    echo "Step 4 completed."
else
    echo "Step 4 failed. Exiting."
    exit 1
fi

# 步骤5：生成gs、rs时间戳保存至sample/gs和sample/rs
echo "Step 5: Generating gs, rs timestamps and saving to sample/gs and sample/rs..."
if python3 "./Synthetic_Data/synthetic_timestamp.py" -path "./Synthetic_Data/${file_name}"; then
    echo "Step 5 completed."
else
    echo "Step 5 failed. Exiting."
    exit 1
fi

# 步骤6：生成gs info保存至sample/gs
echo "Step 6: Generating gs info and saving to sample/gs..."
if python3 "./DVS-Voltmeter/data_process.py" -path "./Synthetic_Data/${file_name}/gs"; then
    echo "Step 6 completed."
else
    echo "Step 6 failed. Exiting."
    exit 1
fi

# 步骤7：读取sample/gs图片，events.txt保存至sample/events
echo "Step 7: Reading gs images and saving events.txt to sample/events..."
if python3 "./DVS-Voltmeter/main.py" --input_dir "./Synthetic_Data/${file_name}/gs" --output_dir "./Synthetic_Data/${file_name}/events" --process_model 1; then
    echo "Step 7 completed."
else
    echo "Step 7 failed. Exiting."
    exit 1
fi

# 步骤8：event可视化
echo "Step 8: event visualization"
if python3 "./Synthetic_Data/gen_vid.py" -ev "./Synthetic_Data/${file_name}/events" -m 1; then
    echo "Step 8 completed."
else
    echo "Step 8 failed. Exiting."
    exit 1
fi

# 步骤9：event的txt文件转npy
echo "Step 9: converting txt to npy"
if python3 "./Synthetic_Data/cvt_txt2npy.py" -ev "./Synthetic_Data/${file_name}/events"; then
    echo "Step 9 completed."
else
    echo "Step 9 failed. Exiting."
    exit 1
fi

# 步骤10：生成rs_blur
echo "Step 10: Reading gs images and generate blurring rs images"
if python3 "./Synthetic_Data/blurring_rs.py" -i "./Synthetic_Data/${file_name}/gs" -o "./Synthetic_Data/${file_name}/rs_blur" --blur_latency 200; then
    echo "Step 10 completed."
else
    echo "Step 10 failed. Exiting."
    exit 1
fi

# 所有步骤完成
echo "All steps completed successfully."
