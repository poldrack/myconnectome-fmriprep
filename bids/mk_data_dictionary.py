# create initial data dictionary (tsv) for myconnectome phenotype data

import json
from typing import OrderedDict
import pandas as pd
import os
import numpy as np
from collections import defaultdict

termurls = {
    'panas': 'https://www.cognitiveatlas.org/task/id/tsk_4a57abb949d09/',
    'diastolic': 'http://purl.bioontology.org/ontology/SNOMEDCT/407555005',
    'systolic': 'http://purl.bioontology.org/ontology/SNOMEDCT/407554009',
    'pulse': 'http://purl.bioontology.org/ontology/SNOMEDCT/78564009',
    'blood:ba': 'http://purl.bioontology.org/ontology/SNOMEDCT/42351005',
    'blood:eo': 'http://purl.bioontology.org/ontology/SNOMEDCT/71960002',
    'blood:hgb': 'http://purl.bioontology.org/ontology/SNOMEDCT/38082009',
    'blood:ly': 'http://purl.bioontology.org/ontology/SNOMEDCT/74765001',
    'blood:mch': 'http://purl.bioontology.org/ontology/SNOMEDCT/54706004',
    'blood:mchc': 'http://purl.bioontology.org/ontology/SNOMEDCT/37254006',
    'blood:mcv': 'http://purl.bioontology.org/ontology/SNOMEDCT/104133003',
    'blood:mo': 'http://purl.bioontology.org/ontology/SNOMEDCT/67776007',
    'blood:mpv': 'http://purl.bioontology.org/ontology/SNOMEDCT/75672003',
    'blood:ne': 'http://purl.bioontology.org/ontology/SNOMEDCT/30630007',
    'blood:plt': 'http://purl.bioontology.org/ontology/SNOMEDCT/61928009',
    'blood:rbc': 'http://purl.bioontology.org/ontology/SNOMEDCT/14089001',
    'blood:wbc': 'http://purl.bioontology.org/ontology/SNOMEDCT/767002',
    'rna:rin': 'http://purl.obolibrary.org/obo/NCIT_C63637'
}

leveldict = {
    'panas': {
         '1': 'Very slightly or not at all', 
         '2': 'A little', 
         '3': 'Moderately', 
         '4': 'Quite a bit',
         '5': 'Extremely'
    },
    'Soreness': {
         '1': 'Extremely sore',
         '2': 'Very sore',
         '3': 'Sore', 
         '4': 'Average', 
         '5': 'Good', 
         '6': 'Very good', 
         '7': 'Extremely good'
    },
    'Sleepquality': {
         '1': 'Extremely poor',
         '2': 'Very poor',
         '3': 'Poor', 
         '4': 'Average', 
         '5': 'Good', 
         '6': 'Very good', 
         '7': 'Extremely good'
    },
    'Anxiety': {
         '1': 'Extremely anxious',
         '2': 'Very anxious',
         '3': 'anxious', 
         '4': 'Average', 
         '5': 'Good', 
         '6': 'Very good', 
         '7': 'Extremely good'
    },
    'Psoriasis': {
        '1': 'Extremely bad',
        '2': 'Very bad',
        '3': 'Bad', 
        '4': 'Average', 
        '5': 'Good', 
        '6': 'Very good', 
        '7': 'Extremely good'
        },
    'Stress': {
        '1': 'Extremely bad',
        '2': 'Very bad',
        '3': 'Bad', 
        '4': 'Average', 
        '5': 'Good', 
        '6': 'Very good', 
        '7': 'Extremely good'
        },
    'Gut': {
        '1': 'Extremely bad',
        '2': 'Very bad',
        '3': 'Bad', 
        '4': 'Average', 
        '5': 'Good', 
        '6': 'Very good', 
        '7': 'Extremely good'
        },
    'tinnitus': {
        '1': 'not bothered', 
        '2': 'bothered a little but not much', 
        '3': 'bothered more than a little but not a lot',
        '4': 'bothered a lot', 
        '5': 'extremely bothered'
    },
    'noisecancel': {
        '0': 'Absent',
        '1': 'Present'
    },
    ':has_': {
        '0': 'Absent',
        '1': 'Present'
    },
}

if __name__ == '__main__':
    basedir = '/data/ds000031/'

    sesfile = os.path.join(basedir, 'sub-01/sub-01_sessions.tsv')
    sesdf = pd.read_csv(sesfile, sep='\t')

    # create data dictionary
    dd = defaultdict(lambda :{
        'LongName': None,
        'Description': None,
        'Units': None,
        'Levels': None,
        'TermURL': None,})

    dd['sescode']['Description'] = 'Session code'
    
    orig_dd = pd.read_csv('orig_data_dictionary.tsv', sep='\t')
    orig_dd.set_index('VARIABLENAME', inplace=True)

    for id in sesdf.columns:
        if id in orig_dd.index:
            if orig_dd.loc[id, 'DESCRIPTION'] == 'DEPRECATED':
                dd[id]['Description'] = f'{id.split("_")[1]} scan present'
            else:
                dd[id]['Description'] = orig_dd.loc[id, 'DESCRIPTION']

            if orig_dd.loc[id, 'UNITS'] is not None and type(orig_dd.loc[id, 'UNITS']) == str:
                #heuristic for levels
                if not (orig_dd.loc[id, 'UNITS'].find("-") > -1 or orig_dd.loc[id, 'UNITS'].find("absent") > -1):
                    dd[id]['Units'] = orig_dd.loc[id, 'UNITS']
            for measure, levels in leveldict.items():
                if measure in id:
                    dd[id]['Levels'] = levels
                    del dd[id]['Units']
            for term, url in termurls.items():
                if term in id:
                    dd[id]['TermURL'] = url

            if 'Units' in dd[id] and dd[id]['Units'] == 'integer':
                dd[id]['Units'] = 'arbitrary integer'
            
            if 'Levels' in dd[id] and dd[id]['Levels'] is None:
                del dd[id]['Levels']

    dictfile = sesfile.replace('.tsv', '.json')
    assert dictfile != sesfile
    with open(dictfile, 'w') as f:
        json.dump(dd, f, indent=4)