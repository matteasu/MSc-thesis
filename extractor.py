import requests
import re
import os
import json
def mate_poi_extractor(buildID, serverURL):
    issues = []
    session = requests.session()
    try:
        request = session.get("{}/api/v1/pois/build/{}".format(serverURL, buildID))
        if request.status_code == 200:
            response = request.json()
            for el in response:
                issue = {}
                words = re.findall(
                    r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", el["analysis_name"]
                )
                name = ""
                for w in words:
                    name += w + " "
                name = name.strip()
                issue["analysis_name"] = name
                target=re.split(":", el["poi"]["sink"], maxsplit=3)[-1]
                target = re.split(":", target)
                if len(target)>1:
                    target=target[0]+"."+target[-1]
                else:
                    target=target[-1]
                target = re.split("\(",target)[0]

                issue["target"] = {
                    "file": re.split(":", el["poi"]["sink"])[0],
                    "location": re.split(":", el["poi"]["sink"])[1]
                    + ":"
                    + re.split(":", el["poi"]["sink"])[2],
                    "script": target,
                }
                issue["description"] = el["poi"]["insight"]
                issues.append(issue)
        elif request.status_code == 404:
            raise AttributeError("No build with id {} was found".format(buildID))
    except:
        raise AttributeError("Can't reach server at {}".format(serverURL))
    return issues

def infer_extractor(path):
    issues = []
    with open(os.path.join(path,'infer-out/report.json'),'r') as f:
        parsed = json.load(f)
        for el in parsed:
            issue = {}
            issue["analysis_name"] = el["bug_type_hum"]
            split = re.split("::",el["procedure"])
            if len(split)>1 :
                if split[0] == split[1]:
                    script = split[0]
                else:
                    script = split[0]+"."+split[1]
            else:
                script = split[0]
            issue["target"] = {
                "file": el["file"],
                "location": str(el["line"])+":"+str(el["column"]),
                "script": script,
            }
            issue["description"] = el["qualifier"]
            issues.append(issue)
    return issues
