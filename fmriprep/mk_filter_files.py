# make filter files for single-session analyses


import os
import json
from bids import BIDSLayout

if __name__ == '__main__':

    basedir = '/data/ds000031'
    filterdir = f'{basedir}/derivatives/filters'
    if not os.path.exists(filterdir):
        os.makedirs(filterdir)
    
    # load the base json file
    with open('bids_fiter.json') as f:
        js = json.load(f)

    layout = BIDSLayout(basedir)

    # get all the sessions with BOLD data
    sessions = layout.get(return_type='id', target='session',
        suffix='bold', extension='nii.gz')
    
    for session in sessions:
        js_session = js.copy()
        js_session['bold']['session'] = session
        outfile = os.path.join(filterdir, f'ses-{session}_filter.json')
        with open(outfile, 'w') as f:
            json.dump(js_session, f, indent=4)
