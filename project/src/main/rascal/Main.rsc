module Main

import IO;
import lang::cpp::M3;
import lang::json::IO;
public list[str] nomi = ["Choice","Player","RandomPlayer","HumanPlayer","BeatLastPlayer","BeatSelfPlayer","Game","main"];
public list[loc] standardLib=[
|file:///usr/include/c++/8|,
|file:///usr/include/x86_64-linux-gnu/c++/8|,
|file:///usr/include/c++/8/backward|,
|file:///usr/lib/gcc/x86_64-linux-gnu/8/include|,
|file:///usr/local/include|,
|file:///usr/lib/gcc/x86_64-linux-gnu/8/include-fixed|,
|file:///usr/include|
];
int main(list[str] names=[],list[loc] stdLib=[]) {
    println("Strating with model creation");
    println(names);
    println(stdLib);
    //map[str,M3] curl_models =(name:tup|name <-names,tup:= createM3FromCppFile(|file:///home/masuni/rps-cpp/|+(name+".cpp"),stdLib=standardLib,includeStdLib=false,includeDirs=[|file:///home/masuni/rps-cpp|]));
    //compose = composeCppM3(|file:///home/masuni/rps-cpp|,{model|name<-names,model:=curl_models[name]});
    //writeJSON(|file:///home/masuni/rps-cpp/m32023.json|,compose);
    //, list[loc] stdLib,list[loc] includeDir
    //println("Model saved in /home/masuni/rps-cpp/");
    return 0;
}
