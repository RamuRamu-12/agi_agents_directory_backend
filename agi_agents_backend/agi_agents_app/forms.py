from django import forms
from .models import Agent

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['name', 'description', 'category', 'industry', 'pricing_model', 'accessory_model', 'website_url']

