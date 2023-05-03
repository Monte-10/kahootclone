from django.http import JsonResponse
from models.models import Game, Participant, Guess
from rest_framework import viewsets
from .serializers import GameSerializer, ParticipantSerializer, GuessSerializer
from rest_framework import permissions
from models.constants import ANSWER, WAITING

# Create your views here.
class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all().order_by('id')
    serializer_class = ParticipantSerializer
    permission_classes = []
    
    
    def get_permissions(self):
        """
        Se encarga de definir los permisos de cada método.
        
        Args:  
            self: instancia de la clase.
            
        Returns:
            Lista de permisos.
        """
        if self.action == 'create':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()
    
    def create(self, request, *args, **kargs):
        """
        Se encarga de crear un participante en una partida con
        la informacion recibida en la peticion. Si la partida
        existe y el alias no esta en uso, crea el participante.
        
        Args:
            self: instancia de la clase.
            request: peticion recibida.
            *args: argumentos.
            **kargs: argumentos clave.
            
        Returns:
            Respuesta de la peticion.
            
        Author:
            Alejandro Monterrubio
        """
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
            
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'publicId'
    
    def get_permissions(self):
        """
        Se encarga de definir los permisos de cada método.
        
        Args:  
            self: instancia de la clase.
            
        Returns:
            Lista de permisos.
            
        Author:
            Pablo Hernaez
        """
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()
    
class GuessViewSet(viewsets.ModelViewSet):
    queryset = Guess.objects.all()
    serializer_class = GuessSerializer
    permission_classes = []
    
    def get_permissions(self):
        """
        Se encarga de definir los permisos de cada método.
        
        Args:  
            self: instancia de la clase.
            
        Returns:
            Lista de permisos.
        """
        if self.action == 'create':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()
    
    def create(self, request, *args, **kargs):
        """
        Se encarga de crear una respuesta en una partida con
        la informacion recibida en la peticion. Si la partida
        existe y el participante existe y este
        no ha respondido antes, crea la respuesta.
        
        Args:
            self: instancia de la clase.
            request: peticion recibida.
            *args: argumentos.
            **kargs: argumentos clave.
            
        Returns:
            Respuesta de la peticion.

        Author:
            Juan Francisco Flores
        """
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
                    status=404)
        else:
            return JsonResponse(
                {'error': 'Game not found.'},
                status=404)
