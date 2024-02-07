apt-get update && apt-get -y install build-essential cmake
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 ..
infer run --compilation-database build/compile_commands.json --biabduction --bufferoverrun

