import json
import shutil
import sys
print(sys.argv[1])

if len(sys.argv) < 2 or sys.argv[1].find('json') < 0:
    raise Exception('Must specify a json file as the argument')

with open(sys.argv[1]) as f:
    data = json.load(f)

data["B0FieldIdentifier"] = "meanfmap"
shutil.copy(sys.argv[1], sys.argv[1] + '_bak')

with open(sys.argv[1], 'w') as f:
    json.dump(data, f, indent=4)
