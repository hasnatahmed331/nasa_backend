from django.http import JsonResponse
import firebase_admin
from firebase_admin import auth
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response



@csrf_exempt
@api_view(['POST'])
def authenticate_firebase_token(request):
    # Get the Firebase ID token from the frontend request
    firebase_id_token = request.POST.get('idToken')
    print(firebase_id_token)

    try:
        # Verify the Firebase ID token using Firebase Admin SDK
        decoded_token = auth.verify_id_token(firebase_id_token)
        
        # Get the UID (User ID) from the decoded token
        uid = decoded_token['uid']

        # Perform actions based on the UID (e.g., authenticate, authorize, fetch user data)
        # ...

        return Response({'uid': uid, 'message': 'Firebase token authenticated successfully'})
    
    except Exception as e:
        # Handle authentication error
        return Response({'error': e.args[0]}, status=401)
