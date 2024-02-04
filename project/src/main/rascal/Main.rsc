module Main

import IO;
import lang::cpp::M3;
import lang::json::IO;
int main(bool cpp=false, loc srcPath=|file:///|,list[str] names=[],list[loc] stdLib=[],list[loc]includeDir=[]) {
    println("Starting with model creation");
    if(cpp==true){
        map[str,M3] curl_models =(name:tup|name <-names,tup:= createM3FromCppFile(srcPath+(name+".cpp"),stdLib=stdLib,includeStdLib=false,includeDirs=includeDir));
        compose = composeCppM3(srcPath,{model|name<-names,model:=curl_models[name]});
        writeJSON(srcPath+("m3CLI.json"),compose);
        println("Model saved in ");
        print(srcPath);
    }
    else{
        println("ciao sono c");
    }
    return 0;
}

