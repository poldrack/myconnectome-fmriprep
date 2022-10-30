# actually more like re-bidsifying the dataset to fit into the existing BIDS structure
# only transfer the bold/dwi data - T1/2 have already been transferred

import os
from pathlib import Path
from bids import BIDSLayout
import shutil
import json

dirmap = {'1': '2022',
          '2': '2022b'}


if __name__ == "__main__":
    basedir = '/data/newdirs/myconnectome_2022/BIDS'
    targdir = '/data/ds000031'
    base_layout = BIDSLayout(basedir)
    cmds = []
    for ses in ['1', '2']:
        sesfiles = base_layout.get(session=ses, extension=['json', 'nii.gz', 'bvec', 'bval'], 
            datatype=['func', 'dwi'], return_type='filename')
        for sesfile in sesfiles:
            newfile = sesfile.replace(basedir, targdir).replace(
                f'ses-{ses}', f'ses-{dirmap[ses]}').replace(
                    'sub-s01', 'sub-01')
            if sesfile.find('echo') > -1:
                newfile = newfile.replace('task-rest', 'task-restME')
                echonum = newfile.split('echo-')[1].split('_')[0]
                jsonbase = os.path.join(basedir, f'task-restME_echo-{echonum}_bold.json')
                task = 'restME'
            else:
                jsonbase = os.path.join(basedir, 'task-rest_bold.json')
                task = 'rest'
            
            print(f'cp {sesfile} {newfile}\n')
            if not os.path.exists(os.path.dirname(newfile)):
                os.makedirs(os.path.dirname(newfile))
            shutil.copy(sesfile, newfile)
            if sesfile.find('bold') > -1:
                metadata = json.load(open(jsonbase))
                metadata['TaskName'] = task
                json.dump(metadata, open(newfile.replace('.nii.gz', '.json'), 'w'))

