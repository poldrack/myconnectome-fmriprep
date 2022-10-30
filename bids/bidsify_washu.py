# bidsify bold data from washu session

import os
from pathlib import Path

if __name__ == "__main__":
    basedir = '/data/newdirs/washu/WashU_data'
    targdir = '/data/ds000031/sub-01/ses-WashU/func'
    if not os.path.exists(targdir):
        os.makedirs(targdir)

    cmds = []

    for sesfile in Path(basedir).glob('*RSFC*.nii.gz'):
        print(sesfile)
        if 'EO' in str(sesfile):
            task = 'restEyesOpen'
        else:
            task = 'rest'
        run = str(sesfile).split('.')[0].split('_')[-1]
        newfile = os.path.join(targdir, f'sub-01_ses-WashU_task-{task}_run-{run}_bold.nii.gz')
        print(sesfile, newfile)
        cmds.append(f'cp {str(sesfile)} {newfile}\n')
        cmds.append(f'cp {str(sesfile).replace("nii.gz", "json")} {newfile.replace("nii.gz", "json")}\n')

    with open('bidsify_washu.sh', 'w') as f:
        f.writelines(cmds)
