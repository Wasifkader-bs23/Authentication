from django.shortcuts import render
from accounts.emails import send_otp_via_email
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from .emails import *
from rest_framework.decorators import api_view
# Create your views here.
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime


class Login(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
  


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

class VerifyOTP(APIView):
    def post(self, request):
        try:
            data=request.data
            serializer = VerifyAccountSerializer(data=data)

            if serializer.is_valid():
                        email=serializer.data['email']
                        otp=serializer.data['otp']

                        user= User.objects.filter(email=email)
                        if not user.exists():
                            return Response({
                            'status':400,
                            'message' :'something went wrong',
                            'data':'invaild email'
                        })

                        if user[0].otp!=otp:
                            return Response({
                                'status':400,
                                'message':'something went wrong',
                                'data':'wrong otp'
                            })
                        
                        user[0].is_verified=True
                        user[0].save()



                        
                        return Response ({
                            'status': 200,
                            'message' :'account verified',
                            'data': {},
                        })

                    
            return Response({
                            'status':400,
                            'message' :'something went wrong',
                            'data':serializer.errors
                        })


        except Exception as e:
            print(e)

class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserViewSerializer(user)
        return Response(serializer.data)

    def patch(self, request,*args,**kwargs):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        

        user = User.objects.filter(id=payload['id']).first()
        data = request.data
        serializer = UserViewSerializer(user,data=request.data, partial=True)
        if serializer.is_valid():
                serializer.save()

        


        return Response(serializer.data)
    
    
        