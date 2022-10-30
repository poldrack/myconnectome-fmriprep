from pathlib import Path
import json

basedir = '/data/ds000031/sub-01/ses-2022b/func'
files = [i.as_posix() for i in Path(basedir).glob('*_bold.json')]
for file in files:
    print(file)
    data = json.load(open(file))
    data = data['bidsinfo']
    data['TaskName'] = 'rest'
    json.dump(data, open(file, 'w'), indent=4)
