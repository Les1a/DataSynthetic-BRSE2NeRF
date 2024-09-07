import cv2
import os
import numpy as np
import argparse


def create_blur_rs(input_folder_gs, output_folder_rs, num_images, row_chunk_size):
    if not os.path.exists(output_folder_rs):
        os.makedirs(output_folder_rs)

    for i in range(1, num_images + 1):
        output_image_path_rs = os.path.join(output_folder_rs, f"rs_blur_{i:03d}.png")

        img_gs_list = []
        for j in range((i - 1) * 480 + 1, i * 480 + row_chunk_size + 1):
            input_image_path_gs = os.path.join(input_folder_gs, f"{j:06d}.png")

            img_gs = cv2.imread(input_image_path_gs, cv2.IMREAD_UNCHANGED)
            img_gs_list.append(img_gs)

        rs_image = np.zeros((480, 640, 3), np.uint8)
        for start in range(480):
            end = start + row_chunk_size
            gs_images_subset = img_gs_list[start:end]
            gs_rows = [img[start, :] for img in gs_images_subset]
            average_array = np.mean(gs_rows, axis=0)
            rs_image[start, :, :] = average_array

        cv2.imwrite(output_image_path_rs, rs_image)
        print(output_image_path_rs, '   Saved')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="blur rs images.")
    parser.add_argument("--input_gs", "-i", type=str, default="./room_2/gs",
                         help="Input folder path for gs images")
    parser.add_argument("--output_rs", "-o", type=str, default="./room_2/rs_blur",
                        help="Output folder path for rs images")
    # parser.add_argument("--num_images", type=int, default=59, help="Number of rs images to process")
    parser.add_argument("--blur_latency", type=int, default=200, help="blurring latency")

    args = parser.parse_args()
    input_gs = args.input_gs
    output_rs = args.output_rs
    blur_latency = args.blur_latency
    num_images = int((len(os.listdir(input_gs)) - 2 - blur_latency) / 480)

    create_blur_rs(input_gs, output_rs, num_images, blur_latency)
