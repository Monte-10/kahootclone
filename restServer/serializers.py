from models.models import Game, Participant, Guess
from rest_framework import serializers
        
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        lookup_field = 'publicId'
        
class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'
        
class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = '__all__'