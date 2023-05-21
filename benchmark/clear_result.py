#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@file clear_result.py
@author Yanwei Du (yanwei.du@gatech.edu)
@date 05-08-2023
@version 1.0
@license Copyright (c) 2023
@desc None
"""

import os
import subprocess
from pathlib import Path

# Set result dir.
RESULT_DIR = ""

# Check result dir.
if RESULT_DIR == "":
    RESULT_DIR = str(Path(__file__).resolve().parent.parent)
assert os.path.exists(RESULT_DIR)

filenames = [
    "*-dask-report.html",
    "debug/",
    "plots/",
    "results/",
    "result_metrics/",
    "visual_comparison_dashboard.html",
    "visual_comparison_dashboard.zip",
    "result*.zip",
]

print("Removing existing results ...")
prefix = " " + RESULT_DIR + "/"
cmd_rm = "rm -rf" + prefix + prefix.join(filenames)
print(cmd_rm)
subprocess.call(cmd_rm, shell=True)
print("Done")
