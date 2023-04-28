from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .constants import WAITING, QUESTION, ANSWER, LEADERBOARD
import uuid
import random


class User(AbstractUser):
    pass


class Questionnaire(models.Model):
    """
    Modelo que representa un cuestionario
    """
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Devuelve el titulo del cuestionario representado por el modelo"""
        return self.title

    class Meta:
        """Ordena la lista de cuestionarios por fecha de actualización"""
        ordering = ['-updated_at']


class Question(models.Model):
    """Modelo que representa una pregunta"""
    question = models.CharField(max_length=255)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    answerTime = models.IntegerField(
        validators=[MinValueValidator(0)], default=20, blank=True)
    value = models.IntegerField(default=1)
    """Devuelve un string con la pregunta representada por el modelo"""
    def __str__(self):
        return self.question


class Answer(models.Model):
    """Modelo que representa una respuesta"""
    answer = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField()
    """Devuelve un string con la respuesta representada por el modelo"""
    def __str__(self):
        return self.answer


class Game(models.Model):
    """Modelo que representa un juego"""
    STATE_CHOICES = (
        (WAITING, 'Waiting'),
        (QUESTION, 'Question'),
        (ANSWER, 'Answer'),
        (LEADERBOARD, 'Leaderboard'),
    )

    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(choices=STATE_CHOICES, default=WAITING)
    publicId = models.IntegerField(unique=True, validators=[
                            MinValueValidator(1), MaxValueValidator(10**6)])
    countdownTime = models.IntegerField(
        validators=[MinValueValidator(0)], default=3)
    questionNo = models.IntegerField(default=0)
    """Le asigna un publicId al juego si no tiene uno"""
    def save(self, *args, **kwargs):
        if not self.publicId:
            while True:
                self.publicId = random.randint(1, 10**6)
                if not Game.objects.filter(publicId=self.publicId).exists():
                    break
        super(Game, self).save(*args, **kwargs)
    """
    Devuelve un string con el publicId del juego representado 
    por el modelo
    """
    def __str__(self):
        return str(self.publicId)


class Participant(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    alias = models.CharField(max_length=255, default="Anonymous")
    points = models.IntegerField(default=0)
    uuidP = models.UUIDField(default=uuid.uuid4, editable=False)
    """
    Devuelve un string con el alias del participante representado 
    por el modelo
    """
    def __str__(self):
        return self.alias



class Guess(models.Model):
    """Modelo que representa una respuesta a una pregunta"""
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    """
    Guarda la respuesta y suma los puntos al participante
    """
    def save(self, *args, **kwargs):
        self.participant.points += (self.question.value
                                    if self.answer.correct else 0)

        self.participant.save()
        super(Guess, self).save(*args, **kwargs)
    """
    Devuelve un string con la respuesta representada por el modelo
    """
    def __str__(self):
        return self.answer
