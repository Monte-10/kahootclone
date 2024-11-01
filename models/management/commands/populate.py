# Populate database
# This file has to be placed within the
# catalog/management/commands directory in your project.
# If that directory doesn't exist, create it.
# The name of the script is the name of the custom command,
# that is, populate.py.
#
# execute python manage.py  populate
#
# use module Faker generator to generate data
# (https://zetcode.com/python/faker/)
import os
import time

from django.core.management.base import BaseCommand
from models.models import User as User
from models.models import Questionnaire as Questionnaire
from models.models import Question as Question
from models.models import Answer as Answer
from models.models import Game as Game
from models.models import Participant as Participant

from faker import Faker
import random


# The name of this class is not optional must be Command
# otherwise manage.py will not process it properly
class Command(BaseCommand):
    # helps and arguments shown when command python manage.py help populate
    # is executed.
    help = """populate kahootclone database
           """
    # if you want to pass an argument to the function
    # uncomment this line

    def add_arguments(self, parser):
        parser.add_argument('publicId',
                            type=int,
                            help='game the participants will join to')
        parser.add_argument('sleep',
                            type=float,
                            default=2.,
                            help='wait this seconds until ' +
                            'inserting next participant')

    def __init__(self, sneaky=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # "if 'RENDER'" allows you to deal with different
        # behaviour in render.com and locally
        # That is, we check a variable ('RENDER')
        # that is only defined in render.com
        if 'RENDER' in os.environ:
            pass
        else:
            pass

        self.user_array = []
        self.questionnaire_array = []
        self.question_array = []
        self.answer_array = []
        self.game_array = []

        self.NUMBERUSERS = 4
        self.NUMBERQESTIONARIES = 30
        self.NUMBERQUESTIONS = 100
        self.NUMBERPARTICIPANTS = 20
        self.NUMBERANSWERPERQUESTION = 4
        self.NUMBERGAMES = 4

    # handle is another compulsory name, do not change it"
    # handle function will be executed by 'manage populate'
    def handle(self, *args, **kwargs):
        "this function will be executed by default"

        self.faker = Faker()

        # if no argument populate database
        if not kwargs['publicId']:
            self.cleanDataBase()   # clean database
            # The faker.Faker() creates and initializes a faker generator,
            self.user()  # create users
            self.questionnaire()  # create questionaries
            self.question()  # create questions
            self.answer()  # create answers
            self.game()  # create games
        else:
            self.publicId = kwargs['publicId']
            self.sleep = kwargs['sleep']
            self.participants()

    def cleanDataBase(self):
        # delete all models stored (clean table)
        # in database
        # order in which data is deleted is important
        Game.objects.all().delete()
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Questionnaire.objects.all().delete()
        User.objects.all().delete()
        print("clean Database")

    def user(self):
        " Insert users"
        # create user
        print("Users")
        # create random users
        for _ in range(self.NUMBERUSERS):
            username = self.faker.unique.user_name()
            email = self.faker.unique.email()
            password = self.faker.password(length=10)
            user = User(username=username, email=email, password=password)
            self.user_array.append(user)
            user.save()

    def questionnaire(self):
        "insert questionnaires"
        print("questionnaire")
        # assign users randomly to the questionnaires
        for _ in range(self.NUMBERQESTIONARIES):
            title = self.faker.sentence()
            user = random.choice(self.user_array)

            # creating a questionnaire instance
            questionnaire = Questionnaire(title=title, user=user)
            self.questionnaire_array.append(questionnaire)
            questionnaire.save()

    def question(self):
        " insert questions, assign randomly to questionnaires"
        print("Question")
        # your code goes here
        # assign questions randomly to the questionnaires
        for _ in range(self.NUMBERQUESTIONS):
            question = self.faker.sentence() + "?"
            questionnaire = random.choice(self.questionnaire_array)
            answerTime = self.faker.random_int(min=0)

            # creating a questionnaire instance
            question = Question(
                question=question, questionnaire=questionnaire,
                answerTime=answerTime)
            self.question_array.append(question)
            question.save()

    def answer(self):
        "insert answers, one of them must be the correct one"
        print("Answer")
        # your code goes here
        # assign answer randomly to the questions
        # maximum number of answers per question is four
        for question in self.question_array:
            numberOfAnswers = random.randint(2, self.NUMBERANSWERPERQUESTION)
            correctAnswer = random.choice(
                [num for num in range(numberOfAnswers)])
            for i in range(numberOfAnswers):
                answer = self.faker.sentence()
                correct = (i == correctAnswer)

                # creating a questionnaire instance
                answer = Answer(
                    answer=answer, question=question, correct=correct)
                answer.save()

    def game(self):
        '''
        Inserts games
        created_at: se asigna el tiempo actual en la creación
        state, countdownTime, questionNo: tienen valores por defecto
        publicId: se asigna al llamar a la función save()
        '''
        print("Game")
        # publicId must be unique
        # publicId = random.randint(1,10**6)
        for _ in range(self.NUMBERGAMES):
            # choose at random the questionnaries
            questionnaire = random.choice(self.questionnaire_array)
            # publicId = publicId + i
            # countdownTime = random.randint(0,60)
            # countdownTime by default
            # creating a questionnaire instance
            game = Game(questionnaire=questionnaire)
            game.save()

    def participants(self):
        '''
        Inserts participants
        '''
        print("Participants")
        for _ in range(self.NUMBERPARTICIPANTS):
            game = Game.objects.get(publicId=self.publicId)
            alias = self.faker.user_name()
            points = random.randint(0, 100)
            participant = Participant(game=game, alias=alias, points=points)
            participant.save()
            time.sleep(self.sleep)
