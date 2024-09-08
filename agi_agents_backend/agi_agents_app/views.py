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
    pricing_filter = request.GET.getlist('pricing')
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
                "id":agent[0],
                "name": agent[1],
                "description": agent[2],
                "email":agent[8],
                "overview": agent[11],
                "key_features": agent[12],
                "use_cases": agent[13],
                "details": {
                     "created_by": agent[14],
                    "category": agent[3],
                    "industry": agent[4],
                     "pricing": agent[5],
                     "access": agent[15],
                    #  "date_added": agent[7].strftime('%Y-%m-%d') ,
                            },
                "website_url": agent[7],
                "preview_image": agent[17],
                "logo":agent[18],
            }
            return JsonResponse({'agent': agent_data})
        else:
            return HttpResponseNotFound(JsonResponse({'error': 'Agent not found'}))
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# 3. Agent Create View
@csrf_exempt
def agent_create(request):
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                # Convert any array fields into proper arrays (handling empty strings)
                key_features = data.get('key_features', '')
                use_cases = data.get('use_cases', '')
                tags = data.get('tags', '')

                # Handle empty strings by converting them to empty arrays
                key_features_array = key_features.split(',') if key_features else []
                use_cases_array = use_cases.split(',') if use_cases else []
                tags_array = tags.split(',') if tags else []

                # Create new agent
                new_agent_id = db.add_agent(
                    name=data.get('name'),
                    description=data.get('description'),
                    category=data.get('category'),
                    industry=data.get('industry'),
                    pricing=data.get('pricing'),
                    accessory_model=data.get('accessory_model'),
                    website_url=data.get('website_url'),
                    email=data.get('email'),
                    tagline=data.get('tagline'),
                    likes=data.get('likes', 0),
                    overview=data.get('overview'),
                    key_features=key_features_array,  # Use array
                    use_cases=use_cases_array,        # Use array
                    created_by=data.get('created_by'),
                    access=data.get('access'),
                    tags=tags_array,                 # Use array
                    preview_image=data.get('preview_image'),
                    logo=data.get('logo'),
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
