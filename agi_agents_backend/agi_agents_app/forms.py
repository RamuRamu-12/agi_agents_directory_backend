from django import forms
from .models import Agent


class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = [
            'name', 
            'description', 
            'category', 
            'industry', 
            'pricing', 
            'accessory_model', 
            'website_url', 
            'email',
            'tagline',
            'likes',
            'overview',
            'key_features',
            'use_cases',
            'created_by',
            'access',
            'tags',
            'preview_image',
            'logo',
            'demo_video'
        ]


