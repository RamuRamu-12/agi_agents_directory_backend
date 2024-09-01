from django.shortcuts import render
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .database import PostgreSQLDB  
from .forms import AgentForm  

# Initialize database connection
db = PostgreSQLDB(dbname='uibmogli', user='uibmogli', password='8ogImHfL_1G249lXtM3k2EAIWTRDH2mX')

# 1. Agent List View with search, filter, and sort
@csrf_exempt
def agent_list(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.getlist('category')
    industry_filter = request.GET.getlist('industry')
    pricing_filter = request.GET.getlist('pricing_model')
    accessory_filter = request.GET.getlist('accessory_model')
    sort_option = request.GET.get('sort', 'date_added')
    
    try:
        agents = db.get_filtered_agents(
            search_query=search_query,
            category_filter=category_filter,
            industry_filter=industry_filter,
            pricing_filter=pricing_filter,
            accessory_filter=accessory_filter,
            sort_option=sort_option
        )
        return JsonResponse({'agents': agents}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# 2. Agent Detail View
@csrf_exempt
def agent_detail(request, id):
    try:
        agent = db.get_agent_by_id(id)
        
        if agent:
            agent_data = {
                'id': agent[0],  # Assuming the first field is 'id'
                'name': agent[1],
                'description': agent[2],
                'category': agent[3],
                'industry': agent[4],
                'pricing_model': agent[5],
                'accessory_model': agent[6],
                'website_url': agent[7],
                'tagline': agent[8],
                'likes': agent[9],
                'overview': agent[10],
                'key_features': agent[11],
                'use_cases': agent[12],
                'created_by': agent[13],
                'access': agent[14],
                'tags': agent[15],
                'preview_image': agent[16],
                'demo_video': agent[17],
                'date_added': agent[18],
            }
            return JsonResponse({'agent': agent_data})
        else:
            return HttpResponseNotFound(JsonResponse({'error': 'Agent not found'}))
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# 3. Agent Create View
# 3. Agent Create View
@csrf_exempt
def agent_create(request):
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                new_agent_id = db.add_agent(
                    name=data['name'],
                    description=data['description'],
                    category=data['category'],
                    industry=data['industry'],
                    pricing_model=data['pricing_model'],
                    accessory_model=data['accessory_model'],
                    website_url=data['website_url'],
                    tagline=data.get('tagline'),
                    likes=data.get('likes', 0),
                    overview=data.get('overview'),
                    key_features=data.get('key_features'),
                    use_cases=data.get('use_cases'),
                    created_by=data.get('created_by'),
                    access=data.get('access'),
                    tags=data.get('tags'),
                    preview_image=data.get('preview_image'),
                    demo_video=data.get('demo_video')
                )
                if new_agent_id:
                    return JsonResponse({'message': 'Agent created successfully', 'agent_id': new_agent_id})
                else:
                    return JsonResponse({'error': 'Failed to create agent'}, status=500)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
