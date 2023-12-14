from copy import deepcopy
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
                for parameter in content[1]["parameters"]:
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
            case "parameter":
                for parameter in content[1]["parameters"]:
                    if parameter is not None and parameter != "":
                        self.viz["elements"]["nodes"].append(
                            {
                                "data": {
                                    "id": content[0] + "." + parameter["name"],
                                    "properties": {
                                        "simpleName": parameter["name"],
                                        "kind": kind,
                                    },
                                    "labels": ["Variable"],
                                }
                            }
                        )
            case "method":
                vulnerabilities = []
                self.viz["elements"]["nodes"].append(
                    {
                        "data": {
                            "id": content[0],
                            "properties": {
                                "simpleName": content[1]["methodName"],
                                "kind": kind,
                                "vulnerabilities": vulnerabilities,
                            },
                            "labels": ["Operation"],
                        }
                    }
                )
            case "class":
                self.viz["elements"]["nodes"].append(
                    {
                        "data": {
                            "id": content[0],
                            "properties": {
                                "simpleName": content[1]["className"],
                                "kind": kind,
                            },
                            "labels": ["Structure"],
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

    def get_function_location(self, function):
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
        data = self.parsed["declaredType"]
        for element in data:
            if re.match("cpp\+function:", element[0]):
                parameters = []
                function = dict()
                function["functionName"] = re.split(
                    "\(", re.sub("cpp\+function:.+\/", "", element[0])
                )[0]
                function["location"] = self.get_function_location(
                    function["functionName"]
                )
                returnField = self.get_type_field(element[1]["returnType"])
                function["returnType"] = self.get_type(
                    element[1]["returnType"], returnField
                )
                if element[1]["parameterTypes"]:
                    parameters = self.get_parameters(
                        function["functionName"], function["location"]["file"]
                    )
                    i = 0
                    for parameter in element[1]["parameterTypes"]:
                        parameters[i]["type"] = self.get_parameter_type(
                            parameter, self.get_type_field(parameter)
                        )
                        i += 1
                function["parameters"] = parameters
                functions[function["functionName"]] = function
        return functions

    def get_methods(self):
        data = self.parsed["declaredType"]
        methods = {}
        for element in data:
            parameters = []
            if re.match("cpp\+method", element[0]):
                method = dict()
                method["class"] = re.split(
                    "\/", re.sub("cpp\+method:\/+", "", element[0])
                )[0]
                method["methodName"] = re.split(
                    "\(", re.sub("cpp\+method:\/+.+/", "", element[0])
                )[0]
                method["returnType"] = self.get_type(
                    element[1]["returnType"],
                    self.get_type_field(element[1]["returnType"]),
                )
                if element[1]["parameterTypes"]:
                    for parameter in element[1]["parameterTypes"]:
                        parameters.append(
                            self.get_parameter_type(
                                parameter, self.get_type_field(parameter)
                            )
                        )
                method["parameters"] = parameters
                id = method["class"] + "." + method["methodName"]
                methods[id] = method
        return methods

    def get_type_field(self, element):
        try:
            if "baseType" in element.keys():
                return "baseType"
            if "decl" in element.keys():
                return "decl"
            if "type" in element.keys():
                return "type"
        except:
            return None

    def get_type_deprecated(self, element, field1, field2):
        if field2 == "decl":
            return re.sub("cpp\+class:\/+", "", element[1][field1][field2])
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
            if "type" in element[1][field1][field2].keys():
                if "decl" in element[1][field1][field2]["type"].keys():
                    if "type" in element[1][field1][field2]["type"].keys():
                        if (
                            element[1][field1][field2]["type"]["type"]["decl"]
                            == "cpp+classTemplate:///std/__cxx11/basic_string"
                        ):
                            return "string"
                        return re.sub(
                            "cpp\+class:\/+",
                            "",
                            element[1][field1][field2]["type"]["type"]["decl"],
                        )
                    if (
                        element[1][field1][field2]["type"]["decl"]
                        == "cpp+classTemplate:///std/__cxx11/basic_string"
                    ):
                        return "string"
                    return re.sub(
                        "cpp\+class:\/+", "", element[1][field1][field2]["type"]["decl"]
                    )
        if field2 == "baseType":
            return element[1][field1][field2]

    def get_type(self, element, field):
        if self.get_type_field(element[field]) is not None:
            self.get_type(element[field], self.get_type_field(element[field]))
        else:
            if field == "baseType":
                return element[field]
            if field == "decl":
                if element[field] == "cpp+classTemplate:///std/__cxx11/basic_string":
                    return "string"
                else:
                    return re.sub("cpp\+class:\/+", "", element[field])

    def get_parameter_type(self, element, field):
        if field == "decl":
            return re.sub("cpp\+class:\/+", "", element[field])
        if field == "type":
            if "decl" in element[field].keys():
                if (
                    element[field]["decl"]
                    == "cpp+classTemplate:///std/__cxx11/basic_string"
                ):
                    return "string"
                else:
                    return re.sub("cpp\+class:\/+", element[field]["decl"])
            if "baseType" in element[field].keys():
                return element[field]["baseType"]
            if "modifiers" in element[field].keys():
                pass
        if field == "baseType":
            return element[field]

    def get_parameters(self, function, location):
        data = self.parsed["declarations"]
        parameters = []
        for element in data:
            if (
                re.match("cpp\+parameter", element[0])
                and function in element[0]
                and location in element[1]
                and re.match("\|file:\/+.+.\|", element[1])
            ):
                parameter = {}
                parameter["name"] = re.sub("cpp\+parameter:\/+.+\/", "", element[0])
                parameter["location"] = int(
                    re.split(",", re.sub("\|file:\/+.+\|\(", "", element[1]))[0]
                )
                parameters.append(parameter)
        parameters = sorted(parameters, key=lambda d: d["location"])
        return parameters

    def get_classes_location(self, c):
        data = self.parsed["functionDefinitions"]
        location = {}
        for element in data:
            if re.match("cpp\+constructor:\/+\/" + c, element[0]) and c in element[0]:
                location["file"], location["position"] = re.split("\(", element[1])
                location["file"] = re.sub("\|file:.+/", "", location["file"])[:-1]
                location["position"] = "(" + location["position"]
                break
        return location

    def get_classes(self):
        data = self.parsed["containment"]
        classes = {}
        for element in data:
            if len(element) > 1:
                if re.match("cpp\+class", element[0]):
                    c = {}
                    if re.match("cpp\+constructor", element[1]):
                        c["className"] = re.split(
                            "\(", re.sub("cpp\+constructor:\/+.+\/", "", element[1])
                        )[0]
                        extends = self.parsed["extends"]
                        c["extends"] = None
                        for el in extends:
                            if el[1] == element[0]:
                                c["extends"] = re.sub("cpp\+class:\/+", "", el[0])
                                break
                        c["location"] = self.get_classes_location(c["className"])
                        id = c["className"]
                        classes[id] = c
        return classes

    def get_invokes(self, operations):
        data = self.parsed["callGraph"]
        invokes = []
        for operation in operations.items():
            for element in data:
                if re.match(".+\.", operation[0]):
                    source = operation[0].replace(".", "/")
                else:
                    source = operation[0]
                if source in element[0]:
                    invoke = {}
                    invoke["source"] = operation[0]
                    try:
                        target = re.sub("cpp\+function:\/+.+\/", "", element[1])
                        if re.match("cpp\+", target):
                            target = re.sub("cpp\+method:\/+", "", element[1])
                            target = target.replace("/", ".")
                        target = re.split("\(", target)[0]
                        
                        if target in operations.keys():
                            invoke["target"] = target
                            invokes.append(invoke)
                    except:
                        pass
                else:
                    pass
        return invokes

    def export(self):
        for file in self.get_files():
            self.add_nodes("file", file)
        functions = self.get_functions()

        for func in functions.items():
            self.add_nodes("function", func, None)
            if func[1]["parameters"]:
                self.add_nodes("parameter", func)
                self.add_edges("hasParameter", func)
            self.add_edges("contains", func)
        for c in self.get_classes().items():
            self.add_nodes("class", c)
            if c[1]["extends"] is not None:
                self.add_edges("specializes", c)
            self.add_edges("contains", c)
        methods = self.get_methods()
        for m in methods.items():
            self.add_nodes("method", m)
            self.add_edges("hasScript", m)
        operations = deepcopy(methods)
        operations.update(functions)
        for invoke in self.get_invokes(operations):
            self.add_edges("invokes",invoke)
        with open(os.path.join(self.path, "converted.json"), "w") as f:
            f.write(json.dumps(self.viz))
