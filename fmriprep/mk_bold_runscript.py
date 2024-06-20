# create script to run all sessions

from pathlib import Path

if __name__ == '__main__':

    base_script = 'run_ses-014.sh'
    basecmd = Path(base_script).read_text()

    basedir = Path('/data/ds000031')
    filterdir = basedir / 'derivatives' / 'filters'
    cmds = []
    for filter in filterdir.glob('*.json'):
        if 'ses-014' in filter.name:
            print('skipping', filter.name)
            continue
        cmds.append(basecmd.replace('ses-014_filter.json',
            str(filter.name)).replace('\\\n    ', ' '))

    cmds.sort()

    with open('run_all_sessions.sh', 'w') as f:
        f.write(''.join(cmds))