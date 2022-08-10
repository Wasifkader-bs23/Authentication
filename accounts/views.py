from django.shortcuts import render
from accounts.emails import send_otp_via_email
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from .emails import *
# Create your views here.
class RegisterAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                return Response ({
                    'status': 200,
                    'message' :'registration successful check email',
                    'data': serializer.data,
                })

            
            return Response({
                'status':400,
                'message' :'something went wrong',
                'data':serializer.errors
            })
        
        except Exception as e:
            print(e)
        