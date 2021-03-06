from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room

class RoomView(generics.ListCreateAPIView): # checkout concrete view classes
    # queryset = what to return
    queryset = Room.objects.all()
    # serializer = how to return
    serializer_class = RoomSerializer

class GetRoom(APIView):
    # define serializer just like CreateRoomView
    serializer_class = RoomSerializer
    # keyword argument, will be used to indicate code need to be an keyword arugment.
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        # request.GET gives you the information from url
        # request.GET.get() is looking for parameters inside this get
        code = request.GET.get(self.lookup_url_kwarg) # looking for this lookup_url_kwarg, which is 'code'
        if code != None:
            # find which room has this code
            room = Room.objects.filter(code=code)
            # if there's this room
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                # check if user is the host
                data['is_host'] = (self.request.session.session_key == room[0].host)
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Room Not Found': 'Invalid Room Code'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)

class JoinRoom(APIView):
    lookup_url_kwarg = 'code'

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session['room_code'] = code
                return Response({'message': 'Room Joined!'}, status=status.HTTP_200_OK)

            return Response({'Bad Request': 'Invalid Room Code'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'Bad Request': 'Invalid post data, did not find a code key'}, status=status.HTTP_400_BAD_REQUEST)


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer
    # Take note that this CreateRoomSerializer doesn't have the 'host' field
    # We know that 'id', 'code', 'created_at' are generated at model, but what about 'host'?
    # 'host' will be validated through session. Basically, session is a temp connection between 
    # your browser and server. What we need to do is to check whether the browser currently has 
    # an active session with the server.

    def post(self, request, format=None):
        # get access to the session id

        # check if current request has an active access with browser
        if not self.request.session.exists(self.request.session.session_key):
            # if no, create a session
            self.request.session.create()

        # serialize request.data and put it into python serializer variable
        serializer = self.serializer_class(data=request.data)

        # if data 'guest_can_pause' & 'votes_to_skip' are valid
        if serializer.is_valid():
            # create a room
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key

            # Check if there's any room in our database that has host == this POST request's host
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                # get the room code and just update this room's fields
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])

                # return the serialized Room data
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                # create a new room
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()

                # return the serialized CreateRoom data
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)