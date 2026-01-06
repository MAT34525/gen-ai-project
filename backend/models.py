from enum import Enum
import requests

class Role(Enum) :
    CHAIRMAN = 0
    COUNCILOR = 1
    USER = 2

class CouncilModel() :

    count : int = 0

    def __init__(self, ip : str = "localhost", port : int = 11434, model_name : str = "model", role : int = Role.COUNCILOR ):

        # Connection settings
        self.ip : str = ip
        self.port : int = port

        # Model parameters
        self.model_name : str = model_name
        self.model_role : int = role

        # Identifier
        self.id = self.count
        self.count += 1

    def pull(self):

        url = f"http://{self.ip}:{self.port}/api/pull"
        
        payload = {
            "model" : self.model_name
        }

        req = requests.post(url, json=payload)


    def healthcheck(self):

        url = f"http://{self.ip}:{self.port}/api/tags"

        req = requests.get(url)

        print(req)