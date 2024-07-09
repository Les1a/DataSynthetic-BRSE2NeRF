# DataSynthetic-BRSE2NeRF

### Run    
    After blender generation
    
    you can change the default value of file_name in gen_syn_data.sh according to the name of blender data.
    
    Next, open a terminal to run 'bash gen_syn_data.sh ordered_name'

    "ordered_name" parameter influences file_name, and if it is none, then using default value in .sh file

### Description
    1、blender生成28800imgs和poses blender_output 假设名字为sample
    在/home/spl6/Documents/xkj目录下
    file_name = sample

    2、将imgs移动至sample/gs，poses移动至sample
    
    '''
    mkdir ./Synthetic_Data/file_name 
    mv ./blender_outputs/file_name ./Synthetic_Data/file_name
    rename ./Synthetic_Data/file_name/train->./Synthetic_Data/file_name/gs
    '''

    3、create_rs 将28800标准化命名，并处理为60rs保存至sample/rs 
    
    '''
    python3 ./Synthetic_Data/create_RS.py -i ./file_name/gs
    '''

    4、3、基础上整合json_path，处理gspose，生成rspose保存至sample
    
    '''
    rename ./file_name/transforms_train_gs.json
    python3 ./Synthetic_Data/json_path.py -js ./file_name/transforms_train_gs.json -o ./file_name
    '''

    5、synthetic_timestamp生成gs、rs时间戳保存至sample/gs和sample/rs

    '''
    python3 ./Synthetic_Data/synthetic_timestamp.py -path ./flie_name
    '''

    6、使用dvs中data_process.py生成gs info，保存至sample/gs

    '''
    python3 ./DVS-Voltmeter/data_process.py -path ../Synthetic_Data/flie_name/gs
    '''

    7、main.py读取sample/gs图片，480图片一组的ev_rs_xxx.txt保存至sample/events

    '''
    python3 ./DVS-Voltmeter/main.py --input_dir ../Synthetic_Data/file_name/gs --output_dir ../Synthetic_Data/file_name/events --process_model 1
    '''

    8、可视化event ev_rs_xxx.txt 为 ev_rs_xxx.png -m 0视频 1图像

    '''
    python3 ./Synthetic_Data/gen_vid.py -ev './file_name/events' -m 0
    '''
    
    <!--(~~8、event_segment，分为60个保存至sample/events，原events删除

    '''
    python3 ./Synthetic_Data/event_seg.py -path ./file_name
    rm ./file_name/gs.txt
    '''

    9、event的txt文件转npy

    '''
    python3 ./Synthetic_Data/cvt_txt2npy.py -ev './file_name/events'~~)
    '''-->
    
    10、生成rs_blur

    '''
    python3 ./Synthetic_Data/blurring_rs.py -i ./file_name/gs -o ./file_name/rs_blur --blur_latency 200
    '''

