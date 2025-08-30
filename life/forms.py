from django import forms


class PromptInput(forms.Form):
    prompt = forms.CharField(label="prompt", max_length=512)

