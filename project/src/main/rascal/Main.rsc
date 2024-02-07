module Main

import IO;
import lang::cpp::M3;
import lang::json::IO;
int main(bool cpp=false, loc srcPath=|file:///|,list[str] names=[],list[loc] stdLib=[],list[loc]includeDir=[]) {
    map[str,M3] models = ();
    println("Starting with model creation");
    if(cpp==true){
        models = (name:tup|name <-names,tup:= createM3FromCppFile(srcPath+(name+".cpp"),stdLib=stdLib,includeStdLib=false,includeDirs=includeDir));
        
    }
    else{
        models = (name:tup|name <-names,tup:= createM3FromCFile(srcPath+(name+".c"),stdLib=stdLib,includeStdLib=false,includeDirs=includeDir));
    }
    compose = composeCppM3(srcPath,{model|name<-names,model:=models[name]});
    writeJSON(srcPath+("m3CLI.json"),compose);
    print("Model saved in ");
    println(srcPath);
    return 0;
}

