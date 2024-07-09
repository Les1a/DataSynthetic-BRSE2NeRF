import os

import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import argparse


def txt2sequence(txt_path, fps=3000):
    event_points = pd.read_csv(txt_path, delim_whitespace=True, names=['t', 'x', 'y', 'p'], nrows=2.5e7)

    period_t = 1 / fps * 1e6  # s
    num_frame = ((event_points.iloc[-1]['t'] - event_points['t'][0]) * fps) // 1e6

    '''sum events'''
    print(int(num_frame))
    img_list = []
    for n in np.arange(num_frame):
        # print(n)
        chosen_idx = np.where((event_points['t'] - event_points['t'][0] >= period_t * n) &
                              (event_points['t'] - event_points['t'][0] < period_t * (n + 1)))[0]
        xypt = event_points.iloc[chosen_idx]
        x, y, p = xypt['x'], xypt['y'], xypt['p']
        p = p * 2 - 1

        img = np.zeros((480, 640))
        img[y, x] += p
        img_list.append(img)
    img_list = np.array(img_list)
    return img_list


def vidvis(images, output_path='./vis.mp4'):
    # output_path = './vis.mp4'

    # define the color map
    cmap = plt.cm.get_cmap('jet').copy()
    cmap.set_under('k')

    # get the height, width, and number of frames of the video
    num_frames, height, width = images.shape

    # create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(output_path, fourcc, 60, (width, height))

    # write each image to the video writer
    for i in range(num_frames):
        output_filename = f'ev_{i:04d}.png'
        # get the image and normalize it
        frame = images[i, :, :]
        image = cmap(frame)
        image = (image[:, :, :3] * 255).astype(np.uint8)

        # set the color for values below the minimum to black
        image[frame == 0] = [0, 0, 0]

        # set the color for values above or equal to 1 to red
        image[(frame >= 1)] = [0, 0, 255]

        # set the color for values below or equal to 1 to green
        image[(frame <= -1)] = [0, 255, 0]

        # write the color image to the video writer
        # cv2.imwrite(output_filename, image)
        output_video.write(image)

    # release the video writer object
    output_video.release()


def imgvis(images, output_path='./vis.mp4'):
    # get the height, width, and number of frames of the video
    num_frames, height, width = images.shape

    for i in range(num_frames):
        # get the image and normalize it
        frame = images[i, :, :]
        cmap = plt.cm.get_cmap('jet').copy()
        cmap.set_under('k')
        image = cmap(frame)
        image = (image[:, :, :3] * 255).astype(np.uint8)

        # set the color for values below the minimum to black
        image[frame == 0] = [0, 0, 0]

        # set the color for values above or equal to 1 to red
        image[(frame >= 1)] = [0, 0, 255]

        # set the color for values below or equal to 1 to green
        image[(frame <= -1)] = [0, 255, 0]

    cv2.imwrite(output_path, image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='convert txt to npy form')
    parser.add_argument('--event_path', '-ev', type=str, default="./lego_unblink_sample/events",
                        help='original event txt file.')
    parser.add_argument('--vis_mode', '-m', type=int, default='0')

    args = parser.parse_args()
    evt_path = args.event_path
    vis_mode = args.vis_mode

    for files in os.listdir(evt_path):
        if files.endswith('.txt'):
            file_path = os.path.join(evt_path, files)
            vid_path = file_path.replace('.txt', '.mp4')
            img_path = file_path.replace('.txt', '.png')

            # trans to video
            if vis_mode == 0:
                img_seq = txt2sequence(file_path, 3000)
                vidvis(img_seq, vid_path)
            elif vis_mode == 1:
                img_seq = txt2sequence(file_path, 20)
                imgvis(img_seq, img_path)
            print(file_path, ' Processing Done!')
