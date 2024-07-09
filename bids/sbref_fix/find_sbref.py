# find bad sbref files


# load bids layout
import os
import sys
import json
import pandas as pd
from bids import BIDSLayout

bidsdir = 
layout = BIDSLayout(bidsdir, validate=False)

sbref_files = layout.get(extension='nii.gz', suffix='sbref', return_type='filename')

