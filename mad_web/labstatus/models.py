import hashlib
import hmac
from enum import Enum

import requests

current_base_url = "https://www.cs.utexas.edu/users/mad/utcs-app-backend/1.0/cgi-bin/utcs.scgi"


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
        keyasbytes = key.encode()
        message = (str(service) + str(arg)).encode()
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

    @staticmethod
    def get_empty():
        return LabMachine({})


class LabsResponse:
    def __init__(self, json):
        self.machines = [{}, {}]
        if json["meta"]["success"]:
            labs = json["values"]
            for entry in labs[0]["machines"]:
                self.machines[0][entry["name"]] = LabMachine(entry)
            for entry in labs[1]["machines"]:
                self.machines[1][entry["name"]] = LabMachine(entry)


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
                (int(third_dimensions["maximumGridWidth"]), int(third_dimensions["maximumGridHeight"])))
            self.dimensions.append(
                (int(basement_dimensions["maximumGridWidth"]), int(basement_dimensions["maximumGridHeight"])))
            third_machines = third["layout"]
            basement_machines = basement["layout"]
            for name, coord in third_machines.items():
                self.machines_layout[0][name] = (
                    float(coord["x"]) / self.dimensions[0][0], float(coord["y"]) / self.dimensions[0][1])

            for name, coord in basement_machines.items():
                self.machines_layout[1][name] = (
                    float(coord["x"]) / self.dimensions[1][0], float(coord["y"]) / self.dimensions[1][1])
