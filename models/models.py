from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import random



class User(AbstractUser):
    pass
    username = models.CharField(max_length=30, unique=True)
    
    groups = None
    user_permissions = None
    
    USERNAME_FIELD = 'username'
    
    def __str__(self):
        return self.username
    
class Questionnaire(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.CharField(max_length=255)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.questionnaire.title}: {self.text}"


class Answer(models.Model):
    answer = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer


class Game(models.Model):
    WAITING = 1
    QUESTION = 2
    ANSWER = 3
    LEADERBOARD = 4
    STATE_CHOICES = [
        (WAITING, 'Waiting'),
        (QUESTION, 'Question'),
        (ANSWER, 'Answer'),
        (LEADERBOARD, 'Leaderboard'),
    ]
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.IntegerField(choices=STATE_CHOICES, default=WAITING)
    public_id = models.IntegerField(unique=True)
    countdown_time = models.IntegerField(default=0)
    question_no = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.public_id = random.randint(1, 10)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.questionnaire.title} ({self.created_at})"


class Participant(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    alias = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    uuidP = models.UUIDField(default=uuid.uuid4, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.points = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.alias} ({self.game})"



class Guess(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.participant.points += 1 if self.answer.correct else 0
            self.participant.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.participant.alias}: {self.question} - {self.answer.answer}"