from django.db import models

import json

# Add encrytprion in the future
class UserMemory(models.Model):
    username = models.CharField(max_length=50)

    dates = models.JSONField(default=dict, null=True)
    generalMemory = models.CharField(max_length=1024, null=True)

    def getUserMemory(self):
        memory = {
            "name": self.username,
            "dates": self.dates,
            "generalMemory": self.generalMemory,
        }

        return json.dumps(memory)

    def addUserMemory(self, dates, generalMemory):
        separator = ''
        generalMemoryStr = ''

        for memDict in generalMemory:
            generalMemoryStr += separator.join(memDict.values())  

        self.generalMemory = (self.generalMemory or "") + generalMemoryStr
        self.dates = (self.dates or []) + dates
        print(self.dates)
        self.save()

        
