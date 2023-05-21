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
import time

# Set dataset name and dir.
DATA_NAME = "Gendarmenmarkt"
NUM_WORKERS = 2
ENABLE_CLUSTER = False
ENABLE_COLMAP_GT = True

# Automatically check if running on cluster from the user name.
if "ydu318" in os.environ["HOME"]:
    DATA_ROOT = "/home/ydu318/sfm/data/1dsfm/"
    IMG_DIR = os.path.join(DATA_ROOT, DATA_NAME)
else:
    DATA_ROOT = "/mnt/DATA/Datasets/sfm/1dsfm"
    IMG_DIR = os.path.join(DATA_ROOT, "images." + DATA_NAME, DATA_NAME)

# Set python script name.
NODE_NAME = "run_scene_optimizer_1dsfm.py"

if ENABLE_COLMAP_GT:
    # Set node name.
    NODE_NAME = "run_scene_optimizer_colmaploader.py"
    # Set colmap result dir.
    COLMAP_RESULT_DIR = os.path.join(IMG_DIR, "colmap_result/sparse/0")

# Compose main cmd.
cmd = (
    "python gtsfm/runner/"
    + NODE_NAME
    + " "
    + "--config_name deep_front_end.yaml "
    + "--dataset_root "
    + IMG_DIR
    + " "
    + "--max_frame_lookahead 10000000 "
    + "--num_workers "
    + str(NUM_WORKERS)
    + " "
    + "--threads_per_worker 8 "
    + "--max_resolution 640 "
    + "--mvs_off"
)
if ENABLE_CLUSTER:
    cmd += " --cluster_config cluster.yaml"

# Add colmap dir if enabled.
if ENABLE_COLMAP_GT:
    cmd = cmd.replace("dataset_root", "images_dir")  # dummy replacement
    cmd += " --colmap_files_dirpath " + COLMAP_RESULT_DIR

# Clear previous result.
cmd_clear = "python benchmark/clear_result.py"
print(cmd_clear)
subprocess.call(cmd_clear, shell=True)
time.sleep(1)

# Run cmd.
print(cmd)
subprocess.call(cmd, shell=True)
