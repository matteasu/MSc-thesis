import json
import re
import os 


def get_cleanPath(path):
    return re.sub(r'\\',"",re.split("\|",re.sub("\|file:\/\/","",path))[0])

def remove_rule(item):
    try:
        if re.match("problem",item) is None:
            return item
    except:
        return item
    return None

def cleaner(path):
    clean_path = get_cleanPath(path)
    with open(os.path.join(clean_path,"m3CLI.json"),"r") as dirty:
        parsed = json.load(dirty)
        for key in parsed.keys():
            if type(parsed.get(key)) == list and len(parsed.get(key)) > 0:
                for index,el in enumerate(parsed.get(key)):
                    if type(el) == list:
                        el = [e for e in el if remove_rule(e)]
                        parsed[key][index] = el
        with open(os.path.join(clean_path,"m3_clean.json"),"w") as clean:
            clean.write(json.dumps(parsed))