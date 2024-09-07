import numpy as np
import os
import argparse


def cvt_txt2npy(evt_path):
    event_txts = [os.path.join(evt_path, f) for f in sorted(
        os.listdir(evt_path)) if f.endswith(".txt")]
    for evt_txt in event_txts:
        evt_npy = []
        with open(evt_txt, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                ns_t, x, y, p = line.split()
                if int(p) == 0:
                    p = -1
                
                evt = [int(x), int(y), int(ns_t), int(p), 0]
                evt_npy.append(evt)
        event_npy_path = evt_txt.replace('.txt', '.npy')
        print("Writing {}".format(event_npy_path))
        np.save(event_npy_path, np.array(evt_npy))
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='convert txt to npy form')
    parser.add_argument('--event_path', '-ev', type=str, default="./lego_unblink_sample/events",
                        help='original event txt file.')
    
    args = parser.parse_args()
    evt_path = args.event_path
    cvt_txt2npy(evt_path)
