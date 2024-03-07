# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import os

dataiku.code_studio.server.

os.chdir('/home/dataiku/lib/project/project-python-libs/FIRSTANALYTICSTRACERBULLET/python/test_project')

import sys
from test_lib.functions import hello_world

sys.path.append('/home/dataiku/lib/project/project-python-libs/FIRSTANALYTICSTRACERBULLET/python/test_project/src/test_project/')

from main import bk_main

# Read recipe inputs
audit = dataiku.Dataset("audit")
audit_df = audit.get_dataframe()

bk_main()

# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.
audit_pitonic_df = audit_df # For this sample code, simply copy input to output

# Write recipe outputs
audit_pitonic = dataiku.Dataset("analyticsbk_dataset")
audit_pitonic.write_with_schema(audit_pitonic_df)

print(audit.read_schema())
