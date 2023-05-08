#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@file run_cmd.py
@author Yanwei Du (yanwei.du@gatech.edu)
@date 05-06-2023
@version 1.0
@license Copyright (c) 2023
@desc None
"""


import os
import subprocess

DATA_ROOT = "/mnt/DATA/Datasets/SFM/1DSFM"
DATA_NAME = "Alamo"  # Gendarmenmarkt

IMG_DIR = os.path.join(DATA_ROOT, "images." + DATA_NAME, DATA_NAME, "images")
COLMAP_RESULT_DIR = os.path.join(IMG_DIR, "../colmap_result/sparse/0")
NUM_WORKERS = 3

cmd = (
    "python gtsfm/runner/run_scene_optimizer_colmaploader.py "
    + "--config_name deep_front_end.yaml "
    + "--images_dir "
    + IMG_DIR
    + " "
    + "--colmap_files_dirpath "
    + COLMAP_RESULT_DIR
    + " "
    + "--max_frame_lookahead 10000000 "
    + "--num_workers "
    + str(NUM_WORKERS)
    + " "
    + "--threads_per_worker 8 "
    + "--max_resolution 6000 "
    + "--mvs_off"
)

print(cmd)
subprocess.call(cmd, shell=True)
