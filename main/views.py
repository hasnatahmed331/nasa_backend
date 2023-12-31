from django.http import JsonResponse

from firebase_admin import auth
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from django.db.models import Count
from embeddings import create , emb_search
import concurrent
from django.shortcuts import get_object_or_404
from django.conf import settings
from qdrant_client import models

from datetime import date

from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import CustomUser, CommunicationAccess



@csrf_exempt
@api_view(['POST'])
def authenticate_firebase_token(request):
    # Get the Firebase ID token from the frontend request
    firebase_id_token = request.data.get('idToken')
    # print(firebase_id_token)

    try:
        # Verify the Firebase ID token using Firebase Admin SDK
        decoded_token = auth.verify_id_token(firebase_id_token)
        
        # print(decoded_token) : email name uid 
                
        # Get the UID (User ID) from the decoded token
        uid = decoded_token['uid']

        # Perform actions based on the UID (e.g., authenticate, authorize, fetch user data)
        user, created = CustomUser.objects.get_or_create(uuid=uid)
        
        if created:
            user.name = decoded_token['name']
            user.email = decoded_token['email']
            user.save()
        
        
        return Response({
            'uid': uid, 
            'message': 'Firebase token authenticated successfully', 
            'created': created,
             'name' : user.name,
             'id' : user.id,
            })
    
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
    user_list_data = []
    
    for user in users:
        users_tags = UsersTag.objects.filter(user=user)
        tag_list = [{'id': user_tag.tag.id, 'name': user_tag.tag.name} 
                    for user_tag in users_tags]
        
        user_data = {
            'id': user.id,
            'username': user.name,
            'tags': tag_list,
        }
        
        user_list_data.append(user_data)
    
    return JsonResponse({'users': user_list_data})


@api_view(['GET'])
def project_list(request):
    projects = Project.objects.all()
    project_list_data = []

    for project in projects:
        project_tags = ProjectsTag.objects.filter(project=project)
        tag_list = [{'id': project_tag.tag.id, 'name': project_tag.tag.name} 
                    for project_tag in project_tags]
        
        project_data = {
            'id': project.id,
            'title': project.title,
            'tags': tag_list,
        }
        
        project_list_data.append(project_data)

    return JsonResponse({'projects': project_list_data})


@api_view(['GET'])
def tag_list(request):
    tags = Tag.objects.all()
    tag_list_data = [{'id': tag.id, 'name': tag.name} for tag in tags]
    return JsonResponse({'tags': tag_list_data})


@api_view(['GET'])
def user_detail(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        
        user_tags = UsersTag.objects.filter(user=user)
        tag_list = [{'id': user_tag.tag.id, 'name': user_tag.tag.name} 
                    for user_tag in user_tags]
        
        user_projects = Project.objects.filter(created_by=user)
        project_list = [{'id': project.id, 'title': project.title}
                        for project in user_projects]
              
        user_data = {
            'id': user.id,
            'uuid' : user.uuid,
            'username': user.name,
            'bio': user.bio,
            'tags': tag_list,
            'projects': project_list,
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
            'created_by_id': project.created_by.id,
            'start_date': project.start_date,
            'title': project.title,
            'description': project.description,
            'tags': tag_list,
        }
        return JsonResponse(project_data)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)


@api_view(['POST'])
def projects_by_tags(request):  
    if request.method == 'POST':
                    
        tag_ids = request.data.get('tag_ids') 
        
        project_list_data = []
        #length of tags list call project list function
            
        project_tags_count = ProjectsTag.objects.filter(tag_id__in=tag_ids).values('project_id').annotate(tag_count=Count('project_id'))

        matching_projects = [project_count['project_id'] for project_count in project_tags_count if project_count['tag_count'] == len(tag_ids)]

        projects = Project.objects.filter(id__in=matching_projects)
               
        for project in projects:
                project_tags = ProjectsTag.objects.filter(project=project)
                tag_list = [{'id': project_tag.tag.id, 'name': project_tag.tag.name} 
                            for project_tag in project_tags]
                
                project_data = {
                    'id': project.id,
                    'title': project.title,
                    'tags': tag_list,
                }
                
                project_list_data.append(project_data)

        
        return JsonResponse({'projects': project_list_data})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@api_view(['POST'])
def users_by_tags(request):
    if request.method == 'POST':
             
        tag_ids = request.data.get('tag_ids') 
        
        user_list_data = []
        
        # Count the number of occurrences of each tag for each user
        user_tags_count = UsersTag.objects.filter(tag_id__in=tag_ids).values('user_id').annotate(tag_count=Count('user_id'))

        # Filter users where the tag count matches the number of specified tags
        matching_users = [user_count['user_id'] for user_count in user_tags_count if user_count['tag_count'] == len(tag_ids)]

        # Query the User model to find users who have both specified tags
        users = CustomUser.objects.filter(id__in=matching_users)
        
        # Create a list of user data
        for user in users:
            users_tags = UsersTag.objects.filter(user=user)
            tag_list = [{'id': user_tag.tag.id, 'name': user_tag.tag.name} 
                        for user_tag in users_tags]
            
            user_data = {
                'id': user.id,
                'username': user.name,
                'tags': tag_list,
            }
            
            user_list_data.append(user_data)

        return JsonResponse({'users': user_list_data})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

@api_view(['POST'])
def bio(request):
    if request.method == 'POST':
            user_id = request.data.get('user_id')
            bio = request.data.get('bio')
            tags = request.data.get('tags')
            
            print(user_id , bio , tags)
            
            already = False
            try:
                user = get_object_or_404(CustomUser, id=user_id)
                user.bio = bio
                user.save()

                # Replace existing tags with the new tags for the user
                existang_tags = UsersTag.objects.filter(user=user)  # Delete existing tags
                if existang_tags.exists():
                    already = True
                    existang_tags.delete()
                for tag_id in tags:
                    tag = get_object_or_404(Tag, name=tag_id)
                    UsersTag.objects.create(user=user, tag=tag)  # Create new UsersTag objects for the user and tags

                context = {'name' : 'user' , 'bio' : bio , 'id' : user_id , 'already' : already}
                executor = concurrent.futures.ThreadPoolExecutor()  
                future =  executor.submit(create , context)
                future.add_done_callback(lambda f: executor.shutdown(wait=False))
               
            
                return JsonResponse({'message': 'Bio updated successfully'})
            except Exception as e:
                return Response({"error" : e.args[0]})
    else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    


@api_view(['POST'])
def project(request):
    if request.method == 'POST':
        
            user_id = request.data.get('user_id')
            title = request.data.get('title')
            description = request.data.get('description')
            tags = request.data.get('tags')
            id = request.data.get('id' , None)
            
            if id is None:
                try:
                    user = get_object_or_404(CustomUser, id=user_id)
                    today = date.today()
                    project = Project.objects.create(
                        created_by=user, title=title, description=description , start_date=today, )
                    id = project.id
                    for tag_id in tags:
                        tag = get_object_or_404(Tag, name=tag_id)
                        ProjectsTag.objects.create(project=project, tag=tag)
                    
                    context = {'name' : 'project' , 'id' : id , 'des' : description  , 'already' : False}
                    executor = concurrent.futures.ThreadPoolExecutor()  
                    future =  executor.submit(create , context)
                    future.add_done_callback(lambda f: executor.shutdown(wait=False))
            
                    
                    return JsonResponse({'message': 'Project created successfully'})
                except Exception as e:
                    return Response({"error" : e.args[0]})
            else:
                print("else")
                try:
                    project = get_object_or_404(Project, id=id)
                    project.title = title
                    project.description = description
                 
                    project.save()

                    # Replace existing tags with the new tags for the project
                    ProjectsTag.objects.filter(project=project).delete()  # Delete existing tags
                    for tag_id in tags:
                        tag = get_object_or_404(Tag, name=tag_id)
                        ProjectsTag.objects.create(project=project, tag=tag)  # Create new ProjectsTag objects for the project and tags
                    
                    context = {'name' : 'project' , 'id' : id , 'des' : description , 'already' : True}
                    executor = concurrent.futures.ThreadPoolExecutor()  
                    future =  executor.submit(create , context)
                    future.add_done_callback(lambda f: executor.shutdown(wait=False))
               
                    
                    return JsonResponse({'message': 'Project updated successfully'})
                except Exception as e:
                    return Response({"error" : e.args[0]})
    else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@api_view(['GET'])
def check(request):
    users = CustomUser.objects.all()

    # Format users in the desired format
    formatted_users = {user.id: user.bio for user in users}
    x =settings.QDRANT_CLIENT.retrieve(collection_name = 'user' , ids = [1,2,3,4])
    print(x)
    return JsonResponse({'users': 'x'})
    
    


@api_view(['POST'])
def semantic_search(request):
    try:
        query =request.data.get('query')
        search   = request.data.get('search') 
        ids = emb_search(search , query)
        
        
        if search == "user":
            users = CustomUser.objects.filter(id__in=ids)
            id_to_order = {id: order for order, id in enumerate(ids)}
            users = sorted(users, key=lambda user: id_to_order[user.id])
            user_list_data = []

            for user in users:
                users_tags = UsersTag.objects.filter(user=user)
                tag_list = [{'id': user_tag.tag.id, 'name': user_tag.tag.name}
                            for user_tag in users_tags]

                user_data = {
                    'id': user.id,
                    'username': user.name,
                    'tags': tag_list,
                }

                user_list_data.append(user_data)

            return JsonResponse({'ids': user_list_data})
        
        elif search == "project":
            projects = Project.objects.filter(id__in=ids)
            
            id_to_order = {id: order for order, id in enumerate(ids)}
            projects = sorted(projects, key=lambda project: id_to_order[project.id])

    
            project_list_data = []

            for project in projects:
                print(project.id)
                project_tags = ProjectsTag.objects.filter(project=project)
                tag_list = [{'id': project_tag.tag.id, 'name': project_tag.tag.name} 
                            for project_tag in project_tags]
                
                project_data = {
                    'id': project.id,
                    'title': project.title,
                    'tags': tag_list,
                }
        
                project_list_data.append(project_data)

            return JsonResponse({'ids': project_list_data}) 
             
        
        return Response({'ids' : ids})
    except Exception as e:
        return Response({'error' : e.args[0]})


@api_view(['POST'])
def send_access_request(request):
    if request.method == 'POST':
        try:
            has_access_to_id = request.data.get('has_access_to_id')
            to_this_person_id = request.data.get('to_this_person_id')
            request_status = request.data.get('request_status')
            message = request.data.get('message', '')

            has_access_to = CustomUser.objects.get(id=has_access_to_id)
            to_this_person = CustomUser.objects.get(id=to_this_person_id)

            # Check if a similar request already exists, and update it if necessary
            existing_request = CommunicationAccess.objects.filter(
                has_access_to=has_access_to,
                to_this_person=to_this_person,
            ).first()

            if existing_request:
                existing_request.status = request_status
                existing_request.message = message
                existing_request.save()
                return JsonResponse({'message': 'Already Request Sent'})
            else:
                new_request = CommunicationAccess(
                    has_access_to=has_access_to,
                    to_this_person=to_this_person,
                    status=request_status,
                    message=message,
                )
                new_request.save()

            return JsonResponse({'message': 'Access request sent successfully'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)


from django.http import JsonResponse
from .models import CustomUser, CommunicationAccess

@api_view(['GET'])
def get_access_for_person(request, person_id):
    try:
        person = CustomUser.objects.get(id=person_id)
        access_list = CommunicationAccess.objects.filter(has_access_to=person)
        access_data = []

        for access in access_list:
            id = access.id
            to_this_person = access.to_this_person
            access_status = access.status
            message = access.message if access.message else "N/A"
            email = to_this_person.email if to_this_person.email else "N/A"

            if access_status == 'requested':
                email = "null"
            
            access_info = {
                "id" : id,
                'to_this_person': to_this_person.name,
                'request_status': access_status,
                'email': email,
                'message':message
            }

            access_data.append(access_info)

        return JsonResponse({'access_list': access_data})
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
   
@api_view(['GET'])
def accept_access_request(request, request_id):
    try:

        access_request = CommunicationAccess.objects.get(id=request_id)
        
        if access_request.status == 'requested':
            access_request.status = 'approved'
            access_request.save()
            
            return JsonResponse({'message': 'Access request accepted'})
        else:
            return JsonResponse({'error': 'Access request is not in a pending state'}, status=400)
    except CommunicationAccess.DoesNotExist:
        return JsonResponse({'error': 'Access request not found'}, status=404) 

@api_view(['GET'])
def get_to_this_person_access(request, person_id):
    try:
        person = CustomUser.objects.get(id=person_id)
        access_list = CommunicationAccess.objects.filter(to_this_person=person)
        access_data = []

        for access in access_list:
            id = access.id
            has_access_to = access.has_access_to
            access_status = access.status
            message = access.message if access.message else "N/A"

            access_info = {
                'has_access_to': has_access_to.name,
                'request_status': access_status,
                'message':message,
                "id":id
            }

            access_data.append(access_info)

        return JsonResponse({'access_list': access_data})
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)



