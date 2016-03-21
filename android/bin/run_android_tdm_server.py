#!/usr/bin/env python

import os
import subprocess
import sys

os.chdir("..")

subprocess.call("tdm_session_and_backend_manager.py --config android/backend.config.json --open-recognizer-support %s" % (" ".join(sys.argv[1:])), shell=True)
