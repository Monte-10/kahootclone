from django.db import models
from models.models import *

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    url = models.URLField(max_length=100)
    class Meta:
        ordering = ['id']
        
class Answers(models.Model):
    answer = models.ForeignKey(Answer)
    question = models.ForeignKey(Question)
    order = models.IntegerField()
    correct = models.BooleanField()
    url = models.URLField(max_length=100)

    
    class Meta:
        ordering = ['id']

class Games(models.Model):
    created_at = models.DateTimeField()
    state = models.IntegerField()
    publicId = models.IntegerField()
    questionNo = models.IntegerField()
    questionnaire = models.IntegerField()

class Participant(models.Model):
    alias = models.CharField(max_length=20)
    uuidP = models.UUIDField(default=uuid.uuid4, editable=False)
    points = models.IntegerField()
    game = models.ForeignKey(Game)
    
    class Meta:
        ordering = ['id']
    
class Guess(models.Model):