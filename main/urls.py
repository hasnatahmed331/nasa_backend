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
    path('semanticsearch/' , views.semantic_search , name="search")
]