from pathlib import Path
import json


funcdir = "/data/ds000031/sub-01/ses-WashU/func"
files = [i.as_posix() for i in Path(funcdir).glob('*.json')]
for file in files:
        
    with open(file) as f:
        data = json.load(f)
    if file.find('restEyesOpen') > -1:
        data['TaskName'] = 'restEyesOpen'
    else:
        data['TaskName'] = 'rest'
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)
