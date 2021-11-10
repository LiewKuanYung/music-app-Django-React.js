from django.shortcuts import render
from rest_framework import generics
from .serializers import RoomSerializer
from .models import Room

class RoomView(generics.ListCreateAPIView): # checkout concrete view classes
    # queryset = what to return
    queryset = Room.objects.all()
    # serializer = how to return
    serializer_class = RoomSerializer


