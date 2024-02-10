import json
import re
import os 
import yaml
import sys
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

def parse_settings(file_name):
    names = []
    stdLib = []
    includeDirs = []
    path = []
    if file_name is None:
        raise AttributeError("Missing yaml file")
    with open(file_name,'r') as file:
        settings = yaml.safe_load(file)
        try:
            cpp = settings['cpp']
        except KeyError:
            print("Missing cpp field")
            sys.exit(1)
        try:
            names = settings['file_names']
            if len(names)==0:
                raise ValueError("Missing values in file_names")
        except KeyError:
            print("Missing file_names field")
            sys.exit(1)
        try:
            stdLib = settings['std_lib']
            if len(stdLib)==0:
                raise ValueError("Missing values in file_names")
            stdLib = ["\|file://{}\|".format(path) for path in stdLib]
        except KeyError:
            print("Missing std_lib field")
            sys.exit(1)
        try:
            includeDirs = settings['include_paths']
            if len(includeDirs) > 0:
                includeDirs = ["\|file://{}\|".format(path) for path in includeDirs]
        except KeyError:
            print("Missing include_paths field")
            sys.exit(1)
        try:
            path = "\|file://{}\|".format(settings['path'])
            includeDirs.append(path)
        except KeyError:
            print("Missing path field")
            sys.exit(1)    
    return cpp,names,stdLib,includeDirs,path
