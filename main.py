import os
import re
from utils import utils
names = ["Choice","Player","RandomPlayer","HumanPlayer","BeatLastPlayer","BeatSelfPlayer","Game","main"]
stdLib = ["\|file:///usr/include/c++/8\|",
"\|file:///usr/include/x86_64-linux-gnu/c++/8\|",
"\|file:///usr/include/c++/8/backward\|",
"\|file:///usr/lib/gcc/x86_64-linux-gnu/8/include\|",
"\|file:///usr/local/include\|",
"\|file:///usr/lib/gcc/x86_64-linux-gnu/8/include-fixed\|",
"\|file:///usr/include\|"]
path="\|file:///home/masuni/rps-cpp/\|"
includeDirs = [path]
#os.system("cd ./project && java -jar rascal.jar Main -srcPath {} -names {} -stdLib {} -includeDir {}".format(path,' '.join(names),' '.join(stdLib),' '.join(includeDirs)))
print("trying to clean the file")
utils.cleaner(path)