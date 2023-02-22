"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game


class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        event = Event.objects.get(pk=pk) 
        serializer = EventSerializer(event) #serialize to convert data to json
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        
        events = Event.objects.all()

        if "game" in request.query_params:
            query = request.GET.get('game')
            query_int = int(query)
            events = Event.objects.all()
            events = events.filter(game_id=query_int)
        else:
            events = Event.objects.all()

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        #getting the user that is logged in 
        organizing_gamer = Gamer.objects.get(user=request.auth.user)
        #retrieve game from database. make sure the game the user is trying to add with new event actually exists in database  
        game = Game.objects.get(pk=request.data["game"])

        #whichever keys are used on the request.data must match what the client is passing to the server.
        event = Event.objects.create(
            location=request.data["location"],
            date_of_event=request.data["date_of_event"],
            start_time=request.data["start_time"],
            organizing_gamer=organizing_gamer,
            game=game
            
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a event
        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.location = request.data["location"]
        event.date_of_event = request.data["date"]
        event.start_time = request.data["start_time"]

        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class EventGameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:
        model = Game
        fields = ('id', 'title',)

class OrganizerSerializer(serializers.ModelSerializer):
    """JSON serializer for organizers
    """
    class Meta:
        model = Gamer
        fields = ('full_name',)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    game = EventGameSerializer(many=False)
    organizing_gamer = OrganizerSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id','organizing_gamer', 'game', 'location',
                'date_of_event', 'start_time')        