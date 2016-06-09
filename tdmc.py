#!/usr/bin/env python

import sys
import httplib
import re
import os
import json
from os.path import join

FILES_TO_UPLOAD = set(["backend.config.json",
                       "__init__.py",
                       "ddd.config.json",
                       "device.py",
                       "domain.xml",
                       "grammar_eng.xml",
                       "grammar_chi.xml",
                       "interactiontesting.config.json",
                       "ontology.xml",
                       "interaction_tests_eng.txt",
                       "interaction_tests_chi.txt",
                       "interaction_tests_gui_eng.txt",
                       "interaction_tests_gui_chi.txt",
                       "contacts.py",
                       ])

def upload_files():
    headers = {
        "Content-type": "text/plain",
        "Accept": "text/plain"
    }
    matching_filenames = []
    for dirpath, dirnames, filenames in os.walk ("."):
        for name in filenames:
            if name in FILES_TO_UPLOAD:
                file_path = join (dirpath, name)
                matching_filenames.append (file_path)

    for index, file_path in enumerate (matching_filenames):
        conn = httplib.HTTPConnection(tdmc_host, 9091)
        conn.request("POST", "/ddds/%s/%s" % (tdmc_account, file_path[2:].replace('\\', '/')), open(file_path, "rb"), headers)
        print conn.getresponse().read()
    
cloud_config_file_name = "cloud.config.json"

tdm_command = sys.argv[1]
if len(sys.argv) > 2:
    tdm_lang = "/%s" % sys.argv[2]
else:
    tdm_lang = ""
    
if tdm_command == "configure":
    new_config = {
        "tdmc_host": sys.argv[2],
        "tdmc_account": "song"
    }
    json.dump(new_config, open(cloud_config_file_name, "w"))
    print("Configured!")
    sys.exit()

if not os.path.exists(cloud_config_file_name):
    print("Missing cloud.config.json. Please run python tdmc.py configure <host>")
    sys.exit()
                  
tdmc_config = json.load(open(cloud_config_file_name, "r"))
                        
tdmc_host = tdmc_config.get("tdmc_host")
tdmc_account = tdmc_config.get("tdmc_account")


tdm_command = sys.argv[1]
if len(sys.argv) > 2:
    tdm_lang = "/%s" % sys.argv[2]
else:
    tdm_lang = ""
    
if tdm_command == "build":
    upload_files()
    conn = httplib.HTTPConnection(tdmc_host, 9091)
    conn.request("PUT", "/ddds/%s/tdm-build" % tdmc_account)
    print conn.getresponse().read()
elif tdm_command == "test":
    conn = httplib.HTTPConnection(tdmc_host, 9091)
    conn.request("PUT", "/ddds/%s/tdm-test%s" % (tdmc_account, tdm_lang))
    print conn.getresponse().read()
elif tdm_command == "serve":
    conn = httplib.HTTPConnection(tdmc_host, 9091)
    conn.request("PUT", "/ddds/%s/tdm-serve%s" % (tdmc_account, tdm_lang))
    print conn.getresponse().read()
elif tdm_command == "stop":
    conn = httplib.HTTPConnection(tdmc_host, 9091)
    conn.request("PUT", "/ddds/%s/tdm-stop" % tdmc_account)
    print conn.getresponse().read()
elif tdm_command == "upload":
    upload_files()
else:
    print "NYI"

