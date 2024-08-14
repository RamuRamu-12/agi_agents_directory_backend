# agents/urls.py

from django.urls import path
from .views import agent_list, agent_detail, agent_create

urlpatterns = [
    path('agent_list', agent_list, name='agent-list'),
    path('agents_detail/<int:id>', agent_detail, name='agent-detail'),
    path('agents_create', agent_create, name='agent-create'),
]
