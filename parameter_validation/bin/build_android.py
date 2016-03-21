#!/usr/bin/env python

import os
import subprocess
import sys

os.chdir("..")

result = subprocess.call(
    "tdm_build.py --config parameter_validation/backend.config.json -asr android",
    shell=True)
sys.exit(result)
