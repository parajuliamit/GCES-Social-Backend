from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from django.contrib.auth.models import User
from base.models import Batch, VerifyPin

from base.serializers import UserSerializer, UserSerializerWithToken, RegisterUserSerializer, BatchSerializer, VerifyUserSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail

from django.contrib.auth.hashers import make_password
from rest_framework import status

import random

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

@api_view(['POST'])
def registerUser(request):
    data = request.data
    resgister_serializer=RegisterUserSerializer(data=data)
    if resgister_serializer.is_valid():
        try:
            user = User.objects.create(
                first_name = data['name'],
                username = data ['email'],
                email = data ['email'],
                password=make_password(data['password'])
            )
            user.is_active = False
            user.save()

            otp = str(random.randint(100000,999999))
            VerifyPin.objects.create(user = user, otp=otp)
            
            send_mail(
                'Verify your GCES Social Account',
                'Your OTP for GCES Social account is: '+otp,
                'gcessocial@gmail.com',
                [data['email']],
                fail_silently=False,
            )
            serializer = UserSerializerWithToken(user,many = False)
            return Response(serializer.data)
        except Exception as e:
            print (e)
            message = {'detail':'User with this email already exists.'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(resgister_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verifyUser(request):
    data = request.data
    serializer=VerifyUserSerializer(data = data)
    if serializer.is_valid():
        code = serializer.validated_data['otp']
        user = serializer.validated_data['user']
        
        user_pin = VerifyPin.objects.filter(user = user).get(user=user)
        pin = user_pin.otp

        if code == pin:
            user_ = User.objects.get(username=user)
            user_.is_active = True
            user_.save()
            user_pin.delete()
            return Response({"message":"success"},status=status.HTTP_200_OK)
        else:
            return Response({"error":"OTP didn't match."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def resendPin(request,pk):
    try:
        otp = str(random.randint(100000,999999))
        pin = VerifyPin.objects.get(user = pk)
        pin.otp = otp
        pin.save()  
        send_mail(
            'Verify your GCES Social Account',
            'Your OTP for GCES Social account is: '+otp,
                    'gcessocial@gmail.com',
                    [pin.user],
                    fail_silently=False,
                )
        return Response({"message":"success"},status=status.HTTP_200_OK)
    except:
        return Response({"error":"unable to send otp"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user,many = False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editName(request):
    user = request.user
    serializer = UserSerializerWithToken(user,many = False)

    data = request.data

    user.first_name = data['name']

    user.save()
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def changePassword(request):
    user = request.user
    serializer = UserSerializerWithToken(user,many = False)

    data = request.data
    
    user.password=make_password(data['password'])
    
    user.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many = True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBatch(request):
    serializer = BatchSerializer(Batch.objects.all(),many = True)
    return Response(serializer.data)