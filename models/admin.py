from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (Answer, Game, Guess, Participant, Question, Questionnaire,
                     User)

admin.site.register(User, UserAdmin)


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at', 'updated_at')
    ordering = ('title', 'user', 'created_at', 'updated_at')


admin.site.register(Questionnaire, QuestionnaireAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'questionnaire',
                    'created_at', 'updated_at', 'answerTime')
    list_filter = ('questionnaire', 'created_at', 'updated_at', 'answerTime')
    ordering = ('question', 'questionnaire',
                'created_at', 'updated_at', 'answerTime')


admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question', 'correct')
    list_filter = ('question', 'correct')
    ordering = ('answer', 'question', 'correct')


admin.site.register(Answer, AnswerAdmin)


class GameAdmin(admin.ModelAdmin):
    list_display = ('questionnaire', 'created_at', 'state',
                    'publicId', 'countdownTime', 'questionNo')
    list_filter = ('questionnaire', 'created_at', 'state',
                   'publicId', 'countdownTime', 'questionNo')
    ordering = ('questionnaire', 'created_at', 'state',
                'publicId', 'countdownTime', 'questionNo')


admin.site.register(Game, GameAdmin)


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('alias', 'game', 'points')
    list_filter = ('alias', 'game', 'points')
    ordering = ('alias', 'game', 'points')


admin.site.register(Participant, ParticipantAdmin)


class GuessAdmin(admin.ModelAdmin):
    list_display = ('participant', 'answer', 'question', 'game')
    list_filter = ('participant', 'answer', 'question', 'game')
    ordering = ('participant', 'answer', 'question', 'game')


admin.site.register(Guess, GuessAdmin)
