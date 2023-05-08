#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@file pack_result.py
@author Yanwei Du (yanwei.du@gatech.edu)
@date 05-07-2023
@version 1.0
@license Copyright (c) 2023
@desc None
"""

from pathlib import Path
import subprocess
import os

prefix = Path(__file__).resolve().parent.parent

filenames = [
    "*-dask-report.html",
    "debug/",
    "plots/",
    "results/",
    "result_metrics/",
    "visual_comparison_dashboard.html",
    "visual_comparison_dashboard.zip",
]

results = [os.path.join(prefix, s) for s in filenames]

print("Zipping results ...")
cmd_zip = "zip -r result.zip " + " ".join(filenames)
print(cmd_zip)
subprocess.call(cmd_zip, shell=True)
print("Done")
