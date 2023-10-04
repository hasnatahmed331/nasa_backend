from . import views
from django.urls import path

urlpatterns = [
    path('' , views.authenticate_firebase_token, name='authenticate_firebase_token')
]