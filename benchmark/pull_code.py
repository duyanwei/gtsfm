#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@file pull_code.py
@author Yanwei Du (yanwei.du@gatech.edu)
@date 05-23-2023
@version 1.0
@license Copyright (c) 2023
@desc None
"""

import os
import subprocess

repo = "https://github.com/duyanwei/gtsfm.git"

branch = "feature/benchmark_1dsfm"
git_cmds = ["git checkout master", "git branch -D " + branch, "git pull", "git checkout " + branch]

cmd_cd = "cd " + os.path.join(os.environ["HOME"], "sfm/gtsam")
print(cmd_cd)
subprocess.call(cmd_cd, shell=True)

# git command
for cmd_git in git_cmds:
    print(cmd_git)
    subprocess.call(cmd_git, shell=True)

print("Done")
