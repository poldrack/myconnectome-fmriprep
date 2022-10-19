from bids import BIDSLayout
import os

layout = BIDSLayout('/data/ds000031')

sessions = layout.get_sessions()
sessions.sort()

good_sessions = []
cmds = []

for session in sessions:
    t1 = layout.get(suffix='T1w', extension='nii.gz', session=session)
    t2 = layout.get(suffix='T2w', extension='nii.gz', session=session)
    if len(t2) > 0:
        t2file = os.path.join(t2[0].dirname, t2[0].filename)
        t2flag = f'-T2 {t2file} -T2pial'
    else:
        t2flag = ''
    if len(t1) > 0:
        t1file = os.path.join(t1[0].dirname, t1[0].filename)
        cmd = f'recon-all -all -s ses-{session} -i {t1file} {t2flag} -threads 7'
        cmds.append(cmd)
print(f'found {len(cmds)} good sessions')


with open('run_recon_all.sh', 'w') as f:
    for i in cmds:
        f.write(i + '\n')

