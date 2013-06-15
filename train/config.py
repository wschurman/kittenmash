import json
import os.path

# load json config
cfile = open(os.path.dirname(__file__) + '/../config.json')
cf = json.load(cfile)
cfile.close()


def config(key):
    if isinstance(cf[key], int):
        return cf[key]
    else:
        return str(cf[key])
