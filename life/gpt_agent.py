from openai import OpenAI

from pathlib import Path
import os

from dotenv import load_dotenv
from django.conf import settings

class gptWrapper:
    def __init__(self):
        self.model = "gpt-5-mini"
        self.instructions = None
        self.client = None

    def initClient(self, ):
        key = os.getenv('OPENAI_API_KEY')
        
        load_dotenv()
        self.loadInstructions()

        self.client = OpenAI(
            api_key = key
        )


    def loadInstructions(self):
        promptFile = Path(settings.PROMPT_FILE)

        if promptFile.exists():
            with open(promptFile, "r", encoding="utf-8") as f:
                self.instructions = f.read()

        else:
            raise RuntimeError("No instructions in path")


    def generateResponse(self, prompt):
        if self.client == None:
            raise RuntimeError("No client loaded")
        
        response = self.client.responses.create(
            model = self.model,
            instructions = self.instructions,
            input = prompt
        )

        return response.output_text
