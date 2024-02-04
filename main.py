import os

import json
from utils import utils
from parsers.cpp import Cpp

cpp, names, stdLib, includeDirs, path = utils.parse_settings()
#os.system("cd ./project && java -jar rascal.jar Main -cpp {} -srcPath {} -names {} -stdLib {} -includeDir {}".format(cpp,path,' '.join(names),' '.join(stdLib),' '.join(includeDirs)))
print("trying to clean the file\n")
utils.cleaner(path)
with open(os.path.join(utils.get_cleanPath(path), "m3_clean.json"), "r") as clean:
    parsed = json.load(clean)
    c = Cpp(utils.get_cleanPath(path),parsed)
    c.export()
    print("exported!")
