import re
import os
import json


class Cpp:
    primitives = ["int", "float", "void", "char", "string", "boolean"]
    viz = {"elements": {"nodes": [], "edges": []}}
    parsed = None
    path = None

    def __init__(self, path, parsed) -> None:
        self.path = path
        self.parsed = parsed

    def add_edges(self, kind, content, other=None):
        match kind:
            case "hasScript":
                edge_id = hash(content[0])
                self.viz["elements"]["edges"].append(
                    {
                        "data": {
                            "id": edge_id,
                            "source": content[1]["class"],
                            "properties": {"weight": 1},
                            "target": content[0],
                            "labels": [kind],
                        }
                    }
                )
            case "hasParameter":
                for parameter in content[1]["arguments"]:
                    if parameter is not None and parameter != "":
                        edge_id = hash(parameter["name"]) + hash(content[0])
                        self.viz["elements"]["edges"].append(
                            {
                                "data": {
                                    "id": edge_id,
                                    "source": content[0],
                                    "properties": {"weight": 1},
                                    "target": content[0] + "." + parameter["name"],
                                    "labels": [kind],
                                }
                            }
                        )
                        edge_id = (
                            hash(parameter["name"])
                            + hash(content[0])
                            + hash(content[1]["location"]["file"])
                        )
                        self.viz["elements"]["edges"].append(
                            {
                                "data": {
                                    "id": edge_id,
                                    "source": content[1]["location"]["file"],
                                    "properties": {"weight": 1},
                                    "target": content[0] + "." + parameter["name"],
                                    "labels": ["contains"],
                                }
                            }
                        )
            case "returnType":
                edge_id = hash(content[0]) + hash(content[1]["returnType"])
                self.viz["elements"]["edges"].append(
                    {
                        "data": {
                            "id": edge_id,
                            "source": content[0],
                            "properties": {"weight": 1},
                            "target": content[1]["returnType"],
                            "labels": [kind],
                        }
                    }
                )
            case "specializes":
                edge_id = hash(content[0]) + hash(content[1]["extends"])
                self.viz["elements"]["edges"].append(
                    {
                        "data": {
                            "id": edge_id,
                            "source": content[0],
                            "properties": {"weight": 1},
                            "target": content[1]["extends"],
                            "labels": [kind],
                        }
                    }
                )
            case "hasVariable":
                edge_id = hash(content[0]) + hash(content[1]["variableName"])
                self.viz["elements"]["edges"].append(
                    {
                        "data": {
                            "id": edge_id,
                            "source": content[1]["functionName"],
                            "properties": {"weight": 1},
                            "target": content[0],
                            "labels": [kind],
                        }
                    }
                )
                edge_id = edge_id + hash(
                    other[content[1]["functionName"]]["location"]["file"]
                )
                self.viz["elements"]["edges"].append(
                    {
                        "data": {
                            "id": edge_id,
                            "source": other[content[1]["functionName"]]["location"][
                                "file"
                            ],
                            "properties": {"weight": 1},
                            "target": content[0],
                            "labels": ["contains"],
                        }
                    }
                )
            case "invokes":
                edge_id = hash(content["target"]) + hash(content["source"])
                self.viz["elements"]["edges"].append(
                    {
                        "data": {
                            "id": edge_id,
                            "source": content["source"],
                            "properties": {"weight": 1},
                            "target": content["target"],
                            "labels": [kind],
                        }
                    }
                )
            case "contains":
                if content[1]["location"].get("file") is None:
                    pass
                else:
                    edge_id = hash(content[0]) + hash(content[1]["location"]["file"])
                    self.viz["elements"]["edges"].append(
                        {
                            "data": {
                                "id": edge_id,
                                "source": content[1]["location"]["file"],
                                "properties": {"weight": 1},
                                "target": content[0],
                                "labels": [kind],
                            }
                        }
                    )

    def add_nodes(self, kind, content, issues=None):
        match kind:
            case "file":
                self.viz["elements"]["nodes"].append(
                    {
                        "data": {
                            "id": content,
                            "properties": {"simpleName": content, "kind": kind},
                            "labels": ["Container"],
                        }
                    }
                )
            case "function":
                vulnerabilities = []
                self.viz["elements"]["nodes"].append(
                    {
                        "data": {
                            "id": content[0],
                            "properties": {
                                "simpleName": content[1]["functionName"],
                                "kind": kind,
                                "vulnerabilities": vulnerabilities,
                                "location": content[1]["location"],
                            },
                            "labels": ["Operation"],
                        }
                    }
                )

    def get_files(self):
        data = self.parsed["provides"]
        files = []
        for f in data:
            files.append(f[0])
        files = list(dict.fromkeys(files))
        for f in files:
            files[files.index(f)] = re.sub("\/.+\/", "", f)
        return files

    def get_actual_location(self, function):
        data = self.parsed["functionDefinitions"]
        location = {}
        for element in data:
            if re.match("cpp\+function:", element[0]) and function in element[0]:
                location["file"], location["position"] = re.split("\(", element[1])
                location["file"] = re.sub("\|file:.+/", "", location["file"])[:-1]
                location["position"] = "(" + location["position"]
                break
        return location

    def get_functions(self):
        functions = {}
        arguments = []
        data = self.parsed["declaredType"]
        for element in data:
            if re.match("cpp\+function:", element[0]):
                parameter_types = []
                function = dict()
                function["functionName"] = re.split(
                    "\(", re.sub("cpp\+function:.+\/", "", element[0])
                )[0]
                function["location"] = self.get_actual_location(
                    function["functionName"]
                )
                returnField = self.get_type_field(element[1]["returnType"])
                function["returnType"] = self.get_type(
                    element, "returnType", returnField
                )
                if element[1]["parameterTypes"]:
                    pass
                functions[function["functionName"]] = function
        return functions

    def get_type_field(self, element):
        if "baseType" in element.keys():
            return "baseType"
        if "decl" in element.keys():
            return "decl"
        if "type" in element.keys():
            return "type"

    def get_type(self, element, field1, field2):
        if field2 == "decl":
            return re.sub("cpp\+class:\/+,", "", element[1][field1][field2])
        if field2 == "type":
            if "decl" in element[1][field1][field2].keys():
                if (
                    element[1][field1][field2]["decl"]
                    == "cpp+classTemplate:///std/__cxx11/basic_string"
                ):
                    return "string"
                else:
                    return re.sub(
                        "cpp\+class:\/+",
                        "",
                        element[1][field1][field2]["decl"],
                    )
        if field2 == "baseType":
            return element[1][field1][field2]

    def export(self):
        functions = self.get_functions()
        for func in functions.items():
            self.add_nodes("function", func, None)
            self.add_edges("contains", func)
        for file in self.get_files():
            self.add_nodes("file", file)
        with open(os.path.join(self.path, "converted.json"), "w") as f:
            f.write(json.dumps(self.viz))
