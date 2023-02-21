"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game,GameType,Gamer


class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        game = Game.objects.get(pk=pk) 
        serializer = GameSerializer(game) #serialize to convert data to json
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        #getting the user that is logged in 
        #use request.auth.user to get Gamer obj based on user
        gamer = Gamer.objects.get(user=request.auth.user)
        #retrieve GameType from database. make sure the game type the user is trying to add with new game actually exists in database  
        game_type = GameType.objects.get(pk=request.data["game_type"])

        #whichever keys are used on the request.data must match what the client is passing to the server.
        game = Game.objects.create(
            title=request.data["title"],
            min_age=request.data["min_age"],
            min_players=request.data["min_players"],
            max_players=request.data["max_players"],
            gamer=gamer,
            game_type=game_type
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:
        model = Game
        fields = ('game_type', 'gamer', 'title',
                'min_age', 'min_players', 'max_players')
        depth = 1        