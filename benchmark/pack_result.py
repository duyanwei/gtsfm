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

import glob
import os
import zipfile
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
]

with zipfile.ZipFile(os.path.join(RESULT_DIR, "../result.zip"), "w") as f:
    for fname in filenames:
        fpath = os.path.join(RESULT_DIR, fname)
        fpath = os.path.abspath(fpath)
        if os.path.isfile(fpath):
            print(fpath)
            f.write(fpath, arcname=fname)
        elif "*" in fpath:
            for subfile_fullpath in glob.glob(fpath):
                print(subfile_fullpath)
                f.write(subfile_fullpath, arcname=subfile_fullpath.replace(RESULT_DIR, ""))
        else:
            for root, dirs, files in os.walk(fpath):
                for subfile in files:
                    subfile_fullpath = os.path.join(root, subfile)
                    print(subfile_fullpath)
                    f.write(subfile_fullpath, arcname=subfile_fullpath.replace(RESULT_DIR, ""))
print("Done")
