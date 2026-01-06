from enum import Enum
import requests

class Role(Enum) :
    CHAIRMAN = 0
    COUNCILOR = 1
    USER = 2

class ModelType(Enum):
    DEFAULT= 0
    CUSTOM = 1

class CouncilModel() :

    count : int = 0

    def __init__(self, 
        ip : str = "localhost", 
        port : int = 11434, 
        model_name : str = "model", 
        role : int = Role.COUNCILOR,
        prompt : str | None = None,
        custom_name : str | None = None):

        # Connection settings
        self.ip : str = ip
        self.port : int = port

        # Model parameters
        self.base_model : str = model_name
        self.model_name : str = model_name
        self.model_role : int = role

        self.model_type : int = ModelType.DEFAULT

        self.prompt : str | None = prompt

        print(prompt)
        print(custom_name)

        if prompt and custom_name:
            self.model_type = ModelType.CUSTOM # Change model type
            self.model_name = custom_name # Update name of custom model

        # Identifier
        self.id = self.count
        self.count += 1

    def pull(self):

        url = f"http://{self.ip}:{self.port}/api/pull"
        
        payload = {
            "model" : self.base_model
        }

        req = requests.post(url, json=payload)

    def create(self) :

        print("Creating new model !")

        if not self.prompt :
            print("Cannot create cutsom model without prompt !")
            return

        url = f"http://{self.ip}:{self.port}/api/create"
        
        payload = {
            "model" : self.model_name,
            "from" : self.base_model,
            "system" : self.prompt
        }

        req = requests.post(url, json=payload)


    def healthcheck(self):

        url = f"http://{self.ip}:{self.port}/api/tags"

        req = requests.get(url)

        print(req)