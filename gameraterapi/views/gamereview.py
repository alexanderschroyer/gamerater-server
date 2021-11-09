"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from gameraterapi.models import Game, Rater, game
from gameraterapi.models.review import Review

class GameReviewView(ViewSet):
    """Game Rater Game Reviews"""
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        rater = Rater.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["gameId"])

        try:
            review = Review.objects.create(
                game = game,
                rater = rater,
                content = request.data["content"],
                created_on = request.data["createdOn"]
            )
            serializer = GameReviewSerializer(review, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of game reviews
        """
        reviews = Review.objects.all()

        serializer = GameReviewSerializer(
            reviews, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single review

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            review = Review.objects.get(pk=pk)
            serializer = GameReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a review

        Returns:
            Response -- Empty body with 204 status code
        """
        rater = Rater.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=pk)

        review = Review.objects.get(pk=pk)
        review.rater = rater
        review.game = game
        review.content = request.data["content"]
        review.created_on = request.data["createdOn"]
        review.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single review

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            review = Review.objects.get(pk=pk)
            review.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    class Meta:
        model = Game
        fields = ('id', 'rater', 'title')

class GameReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for game reviews

    Arguments:
        serializer type
    """
    game = GameSerializer()
    rater = RaterSerializer()
    class Meta:
        model = Review
        fields = ('id', 'game', 'rater', 'content', 'created_on')