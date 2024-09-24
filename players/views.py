from rest_framework.decorators import api_view
from rest_framework import status
from .models import Player
from .serializers import PlayersSerializer
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination

from django.db.models import Q

from django.core.cache import cache

import hashlib

from django.http import JsonResponse

def player_ids(request):
    player_ids = Player.objects.values_list('id', flat=True)
    return JsonResponse(list(player_ids), safe=False)


@api_view(['GET'])
def player_list(request):
    player_id = request.query_params.get('player_id', None)
    name = request.query_params.get('name', None)
    club = request.query_params.get('club', None)
    min_age = request.query_params.get('min_age', None)
    max_age = request.query_params.get('max_age', None)
    page = request.query_params.get('page', 1)

    cache_key = hashlib.md5(f"{player_id}_{name}_{club}_{min_age}_{max_age}_{page}".encode()).hexdigest()

    cached_data = cache.get(cache_key)
    if cached_data:
        return Response({
            'redis cached data':cached_data
        }, status.HTTP_200_OK)

    # Uses a Q object to allow combining multiple query parameters.
    query = Q()
    if player_id:
        query &= Q(id=player_id)
    if name:
        query &= Q(name__icontains=name)
    if club:
        query &= Q(club__icontains=club)
    if min_age is not None and max_age is not None:
        try:
            min_age = int(min_age)
            max_age = int(max_age)
            if min_age <= max_age:
                query &= Q(age__range=(min_age, max_age))
            else:
                return Response({'error': 'min_age cannot be greater than max_age.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid age range provided.'}, status=status.HTTP_400_BAD_REQUEST)

    players = Player.objects.filter(query)

    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_players = paginator.paginate_queryset(players, request)

    serializer = PlayersSerializer(paginated_players, many=True)

    # Return response with dynamic page size
    response_data = paginator.get_paginated_response({
        'page_size': paginator.page_size,
        'players_details': serializer.data
    }).data

    cache.set(cache_key, response_data, timeout=60*5)
    return Response(response_data, status.HTTP_200_OK)
