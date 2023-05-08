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

IMG_DIR = os.path.join(DATA_ROOT, "images." + DATA_NAME, DATA_NAME)
NUM_WORKERS = 3

cmd = (
    "python gtsfm/runner/run_scene_optimizer_1dsfm.py "
    + "--config_name deep_front_end.yaml "
    + "--dataset_root "
    + IMG_DIR
    + " "
    + "--max_frame_lookahead 10000000 "
    + "--num_workers "
    + str(NUM_WORKERS)
    + " "
    + "--threads_per_worker 8 "
    + "--max_resolution 6000 "
    + "--mvs_off"
)

# " --cluster_configs cluster.yaml"

print(cmd)
subprocess.call(cmd, shell=True)
