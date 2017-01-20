import hashlib
import hmac
import math
import time
from enum import Enum

import requests

current_base_url = "https://www.cs.utexas.edu/users/mad/utcs-app-backend/staging/cgi-bin/utcs.scgi"


class UTCSService(Enum):
    Labs = 0,
    LabsLayout = 1

    def __str__(self):
        if self is UTCSService.Labs:
            return "labs"
        elif self is UTCSService.LabsLayout:
            return "labs-layout"


class UTCSBackend:
    def __init__(self, api_key: str, base_url: str = current_base_url):
        self.key = api_key
        self.base_url = current_base_url

    def request(self, service: UTCSService):
        url = self._create_url(service)
        headers = self._create_headers(service)
        response = requests.get(url, headers=headers)
        if service is UTCSService.Labs:
            return LabsResponse(response.json())
        elif service is UTCSService.LabsLayout:
            return LabsLayoutResponse(response.json())

    def _create_url(self, service: UTCSService):
        return self.base_url + "?service=" + str(service)

    def _create_headers(self, service: UTCSService):
        digest = UTCSBackend._makedigest(str(service), None, self.key)
        return {"authentication": "hmac web:" + digest}

    @staticmethod
    def _makedigest(service, arg, key):
        if arg is None:
            arg = ""
        timestamp = math.floor(int(time.time()) / 30)
        keyasbytes = key.encode()
        message = (str(service) + str(arg) + str(timestamp)).encode()
        digester = hmac.new(keyasbytes, message, hashlib.sha1)

        return digester.hexdigest()


class LabMachine:
    def __init__(self, json):
        self.name = json.get("name")
        self.occupied = json.get("occupied")
        self.up = json.get("up")
        self.uptime = json.get("uptime")
        self.load = json.get("load")
        self.users = json.get("users")
        self.location = (0, 0)
        self.lab = json.get("lab")

    @staticmethod
    def get_empty():
        return LabMachine({})


class LabsResponse:
    def __init__(self, json):
        self.machines = [{}, {}]
        if json["meta"]["success"]:
            machines = json["values"]
            for entry in machines:
                machine = LabMachine(entry)
                if machine.lab == "third":
                    self.machines[0][machine.name] = machine
                else:
                    self.machines[1][machine.name] = machine


class LabsLayoutResponse:
    def __init__(self, json):
        self.machines_layout = [{}, {}]
        self.dimensions = []
        if json["meta"]["success"]:
            third = json["values"][0]
            basement = json["values"][1]
            third_dimensions = third["dimensions"]
            basement_dimensions = basement["dimensions"]
            self.dimensions.append(
                (int(third_dimensions["width"]), int(third_dimensions["height"])))
            self.dimensions.append(
                (int(basement_dimensions["width"]), int(basement_dimensions["height"])))
            third_machines = third["layout"]
            basement_machines = basement["layout"]
            for entry in third_machines:
                name = entry["name"]
                x = float(entry["x"])
                y = float(entry["y"])
                self.machines_layout[0][name] = (
                    x / self.dimensions[0][0], y / self.dimensions[0][1])

            for entry in basement_machines:
                name = entry["name"]
                x = float(entry["x"])
                y = float(entry["y"])
                self.machines_layout[1][name] = (
                    x / self.dimensions[0][0], y / self.dimensions[0][1])
