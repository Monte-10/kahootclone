from django.http import JsonResponse
from models.models import Game, Participant, Guess
from rest_framework import viewsets
from .serializers import GameSerializer, ParticipantSerializer, GuessSerializer
from rest_framework.permissions import AllowAny
from models.constants import ANSWER, WAITING

# Create your views here.
class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all().order_by('id')
    serializer_class = ParticipantSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kargs):
        if not request.data['alias'] or not request.data['game']:
            return JsonResponse(
                {'error': 'You must fill both fields'}, 
                status=400)
            
        id = int(request.data['game'])
        alias = request.data['alias']
        game = Game.objects.filter(publicId=id)
        
        if game.exists():
            if game.first().state != WAITING:
                return JsonResponse(
                    {'error': 'Game already started'}, 
                    status=400)
                
            privateId = game.first().id
            request.data['game'] = privateId
            aliasExist = Participant.objects.filter(
                alias=alias, game=privateId).exists()
            
            if aliasExist:
                return JsonResponse(
                    {'error': 'Alias already exists, choose another one.'}, 
                    status=403)
            else:
                return super().create(request, *args, **kargs)
        
        else:
            return JsonResponse(
                {'error': 'Game not found.'}, 
                status=404)
            
    def retrieve(self, request, *args, **kwargs):
        return JsonResponse(
            {'error': 'Authentication credentials were not provided.'},
            status=404)
        
    def list(self, request, *args, **kwargs):
        return JsonResponse(
            {'error': 'Authentication credentials were not provided.'},
            status=404)
        
    def update(self, request, *args, **kwargs):
        return JsonResponse(
            {'error': 'Authentication credentials were not provided.'},
            status=404)
    
    def destroy(self, request, *args, **kwargs):
        return JsonResponse(
            {'error': 'Authentication credentials were not provided.'},
            status=404)
        
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'publicId'
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kargs):
        pass
    
class GuessViewSet(viewsets.ModelViewSet):
    queryset = Guess.objects.all()
    serializer_class = GuessSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kargs):
        id = int(request.data['game'])
        uuidP = request.data['uuidp']
        answerNo = int(request.data['answer'])
        
        game = Game.objects.filter(publicId=id)
        if game.exists():
            game = game.first()
            if game.state == ANSWER:
                questionNo = game.questionNo
                questionnaire = game.questionnaire
                question = questionnaire.question_set.all()[questionNo]
                participant = Participant.objects.filter(
                    uuidP=uuidP, game=game.id)
                if participant.exists():
                    answerExist = Guess.objects.filter(
                        game=game.id, 
                        participant=participant.first().id,
                        question=question.id).exists()
                    if answerExist:
                        return JsonResponse(
                            {'error': 'Answer already exists'}, 
                            status=403)
                    else:
                        long = question.answer_set.all().count()
                        if answerNo < 0 or answerNo >= long:
                            return JsonResponse(
                                {'error': 'Answer not found'},
                                status=404)
                        else:
                            answer = question.answer_set.all()[answerNo]
                        request.data['answer'] = answer.id
                        request.data['question'] = question.id
                        request.data['participant'] = participant.first().id
                        request.data['game'] = game.id
                        return super().create(request, *args, **kargs)
                    
                else:
                    return JsonResponse(
                        {'error': 'Participant not found.'},
                        status=404)
            else:
                return JsonResponse(
                    {'error': 'wait until the question is shown.'},
                    status=403)
        else:
            return JsonResponse(
                {'error': 'Game not found.'},
                status=404)
            
    def retrieve(self, request, *args, **kwargs):
        return JsonResponse(
            {'error': 'Authentication credentials were not provided.'},
            status=404)
        
    def list(self, request, *args, **kwargs):
        return JsonResponse(
            {'error': 'Authentication credentials were not provided.'},
            status=404)
        
    def update(self, request, *args, **kwargs):
        return JsonResponse(
            {'error': 'Authentication credentials were not provided.'},
            status=403)
        
    def destroy(self, request, *args, **kwargs):
        return JsonResponse(
            {'error': 'Authentication credentials were not provided.'},
            status=403)