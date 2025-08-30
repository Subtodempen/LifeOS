from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .forms import PromptInput
from .gpt_agent import gptWrapper

from .models import UserMemory
import json

from django.views import View
from django.utils.decorators import method_decorator

@method_decorator(login_required, name="dispatch")
class indexPrompt(View):
    def __init__(self):
        self.chatGPTWrapper = gptWrapper()
        self.chatGPTWrapper.initClient() # maybe move

    def post(self, request):
        form = PromptInput(request.POST)
        userDataModel = self.getUserModel(request.user.username)
        
        message = None

        if form.is_valid():
            formData = form.cleaned_data
            
            prompt = formData["prompt"]
            memory = userDataModel.getUserMemory()
            print(memory)
            try:
                result = self.handlePrompt(prompt, memory)
                jsonResult = self.serializeJson(result)

                message, dates, generalMemory = self.parseJSONResult(jsonResult)
                userDataModel.addUserMemory(dates, generalMemory)
            
            except ValueError as v:
                message = f"could not handle json produced {v}"

            except Exception as e:
                message = f"GPT failed with error: {e}"

        return render(request, 'agents/chat.html', {"message": message})
    
    
    def get(self, request):
        return render(request, 'agents/chat.html')
    

    def getUserModel(self, username):
        try:
            userDataModel = UserMemory.objects.get(username = username) 

        except ObjectDoesNotExist:
            # create an empty object for userr
            userDataModel = UserMemory(
                username = username,
                dates = None,
                generalMemory = None,
            )

            userDataModel.save()

        return userDataModel


    def handlePrompt(self, prompt, memory):
        # get memory from gpt on this current user
        # post it with JSON
        prompt = {"metadata": memory, "prompt": prompt}
        return self.chatGPTWrapper.generateResponse(json.dumps(prompt))

    
    def parseJSONResult(self, jsonResult):
        return (jsonResult.get("response"), jsonResult.get("dates"), jsonResult.get("general_memory_updates"))

    # will raise a runtime json error if gpt has incorrect format
    def serializeJson(self, jsonResult):
        return json.loads(jsonResult)

    

