from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Agent
from .forms import AgentForm
from django.views.decorators.csrf import csrf_exempt

# 1. Agent List View with search, filter, and sort

@csrf_exempt
def agent_list(request):
    agents = Agent.objects.all()

    # Search filter
    search_query = request.GET.get('search', '')
    if search_query:
        agents = agents.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Category filter
    category_filter = request.GET.getlist('category')
    if category_filter:
        agents = agents.filter(category__in=category_filter)

    # Industry filter
    industry_filter = request.GET.getlist('industry')
    if industry_filter:
        agents = agents.filter(industry__in=industry_filter)

    # Pricing model filter
    pricing_filter = request.GET.getlist('pricing_model')
    if pricing_filter:
        agents = agents.filter(pricing_model__in=pricing_filter)

    # Accessory model filter
    accessory_filter = request.GET.getlist('accessory_model')
    if accessory_filter:
        agents = agents.filter(accessory_model__in=accessory_filter)

    # Sorting
    sort_option = request.GET.get('sort', 'date_added')
    if sort_option == 'name_asc':
        agents = agents.order_by('name')
    elif sort_option == 'name_desc':
        agents = agents.order_by('-name')
    elif sort_option == 'oldest':
        agents = agents.order_by('date_added')
    else:
        agents = agents.order_by('-date_added')

    agent_list = list(agents.values())
    return JsonResponse({'agents': agent_list}, safe=False)



# 2. Agent Detail View
@csrf_exempt
def agent_detail(request, id):
    # Fetch the agent object from the database
    agent = get_object_or_404(Agent, id=id)
    
    # Prepare the data to be returned in the response
    agent_data = {
        'id': agent.id,
        'name': agent.name,
        'description': agent.description,
        'category': agent.category,
        'industry': agent.industry,
        'pricing_model': agent.pricing_model,
        'accessory_model': agent.accessory_model,
        'website_url': agent.website_url,
        'tagline': agent.tagline,
        'likes': agent.likes,
        'overview': agent.overview,
        'key_features': agent.key_features,
        'use_cases': agent.use_cases,
        'created_by': agent.created_by,
        'access': agent.access,
        'tags': agent.tags,
        'preview_image': agent.preview_image,
        'demo_video': agent.demo_video,
        'date_added': agent.date_added,
    }
    # Return the agent data as a JSON response
    return JsonResponse({'agent': agent_data})



# 3. Agent Create View
@csrf_exempt
def agent_create(request):
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            agent = form.save()
            return JsonResponse({'message': 'Agent created successfully', 'agent_id': agent.id})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)


