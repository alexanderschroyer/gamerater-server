"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from gameraterapi.models import Game, Rater

class GameView(ViewSet):
    """Game Rater Games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        rater = Rater.objects.get(user=request.auth.user)

        try:
            game = Game.objects.create(
                rater=rater,
                title=request.data["title"],
                description=request.data["description"],
                designer=request.data["designer"],
                year_released=request.data["yearReleased"],
                number_of_players=request.data["numberOfPlayers"],
                estimated_time_to_play=request.data["estimatedTimeToPlay"],
                age_recommendation=request.data["ageRecommendation"],
                created_on=request.data["createdOn"]
            )
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        rater = Rater.objects.get(user=request.auth.user)

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.year_released = request.data["yearReleased"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.estimated_time_to_play = request.data["estimatedTimeToPlay"]
        game.created_on = request.data["createdOn"]
        game.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')

class RaterSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    user = UserSerializer()
    class Meta:
        model = Rater
        fields = ('id', 'user', 'bio')

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    rater = RaterSerializer()
    class Meta:
        model = Game
        fields = ('id', 'rater', 'title', 'description', 'designer', 'year_released', 'number_of_players', 'estimated_time_to_play', 'age_recommendation', 'created_on')