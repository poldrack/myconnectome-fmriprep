import json
import shutil
import sys
from pathlib import Path
from bids import BIDSLayout

def add_source(file):
    with open(file) as f:
        data = json.load(f)

    data["B0FieldSource"] = "meanfmap"

    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    layout = BIDSLayout('/data/ds000031')
    boldfiles = layout.get(suffix='bold', datatype='func', extension='json')

    for file in boldfiles:
        print(f'fixing {file.path}')
        add_source(file.path)
