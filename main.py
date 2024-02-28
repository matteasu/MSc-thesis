import os

import json
from utils import utils
from parsers import *
from extractor import infer_extractor, mate_poi_extractor

cpp, names, stdLib, includeDirs, path = utils.parse_settings()
os.system(
    "cd ./project && java -jar rascal.jar Main -cpp {} -srcPath {} -names {} -stdLib {} -includeDir {}".format(
        cpp, path, " ".join(names), " ".join(stdLib), " ".join(includeDirs)
    )
)
print("trying to clean the file\n")
utils.cleaner(path)
with open(os.path.join(utils.get_cleanPath(path), "m3_clean.json"), "r") as clean:
    parsed = json.load(clean)
    """issues = mate_poi_extractor(
        "25572de1d88647e3978e043fb6a5ae96", "http://localhost:8666"
    )"""
    if cpp == "true":
        kind = Cpp
    else:
        kind = C
    converter = kind(utils.get_cleanPath(path), parsed, None)

    converter.export()
    print("exported!")
