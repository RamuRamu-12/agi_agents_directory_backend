from django.shortcuts import render
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .database import PostgreSQLDB  
from .forms import AgentForm, AgentUpdateForm  


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



#Agent Create Api
from django.conf import settings  # Import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
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

                # Add agent to the database via PostgreSQLDB
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
                    key_features=key_features_array,
                    use_cases=use_cases_array,
                    created_by=data.get('created_by'),
                    access=data.get('access'),
                    tags=tags_array,
                    preview_image=data.get('preview_image'),
                    logo=data.get('logo'),
                    demo_video=data.get('demo_video'),
                    is_approved=False  # New agents are not approved by default
                )

                if new_agent_id:
                    # URLs for approving and rejecting the agent
                    approve_url = f'{settings.SITE_URL}/api/admin/agent/{new_agent_id}/approve/'
                    reject_url = f'{settings.SITE_URL}/api/admin/agent/{new_agent_id}/reject/'
                    modify_url = f'{settings.SITE_URL}/api/agent/{new_agent_id}/modify/'
                    # Email content with all the agent details
                    email_content = f"""
                    <h3>New Agent Created</h3>
                    <p>An agent "<strong>{data.get('name')}</strong>" (Agent ID: {new_agent_id}) has been created and requires approval.</p>
                    <h4>Agent Details</h4>
                    <ul>
                        <li><strong>Name:</strong> {data.get('name')}</li>
                        <li><strong>Description:</strong> {data.get('description')}</li>
                        <li><strong>Category:</strong> {data.get('category')}</li>
                        <li><strong>Industry:</strong> {data.get('industry')}</li>
                        <li><strong>Pricing:</strong> {data.get('pricing')}</li>
                        <li><strong>Accessory Model:</strong> {data.get('accessory_model')}</li>
                        <li><strong>Website URL:</strong> {data.get('website_url')}</li>
                        <li><strong>Email:</strong> {data.get('email')}</li>
                        <li><strong>Tagline:</strong> {data.get('tagline')}</li>
                        <li><strong>Likes:</strong> {data.get('likes', 0)}</li>
                        <li><strong>Overview:</strong> {data.get('overview')}</li>
                        <li><strong>Key Features:</strong> {', '.join(key_features_array)}</li>
                        <li><strong>Use Cases:</strong> {', '.join(use_cases_array)}</li>
                        <li><strong>Created By:</strong> {data.get('created_by')}</li>
                        <li><strong>Access:</strong> {data.get('access')}</li>
                        <li><strong>Tags:</strong> {', '.join(tags_array)}</li>
                        <li><strong>Preview Image:</strong> {data.get('preview_image')}</li>
                        <li><strong>Logo:</strong> {data.get('logo')}</li>
                        <li><strong>Demo Video:</strong> {data.get('demo_video')}</li>
                    </ul>
                    <p>Please choose one of the options below:</p>
                    <a href="{approve_url}" style="background-color:green;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">Approve</a>
                    &nbsp;
                    
                    <a href="{reject_url}" style="background-color:red;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">Reject</a>
                    &nbsp;
                    <a href="{modify_url}" style="background-color:blue;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">Edit</a>
                    
                    <p>Thank you!</p>
                    """

                    # Send email to admin for approval
                    send_mail(
                        'New Agent Approval Required',
                        'A new agent has been created and requires your approval.',  # Plain text fallback
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.ADMIN_EMAIL],
                        fail_silently=False,
                        html_message=email_content  # Send the HTML email content
                    )

                    return JsonResponse({
                        'message': 'Agent created successfully and sent for approval',
                        'agent_id': new_agent_id
                    })
                else:
                    return JsonResponse({'error': 'Failed to add agent to the database'}, status=500)

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)



#Approval or reject api
from django.conf import settings  # Import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def approve_or_reject_agent(request, agent_id, action):
    if request.method == 'GET':
        # Retrieve the agent by ID
        agent = db.get_agent_by_id(agent_id)

        if not agent:
            return JsonResponse({'error': 'Agent not found'}, status=404)

        try:
            if action == 'approve':
                # Update the agent as approved
                db.update_agent(
                    agent_id=agent_id,
                    name=agent[1],
                    description=agent[2],
                    category=agent[3],
                    industry=agent[4],
                    pricing=agent[5],
                    accessory_model=agent[6],
                    website_url=agent[7],
                    email=agent[8],
                    tagline=agent[9],
                    likes=agent[10],
                    overview=agent[11],
                    key_features=agent[12],
                    use_cases=agent[13],
                    created_by=agent[14],
                    access=agent[15],
                    tags=agent[16],
                    preview_image=agent[17],
                    logo=agent[18],
                    demo_video=agent[19],
                    is_approved=True  # Set the agent as approved
                )

                # Email content with all the agent details
                email_content = f"""
                <h3>Your Agent Has Been Approved</h3>
                <p>Congratulations! Your agent "<strong>{agent[1]}</strong>" has been approved.</p>
                <h4>Agent Details</h4>
                <ul>
                    <li><strong>Name:</strong> {agent[1]}</li>
                    <li><strong>Description:</strong> {agent[2]}</li>
                    <li><strong>Category:</strong> {agent[3]}</li>
                    <li><strong>Industry:</strong> {agent[4]}</li>
                    <li><strong>Pricing:</strong> {agent[5]}</li>
                    <li><strong>Accessory Model:</strong> {agent[6]}</li>
                    <li><strong>Website URL:</strong> {agent[7]}</li>
                    <li><strong>Email:</strong> {agent[8]}</li>
                    <li><strong>Tagline:</strong> {agent[9]}</li>
                    <li><strong>Likes:</strong> {agent[10]}</li>
                    <li><strong>Overview:</strong> {agent[11]}</li>
                    <li><strong>Key Features:</strong> {', '.join(agent[12])}</li>
                    <li><strong>Use Cases:</strong> {', '.join(agent[13])}</li>
                    <li><strong>Created By:</strong> {agent[14]}</li>
                    <li><strong>Access:</strong> {agent[15]}</li>
                    <li><strong>Tags:</strong> {', '.join(agent[16])}</li>
                    <li><strong>Preview Image:</strong> {agent[17]}</li>
                    <li><strong>Logo:</strong> {agent[18]}</li>
                    <li><strong>Demo Video:</strong> {agent[19]}</li>
                </ul>
                <p>Thank you for your submission!</p>
                """

                # Notify the agent creator that their agent has been approved with all details
                send_mail(
                    'Your Agent is Approved',
                    f'Agent "{agent[1]}" has been approved.',  # Plain text fallback
                    settings.DEFAULT_FROM_EMAIL,
                    [agent[8]],  # Send to the agent creator's email
                    fail_silently=False,
                    html_message=email_content  # Send the HTML email content
                )

                return JsonResponse({'message': 'Agent approved successfully'})

            elif action == 'reject':
                # Delete the agent if rejected
                db.delete_agent(agent_id)

                # Notify the agent creator that their agent has been rejected
                send_mail(
                    'Your Agent is Rejected',
                    f'Agent "{agent[1]}" has been rejected.',
                    settings.DEFAULT_FROM_EMAIL,
                    [agent[8]],  # Send to the agent creator's email
                    fail_silently=False,
                )

                return JsonResponse({'message': 'Agent rejected and deleted successfully'})

            else:
                return JsonResponse({'error': 'Invalid action'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)





#agent_update_form
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
# API for modifying agent details by admin
@csrf_exempt
def modify_agent(request, agent_id):
    if request.method == 'POST':
        form = AgentUpdateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                # Fetch the existing agent by ID
                agent = db.get_agent_by_id(agent_id)
                if not agent:
                    return JsonResponse({'error': 'Agent not found'}, status=404)

                # Handle key features, use cases, and tags arrays
                key_features = data.get('key_features', agent[12])
                use_cases = data.get('use_cases', agent[13])
                tags = data.get('tags', agent[16])

                key_features_array = key_features.split(',') if key_features else agent[12]
                use_cases_array = use_cases.split(',') if use_cases else agent[13]
                tags_array = tags.split(',') if tags else agent[16]

                # Update the agent's details in the database
                db.update_agent(
                    agent_id=agent_id,
                    name=data.get('name', agent[1]),
                    description=data.get('description', agent[2]),
                    category=data.get('category', agent[3]),
                    industry=data.get('industry', agent[4]),
                    pricing=data.get('pricing', agent[5]),
                    accessory_model=data.get('accessory_model', agent[6]),
                    website_url=data.get('website_url', agent[7]),
                    email=data.get('email', agent[8]),
                    tagline=data.get('tagline', agent[9]),
                    likes=data.get('likes', agent[10]),
                    overview=data.get('overview', agent[11]),
                    key_features=key_features_array,
                    use_cases=use_cases_array,
                    created_by=data.get('created_by', agent[14]),
                    access=data.get('access', agent[15]),
                    tags=tags_array,
                    preview_image=data.get('preview_image', agent[17]),
                    logo=data.get('logo', agent[18]),
                    demo_video=data.get('demo_video', agent[19]),
                    is_approved=agent[21]  # Keep the existing approval status
                )

                return JsonResponse({'message': 'Agent updated successfully'})

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        else:
            return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

