# agents/urls.py

from django.urls import path
from .views import agent_list, agent_detail, agent_create, modify_agent,add_email

urlpatterns = [
    path('agent_list', agent_list, name='agent-list'),
    path('agents_detail/<int:id>', agent_detail, name='agent-detail'),
    path('agents_create', agent_create, name='agent-create'),
    #path('admin/agent/<int:agent_id>/<str:action>/', approve_or_reject_agent, name='approve_or_reject_agent'),
    path('agent/<int:agent_id>/modify/', modify_agent , name='modify_agent'),
    path('add_email', add_email, name='add_email')
]
