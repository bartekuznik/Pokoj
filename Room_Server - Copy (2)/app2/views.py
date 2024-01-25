from django.shortcuts import render
from .serializers import RoomSerializer, PlayerGameSerializer
from rest_framework import generics
from .models import Room, PlayerInGame
# Create your views here.

class RoomList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class PlayerList(generics.ListAPIView):
    queryset = PlayerInGame.objects.all()
    serializer_class = PlayerGameSerializer
    
class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerInGame.objects.all()
    serializer_class = PlayerGameSerializer