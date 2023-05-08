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
from pathlib import Path
import subprocess

"""
Usage:
cd gtsfm
python benchmark/clear_result.py
"""


prefix = Path(__file__).resolve().parent.parent

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
cmd_rm = "rm -rf " + " ".join(filenames)
print(cmd_rm)
subprocess.call(cmd_rm, shell=True)
print("Done")
