# DataSynthetic-BRSE2NeRF

## Run
After blender generation, you can change the default value of `file_name` in `gen_syn_data.sh` according to the name of blender data. 

Next, open a terminal to run `bash gen_syn_data.sh ordered_name`.

The `ordered_name` parameter influences `file_name`, and if it is none, then using default value in `.sh` file.

## Description

1. blender 生成 28800 imgs 和 poses `blender_output`，假设名字为 `sample`。在 `/home/spl6/Documents/xkj` 目录下, `file_name = sample`。

2. 将 imgs 移动至 `sample/gs`，poses 移动至 `sample`:

   ```bash
   mkdir ./Synthetic_Data/file_name 
   mv ./blender_outputs/file_name ./Synthetic_Data/file_name
   rename ./Synthetic_Data/file_name/train->./Synthetic_Data/file_name/gs
   ```

3. `create_rs` 将 28800 标准化命名，并处理为 60 rs 保存至 `sample/rs`:
   ```bash
   python3 ./Synthetic_Data/create_RS.py -i ./file_name/gs
   ```

4. 在步骤 3 的基础上整合 `json_path`，处理 `gspose`，生成 `rspose` 保存至 `sample`:
   ```bash
   rename ./file_name/transforms_train_gs.json
   python3 ./Synthetic_Data/json_path.py -js ./file_name/transforms_train_gs.json -o ./file_name
   ```

5. `synthetic_timestamp` 生成 `gs`、`rs` 时间戳保存至 `sample/gs` 和 `sample/rs`:
   ```bash
   python3 ./Synthetic_Data/synthetic_timestamp.py -path ./flie_name
   ```

6. 使用 `DVS-Voltmeter/data_process.py` 生成 `gs` info，保存至 `sample/gs`:
   ```bash
   python3 ./DVS-Voltmeter/data_process.py -path ../Synthetic_Data/flie_name/gs
   ```

7. `main.py` 读取 `sample/gs` 图片，480 图片一组的 `ev_rs_xxx.txt` 保存至 `sample/events`:
   ```bash
   python3 ./DVS-Voltmeter/main.py --input_dir ../Synthetic_Data/file_name/gs --output_dir ../Synthetic_Data/file_name/events --process_model 1
   ```

8. 可视化 event `ev_rs_xxx.txt` 为 `ev_rs_xxx.png` `-m 0` 视频 `1` 图像:
   ```bash
   python3 ./Synthetic_Data/gen_vid.py -ev './file_name/events' -m 0
   ```

9. 生成 `rs_blur`:
   ```bash
   python3 ./Synthetic_Data/blurring_rs.py -i ./file_name/gs -o ./file_name/rs_blur --blur_latency 200
   ```
