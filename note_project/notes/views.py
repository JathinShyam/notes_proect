from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import Note
from .serializers import LoginSerializer, RegisterSerializer, NoteSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.contrib.auth import authenticate, login, logout


class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])

        if not user:
            return Response({
                'status' : False,
                'message' : 'Invalid credentials',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        token, _ = Token.objects.get_or_create(user=user)
        print(token)
        return Response({
            'status' : True,
            'message' : 'User logged in successfully',
            'token' : str(token)
        },
        status=status.HTTP_200_OK)


class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response({
            'status' : True,
            'message' : 'User created successfully'
        },
        status=status.HTTP_201_CREATED)


class SignOutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def note(request):
    if request.method == 'GET':
        try:
            notes = Note.objects.filter(owner=request.user)
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        data = request.data
        data['owner'] = request.user.id  # Assign the authenticated user as the owner
        serializer = NoteSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class NotesAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            print(request.user)
            notes = Note.objects.filter(owner=request.user)
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        data = request.data
        data['owner'] = request.user.id  # Assign the authenticated user as the owner
        serializer = NoteSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)