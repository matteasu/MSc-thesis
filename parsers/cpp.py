import re
class Cpp:
    primitives = ["int", "float", "void", "char", "string", "boolean"]
    viz = {"elements": {"nodes": [], "edges": []}}

    def __init__(self) -> None:
        pass

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
                edge_id = edge_id + hash(other[content[1]["functionName"]]["location"]["file"])
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
