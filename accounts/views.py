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


@api_view(['POST'])
def login_api(request):
    try:
        data= request.data
        email=data.get('email')
        password=data.get('password')
        user = authenticate(email=email,password=password)
        if user:
            token = Token.objects.get_or_create(user=user)
            return Response({
                'status': 200,
                'token':str(Token)
            })
        return Response({
            'status':300,
            'message':'invaild credentials',
        })
    except Exception as e:
            print(e)
    return Response({
            'status':400,
            'message':'went wrong',
        })

class Login(APIView):
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
    # def post(self, request):
    #     try:
    #         data=request.data
    #         serializer = LoginSerializer(data=data)
    #         email=data.get('email')
    #         password=data.get('password')
    #         user = authenticate(email=email,password=password)
            
    #         if serializer.is_valid():
    #                     token = Token.objects.get_or_create(user=user)
    #                     email=serializer.data['email']
    #                     password=serializer.data['password']

    #                     user= User.objects.filter(email=email)
    #                     if not user.exists():
    #                         return Response({
    #                         'status':400,
    #                         'message' :'something went wrong',
    #                         'data':'invaild email'
    #                     })

    #                     if user[0].password!=password:
    #                         return Response({
    #                             'status':400,
    #                             'message':'something went wrong',
    #                             'data':'wrong otp'
    #                         })
                        
                         
    #                     return Response({
    #                         'status': 200,
    #                         'token':str(Token)
    #                     })



                        
                        

                    
    #         return Response({
    #                         'status':400,
    #                         'message' :'something went wrong',
    #                         'data':serializer.errors
    #                     })


    #     except Exception as e:
    #         print(e)


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
        