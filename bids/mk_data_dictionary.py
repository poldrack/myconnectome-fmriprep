# create initial data dictionary (tsv) for myconnectome phenotype data

import json
import pandas as pd
import os
import numpy as np

if __name__ == '__main__':
    basedir = '/data/ds000031/'

    sesfile = os.path.join(basedir, 'sub-01/sub-01_sessions.tsv')
    sesdf = pd.read_csv(sesfile, sep='\t')

    # create data dictionary
    dd = pd.DataFrame({
        'id': sesdf.columns,
        'LongName': None,
        'Description': None,
        'Units': None,
        'Levels': None,
        'TermURL': None,})

    orig_dd = pd.read_csv('orig_data_dictionary.tsv', sep='\t')
    orig_dd.set_index('VARIABLENAME', inplace=True)
    for id in dd.id:
        if id in orig_dd.index:
            print(id, orig_dd.loc[id, :])
            
            dd.loc[dd.id == id, 'Description'] = orig_dd.loc[id, 'DESCRIPTION']
            if orig_dd.loc[id, 'UNITS'] is not None and type(orig_dd.loc[id, 'UNITS']) == str:
                #heuristic for levels
                if orig_dd.loc[id, 'UNITS'].find("-") > -1 or orig_dd.loc[id, 'UNITS'].find("absent") > -1:
                    dd.loc[dd.id == id, 'Levels'] = orig_dd.loc[id, 'UNITS']
                else:
                    dd.loc[dd.id == id, 'Units'] = orig_dd.loc[id, 'UNITS']
    dd.to_csv('phenotype_data_dictionary.tsv', sep='\t', index=False)

    datadict = dd.to_dict()