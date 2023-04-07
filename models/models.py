from django.contrib.auth.models import AbstractUser
from django.db import models
from .constants import WAITING, QUESTION, ANSWER, LEADERBOARD, GAME_STATES
import uuid
import random



class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.username
    
class Questionnaire(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.CharField(max_length=255)
    question = models.CharField(max_length=255)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    answerTime = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.questionnaire.title}: {self.text}"


class Answer(models.Model):
    answer = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class Game(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(choices=GAME_STATES, default=WAITING)
    publicId = models.IntegerField(unique=True, default=random.randint(100000,999999))
    countdownTime = models.IntegerField(default=0)
    questionNo = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.publicId = random.randint(100000, 999999)
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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.participant.points += 1 if self.answer.correct else 0
            self.participant.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.participant.alias}: {self.question} - {self.answer.answer}"
    
