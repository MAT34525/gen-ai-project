from enum import Enum
import requests
import textwrap
import re
import json

IP_REGEX = r"^([0-9a-z\-]+[.]?)+([0-9a-z\-]+)?$"

class Role(Enum) :
    CHAIRMAN = 0
    COUNCILOR = 1
    USER = 2

class ModelType(Enum):
    DEFAULT= 0
    CUSTOM = 1

class CouncilModel() :
    """
    Create an instance of a council model with connection and model settings.

    Returns:
        _type_: _description_
    """

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

        if not re.search(IP_REGEX, self.ip) :
            raise SyntaxError(f"Invalid IP format : {self.ip} !")

        # Model parameters
        self.base_model : str = model_name
        self.model_name : str = model_name
        self.model_role : int = role

        # Pull base model
        self.pull()

        # Load propt if applicable
        self.model_type : int = ModelType.DEFAULT
        self.prompt : str | None = prompt

        if prompt and custom_name:
            self.model_type = ModelType.CUSTOM # Change model type
            self.model_name = custom_name # Update name of custom model
            self.create() # Create new model from base model

        # Identifier
        self.id = self.count
        self.count += 1            

        # Display object summary
        print(self)

    # def status(self) -> dict :

    def pull(self) -> None:
        """Pull model from attributes"""

        print(f"Pulling model for {self.host}")

        url = f"http://{self.host}/api/pull"
        
        payload = {
            "model" : self.base_model
        }

        try :
            req = requests.post(url, json=payload)
            req.raise_for_status()

            print(f"Successfully pulled model : {self.model_name} for {self.host}")
        
        except (requests.HTTPError, requests.exceptions.ConnectionError) as e :
            print(f"Failed to pull the model : {e}")

    def create(self) -> None:
        """Create new model from system prompt."""

        print(f"Creating new model for {self.host}")

        if not self.prompt :
            print("Cannot create cutsom model without prompt !")
            return

        url = f"http://{self.host}/api/create"
        
        payload = {
            "model" : self.model_name,
            "from" : self.base_model,
            "system" : self.prompt
        }

        try :
            req = requests.post(url, json=payload)
            req.raise_for_status()

            print(f"Successfully created model : {self.model_name} from {self.base_model} for {self.host} : {req}")
        
        except (requests.HTTPError, requests.exceptions.ConnectionError) as e :
            print(f"Failed to create the model : {e}")


    def fetch_available_models(self) -> dict:
        """Fetch available models from ollama host."""

        url = f"http://{self.ip}:{self.port}/api/tags"

        models = {}

        try: 
            req = requests.get(url)
            req.raise_for_status()

            models = req.json()

            print(models)

        except (requests.HTTPError, requests.exceptions.ConnectionError) as e :
            print(f"Failed to fetch availbale models from {self.host} : {e}")
        
        return models




    def healthcheck(self) -> bool:

        url = f"http://{self.ip}:{self.port}/api/tags"

        req = requests.get(url)

        print(req)

    @property
    def host(self) -> str :
        return f"{self.ip}:{self.port}"

    def __str__(self) -> str:
        """Description of CouncilModel."""

        base = textwrap.dedent(f"""
        Council model :
        - Role : {"CHAIRMAIN" if self.model_role == Role.CHAIRMAN else "COUNCILOR"}
        - Base model : {self.base_model}
        - Host : {self.ip}:{self.port}
        - Custom prompt : {self.prompt is not None}
        """)

        opt = textwrap.dedent("""
        - Prompt : {self.prompt}
        - Model name : {self.model_name}
        """)

        message = base + (opt if self.prompt else "")

        return message
