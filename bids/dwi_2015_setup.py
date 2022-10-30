# rename files for bids


from pathlib import Path
import json
import os
import shutil

if __name__ == "__main__":
    basedir = Path('/data/newdirs/2015')
    targdir = '/data/ds000031/sub-01/ses-2015/dwi'
    if not os.path.exists(targdir):
        os.makedirs(targdir)
    for f in basedir.glob('*.nii.gz'):
        md = json.load(open(f.as_posix().replace('.nii.gz', '.json')))
        desc = md['SeriesDescription'].split(' ')
        label = f'sub-01_ses-2015_acq-{desc[2]}_dir-{desc[1]}_dwi'
        print(label)
        shutil.copy(f.as_posix(), os.path.join(targdir, label + '.nii.gz'))
        for ext in ('.json', '.bval', '.bvec'):
            shutil.copy(f.as_posix().replace('.nii.gz', ext), os.path.join(targdir, label + ext))