from django.contrib import admin
from .models import *

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio' , 'name' , 'uuid' , 'id') 
    
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'start_date', 'title', 'description')
    
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    
class UsersTagAdmin(admin.ModelAdmin):
    list_display = ('id','user','tag')

class ProjectsTagAdmin(admin.ModelAdmin):
    list_display = ('id','project','tag')
    
admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(UsersTag)
admin.site.register(ProjectsTag)

