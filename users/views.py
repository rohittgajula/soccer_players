from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework import status, viewsets

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

import hashlib
from django.core.cache import cache

from players.models import Player
from players.serializers import PlayersSerializer
from .permissions import UserPermissions

from django.contrib.auth.hashers import make_password

import logging

logger = logging.getLogger(__name__)




@permission_classes([UserPermissions])
@api_view(['GET', 'PATCH', 'DELETE'])
def user_details(request):
  pk = request.query_params.get('pk')

  cache_key = hashlib.md5(f"{pk}".encode()).hexdigest() if pk else 'user_list_cache_key'
  logger.info(f"Cache key used: {cache_key}")

  cache_data = cache.get(cache_key)

  if cache_data:
    return Response({
      'cache user data':cache_data
    }, status.HTTP_200_OK)

  if pk is None:
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    cache.set(cache_key, serializer.data, timeout=60*5)
    return Response({
      'users':serializer.data
    }, status.HTTP_200_OK)
  
  try:
    user = User.objects.get(pk=pk)
  except User.DoesNotExist:
    return Response({
      'error':'User not found.'
    }, status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'GET':
    serializer = UserSerializer(user)
    cache.set(cache_key, serializer.data, timeout=60*5)
    return Response({
      'user':serializer.data
    }, status.HTTP_200_OK)
  
  if request.method == 'PATCH':
    serializer = UserSerializer(user, data=request.data, partial=True)
    cache.set(cache_key, serializer.data, timeout=60*5)
    if serializer.is_valid():
      serializer.save()
      return Response({
        'details':serializer.data
      }, status.HTTP_200_OK)
    return Response({
      'error':serializer.errors
    }, status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'DLEETE':
    user.delete()
    cache.delete(cache_key)
    return Response({
      'details':'User deleted sucessfully.'
    }, status.HTTP_204_NO_CONTENT)
  


  

@api_view(['POST'])
def register_user(request):
  data = request.data
  if 'password' in data:
    data['password'] = make_password(data['password'])
  serializer = RegisterSerializer(data=data)
  if serializer.is_valid():
    serializer.save()

    cache.delete('user_list_cache_key')   # invalidate cache after new user is created
    logger.info(f"Cache invalidated for key: user_list_cache_key")

    return Response({
      'details':'User registered sucessfully.',
      'user':serializer.data
    }, status.HTTP_201_CREATED)
  return Response({
    'error':serializer.errors
  }, status.HTTP_400_BAD_REQUEST)
  




@permission_classes([UserPermissions])
@api_view(['POST'])
def toggle_favorite(request, public_id):
  player_id = request.data.get('player_id')

  user = get_object_or_404(User, public_id=public_id)

  if player_id:
    try:
      player = Player.objects.get(id=player_id)
    except Player.DoesNotExist:
      return Response({
        'error':'Player does not exists.'
      }, status.HTTP_404_NOT_FOUND)
    
    if user.favourate_players.filter(id=player_id).exists():
      user.favourate_players.remove(player)
      user.save()
      
      player_data = PlayersSerializer(player)
      return Response({
        'message':'Removed from favorites.',
        'player_data':player_data.data
      }, status.HTTP_200_OK)
    else:
      user.favourate_players.add(player)
      user.save()

      player_data = PlayersSerializer(player)
      return Response({
        'message':'Added to favorites.',
        'player_data':player_data.data
      }, status.HTTP_200_OK)
  else:
    return Response({
      'error':'Please provide a valid player ID.'
    }, status.HTTP_400_BAD_REQUEST)
  




@api_view(['GET'])
def list_favorite(request, public_id):

  cache_key = hashlib.md5(f"{public_id}".encode()).hexdigest()
  cache_data = cache.get(cache_key)

  if cache_data:
    return Response({
      'cache favorites':cache_data
    }, status.HTTP_200_OK)

  user = get_object_or_404(User, public_id=public_id)
  favorites = user.favourate_players.all()

  serializer = PlayersSerializer(favorites, many=True)
  cache.set(cache_key, serializer.data, timeout=60*5)
  return Response({
    'favorites':serializer.data
  }, status.HTTP_200_OK)





class ProtectedView(APIView):

  permission_classes = [IsAuthenticated]
  def  get(self, request):
    return Response({
      'message':'This is a private view.'
    }, status.HTTP_200_OK)
  




class PublicView(APIView):

  def get(self, request):
    return Response({
      'message':'This is a public view'
    }, status.HTTP_200_OK)
  



  
class LoginView(viewsets.ViewSet):
  serializer_class = LoginSerializer
  http_method_names = ['post']
  
  def create(self, request, *args, **kwargs):
    serializer = self.serializer_class(data = request.data)
    
    try:
        serializer.is_valid(raise_exception=True)
    except TokenError as e:
        raise InvalidToken(e)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)

