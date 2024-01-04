from rest_framework.response import Response
from .models import Note
from .serializers import LoginSerializer, RegisterSerializer, NoteSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        # If serializer is not valid.
        if not serializer.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])

        # If user is not found.
        if not user:
            return Response({
                'status' : False,
                'message' : 'Invalid credentials',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate token for the user.
        token, _ = Token.objects.get_or_create(user=user)

        # Returning the token.
        return Response({
            'status' : True,
            'message' : 'User logged in successfully',
            'token' : str(token)
        },
        status=status.HTTP_200_OK)


class RegisterAPI(APIView):
    # POST Method
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        # If serializer is not valid.
        if not serializer.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        # Returning the message.
        return Response({
            'status' : True,
            'message' : 'User created successfully'
        },
        status=status.HTTP_201_CREATED)


class SignOutAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def post(self, request):
        logout(request)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)


class NotesAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # throttle_scope = "low"

    # View Notes
    def get(self, request):
        try:
            print(request.user)
            notes = Note.objects.filter(owner=request.user)
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Create Notes
    def post(self, request):
        data = request.data
        data['owner'] = request.user.id  # Assign the authenticated user as the owner
        serializer = NoteSerializer(data=data)

        # Serializer check
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class NoteDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # throttle_scope = "high"

    # View Note
    def get(self, request, id):
        try:
            note = Note.objects.get(id=id, owner=request.user)
            serializer = NoteSerializer(note)
            return Response(serializer.data)
        
        # If note is not found.
        except Note.DoesNotExist:
            return Response({"detail": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # If any other exception occurs.
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Update Note
    def put(self, request, id):
        try:
            note = Note.objects.get(id=id, owner=request.user)
            serializer = NoteSerializer(note, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # If note is not found.
        except Note.DoesNotExist:
            return Response({"detail": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # If any other exception occurs.
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Delete Note
    def delete(self, request, id):
        try:
            note = Note.objects.get(id=id, owner=request.user)
            note.delete()
            return Response({"detail": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        
        # If note is not found.
        except Note.DoesNotExist:
            return Response({"detail": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # If any other exception occurs.
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class NoteShareAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # throttle_scope = "low"

    # Share Note
    def post(self, request, id):
        
        try:
            note = Note.objects.get(id=id, owner=request.user)
            user_to_share_with_id = request.data.get('user_to_share_with')

            if user_to_share_with_id is not None:
                user_to_share_with = User.objects.get(id=user_to_share_with_id)
                note.shared_with.add(user_to_share_with)
                note.save()

                return Response({"detail": "Note shared successfully"}, status=status.HTTP_200_OK)
            # If user_to_share_with is not provided.
            else:
                return Response({"detail": "user_to_share_with parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        # If note is not found.
        except Note.DoesNotExist:
            return Response({"detail": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # If user to share with is not found.
        except User.DoesNotExist:
            return Response({"detail": "User to share with not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # If any other exception occurs.
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NoteSearchAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        query = request.query_params.get('q', '')

        if query:
            # Use PostgreSQL Full Text Search for efficient searching
            vector = SearchVector("title", "content")
            query = SearchQuery(query)
            notes = Note.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')
            # notes = Note.objects.annotate(rank=SearchRank(F('search_vector'), SearchQuery(query))).filter(
            #     rank__gte=0.3
            # ).order_by('-rank')
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "Please provide a search query"}, status=status.HTTP_400_BAD_REQUEST)
