from . import views
from django.urls import path

urlpatterns = [
    path('login/' , views.authenticate_firebase_token, name='authenticate_firebase_token'),
    path('hey/', views.hello, name='hey'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('allusers/', views.user_list, name='user_list'),
    path('allprojects/', views.project_list, name='project_list'),
    path('alltags/', views.tag_list, name='tag_list'),
    path('projectsbytag/', views.projects_by_tags, name='projects_by_tag'),
    path('usersbytag/', views.users_by_tags, name='users_by_tag'),
    
    path('updateproject/' , views.project, name='project'),
    path('updatebio/' , views.bio, name='bio'),
    path('check/' , views.check, name='check'),
    path('semanticsearch/' , views.semantic_search , name="search"),
    
    path('requestaccept/<int:request_id>/' , views.accept_access_request , name='accept_request'),
    path('requestcommunication/' , views.send_access_request , name='request_communication'),
    path('ihavesent/<int:person_id>/' , views.get_access_for_person , name='get_access_for_person'),
    path('ihaverecieved/<int:person_id>/' , views.get_to_this_person_access , name='get_access_from_person'),
]