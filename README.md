# Enabling Analysis and Reasoning on Software Systems through Knowledge Graph Representation

Knowledge Extractor for C and C++ programs based on the model defined by Rukmono and Chaudron in [Enabling Analysis and Reasoning on Software Systems through Knowledge Graph Representation](https://ieeexplore.ieee.org/document/10174249).

The output of this can be visualized using [ClassViz](https://github.com/matteasu/classviz).

More details about this can be found in the [thesis](https://github.com/matteasu/MSc-thesis/blob/main/thesis.pdf).

### Requirements
- Python 3.10 +
- [Requests library](https://pypi.org/project/requests/)
- [Pyyaml library](https://pypi.org/project/PyYAML/)
- [Maven](https://maven.apache.org/install.html) 
- [Rascal Standalone Jar version 0.35.0-RC1](https://releases.usethesource.io/maven/org/rascalmpl/rascal/) or newer releases

### Install Instructions
- Clone the repo
- Install the Python requirements
- Place the Rascal JAR file under the `project` folder
- cd into the `project` folder, and run `mvn dependency:copy-dependencies` to download all the dependencies needed by Rascal

### Usage Instructions
- To extract a program, it is necessary to specify the source code files, paths, and where Rascal should look for the potential included libraries. All of this is parsed from a YAML file. Two examples of this are provided in the repo.
- At the moment, it is necessary to specify the name of the YAML file by manually modifying the `main.py` file; a future version of this tool will improve this aspect.
- Run `main.py`
- This knowledge extractor can also be used to embed Vulnerability information produced by analyzers such as [MATE](https://galoisinc.github.io/MATE/index.html) or [Infer](https://fbinfer.com/). By looking at `extractor.py`, it should be clear enough how to implement additional parsers for other code analyzers.

this is a test
