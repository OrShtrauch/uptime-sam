import os
import time
import base64
import json
import requests
import multiprocessing

from flask import Flask, request, Response

RPI = "rpi"
AUTOMATION = "Automation"

username: str = os.environ.get('USERNAME')
password: str = os.environ.get('PASSWORD')
url: str = os.environ.get('URL')
interval: int = int(os.environ.get('INTERVAL'))
file_name: str = os.environ.get('FILE_NAME')
port: str = os.environ.get('PORT')

def fetch_data():    
    auth = f"{username}:{password}"
    auth_bytes = auth.encode('ascii')
    base64_bytes = base64.b64encode(auth_bytes)
    base64_message = base64_bytes.decode('ascii')

    headers = { "Authorization": f"Basic {base64_message}" }

    try:
        data =  requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        return None

    return data.json().get("resources")

def process_data(resources, rpi_dict):
    if not rpi_dict:
        return 
    
    for resource in resources:
        if RPI not in resource.get('labels'):
            continue

        display_name = "R"
        name = resource.get('name')

        # e.g. 1.11 -> [1, 11]
        split_name = name.split('.')

        first_number = int(split_name[0])

        if first_number < 10:
            display_name += "0"

        display_name += f"{first_number}-"


        second_number = int(split_name[1])
        display_name += f"S{second_number}"

        reserved = resource.get('reservedBy')

        try:
            if AUTOMATION in resource.get('buildName'):
                reserved = "Jenkins CI"
        except TypeError:
            pass

        if not reserved:
            reserved = "Free"

        rpi_dict["resources"][display_name] = reserved
    return rpi_dict

def do():
    rpi_dict = {"resources": {}}

    while True:
        resources = fetch_data()
        rpi_dict = process_data(resources, rpi_dict)

        with open(file_name, "w") as fd:
            json.dump(rpi_dict, fd)

        time.sleep(interval)


app = Flask(__name__)

@app.route("/", methods=["GET"])
def get_resources():                
        with open(file_name, "r") as fd:
            data = fd.read()                        
        
        resp = Response(json.dumps(data), status=200)
        resp.headers['Access-Control-Allow-Origin'] = '*'

        return resp

@app.route("/resource/<name>", methods=["GET"])
def get_resource(name):
        with open(file_name, "r") as fd:
            data = fd.read()                        
        
        try:
            data = json.loads(data).get("resources")
        except Exception:
            data = {}


        resp = Response(json.dumps({ "title": data.get(name) }), status=200)
        resp.headers['Access-Control-Allow-Origin'] = '*'

        return resp        

if __name__ == '__main__':
    p = multiprocessing.Process(target=do)
    p.start()
    

    app.run("0.0.0.0", port)

