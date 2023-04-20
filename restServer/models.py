from django.db import models
from models.models import *

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    class Meta:
        ordering = ['id']
        
class Answers(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField()
    correct = models.BooleanField()
    
    class Meta:
        ordering = ['id']

class Games(models.Model):
    created_at = models.DateTimeField()
    state = models.IntegerField()
    publicId = models.IntegerField()
    questionNo = models.IntegerField()
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['id']

class Participant(models.Model):
    alias = models.CharField(max_length=20)
    uuidP = models.UUIDField(default=uuid.uuid4, editable=False)
    points = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['id']
    
class Guess(models.Model):