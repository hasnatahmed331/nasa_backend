from django.http import JsonResponse
import firebase_admin
from firebase_admin import auth
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from django.db.models import Count



@csrf_exempt
@api_view(['POST'])
def authenticate_firebase_token(request):
    # Get the Firebase ID token from the frontend request
    firebase_id_token = request.POST.get('idToken')
    # print(firebase_id_token)

    try:
        # Verify the Firebase ID token using Firebase Admin SDK
        decoded_token = auth.verify_id_token(firebase_id_token)
                
        # Get the UID (User ID) from the decoded token
        uid = decoded_token['uid']

        # Perform actions based on the UID (e.g., authenticate, authorize, fetch user data)
        user, created = CustomUser.objects.get_or_create(uuid=uid)
        
        if created:
            user.name = decoded_token['name']
            user.save()
        
        user.save()
        
        return Response({'uid': uid, 'message': 'Firebase token authenticated successfully' , 'created': created})
    
    except Exception as e:
        # Handle authentication error
        print(e)
        return Response({'error': e.args[0]}, status=401)

@api_view(['GET'])
def hello(request):
    return HttpResponse("Hello world!")


@api_view(['GET'])
def user_list(request):
    users = CustomUser.objects.all()
    user_list_data = [{'id': user.id, "uuid" : user.uuid ,  'username': user.name} for user in users]
    return JsonResponse({'users': user_list_data})


@api_view(['GET'])
def project_list(request):
    projects = Project.objects.all()
    project_list_data = [{'id': project.id, 'title': project.title} for project in projects]
    return JsonResponse({'projects': project_list_data})


@api_view(['GET'])
def tag_list(request):
    tags = Tag.objects.all()
    tag_list_data = [{'id': tag.id, 'name': tag.name, 'type': tag.type, 'level': tag.level} for tag in tags]
    return JsonResponse({'tags': tag_list_data})


@api_view(['GET'])
def user_detail(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        
        user_tags = UsersTag.objects.filter(user=user)
        tag_list = [{'id': user_tag.tag.id, 'name': user_tag.tag.name,'level': user_tag.tag.level} 
                    for user_tag in user_tags]
              
        user_data = {
            'id': user.id,
            'uuid' : user.uuid,
            'username': user.name,
            'bio': user.bio,
            'tags': tag_list,
        }
        return JsonResponse(user_data)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


@api_view(['GET'])
def project_detail(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        
        project_tags = ProjectsTag.objects.filter(project=project)
        tag_list = [{'id': project_tag.tag.id, 'name': project_tag.tag.name} 
                    for project_tag in project_tags]
        
        project_data = {
            'id': project.id,
            'created_by': project.created_by.name,
            'created_by_id': project.created_by.uuid,
            'start_date': project.start_date,
            'title': project.title,
            'description': project.description,
            'tags': tag_list,
        }
        return JsonResponse(project_data)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)


@api_view(['GET'])
def projects_by_tags(request):
    if request.method == 'GET':
        
        tag_ids = [3,4]  # Replace with the tag IDs you want to test
        
        project_tags_count = ProjectsTag.objects.filter(tag_id__in=tag_ids).values('project_id').annotate(tag_count=Count('project_id'))

        matching_projects = [project_count['project_id'] for project_count in project_tags_count if project_count['tag_count'] == len(tag_ids)]


         # Query the User model to find users who have both specified tags
        projects = Project.objects.filter(id__in=matching_projects)
        
        # Create a list of user data
        project_list = [{'id': project.id, 'title': project.title} for project in projects]

        return JsonResponse({'projects': project_list})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



@api_view(['POST'])
def users_by_tags(request):
    if request.method == 'POST':
        # Hardcode some tag IDs for testing
        tag_ids = [2]  # Replace with the tag IDs you want to test

        # Count the number of occurrences of each tag for each user
        user_tags_count = UsersTag.objects.filter(tag_id__in=tag_ids).values('user_id').annotate(tag_count=Count('user_id'))

        # Filter users where the tag count matches the number of specified tags
        matching_users = [user_count['user_id'] for user_count in user_tags_count if user_count['tag_count'] == len(tag_ids)]

        # Query the User model to find users who have both specified tags
        users = CustomUser.objects.filter(id__in=matching_users)
        
        # Create a list of user data
        user_list = [{'id': user.id, 'username': user.name} for user in users]

        return JsonResponse({'users': user_list})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

