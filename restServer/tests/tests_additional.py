from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from models.models import (Game, Guess, Participant,
                           User, Questionnaire, Question, Answer)
from rest_framework.reverse import reverse
from models.constants import QUESTION, ANSWER

PARTICIPANT_LIST = "participant-list"

GUESS_LIST = "guess-list"


class RestTests(APITestCase):
    """ additional tests for the rest framework
    """

    def setUp(self):
        # ApiClient acts as a dummy web browser,
        # allowing you to test your views
        # and interact with your Django application programmatically.
        self.client = APIClient()
        # create user
        self.userDict = {"username": 'a',
                         "password": 'a',
                         "first_name": 'a',
                         "last_name": 'a',
                         "email": 'a@aa.es'
                         }
        user, created = User.objects.get_or_create(**self.userDict)
        # save password encripted
        if created:
            user.set_password(self.userDict['password'])
            user.save()
        self.user = user

        # create questionnaire
        self.questionnaireDict = {"title": 'questionnaire_title',
                                  "user": self.user
                                  }
        self.questionnaire = Questionnaire.objects.get_or_create(
            **self.questionnaireDict)[0]

        # create a few questions
        # question 1
        self.questionDict = {"question": 'this is a question',
                             "questionnaire": self.questionnaire,
                             }
        self.question = Question.objects.get_or_create(**self.questionDict)[0]

        # question2
        self.questionDict2 = {"question": 'this is a question2',
                              "questionnaire": self.questionnaire,
                              }
        self.question2 = Question.objects.get_or_create(
            **self.questionDict2)[0]

        # create a few answers
        # answer1
        self.answerDict = {"answer": 'this is an answer',
                           "question": self.question,
                           "correct": True
                           }
        self.answer = Answer.objects.get_or_create(**self.answerDict)[0]

        # answer2
        self.answerDict2 = {"answer": 'this is an answer2',
                            "question": self.question,
                            "correct": False
                            }
        self.answer2 = Answer.objects.get_or_create(**self.answerDict2)[0]

        # answer3
        self.answerDict3 = {"answer": 'this is an answer3',
                            "question": self.question2,
                            "correct": True
                            }
        self.answer3 = Answer.objects.get_or_create(**self.answerDict3)[0]

        # create a game
        self.gameDict = {
            'questionnaire': self.questionnaire,
            'publicId': 123456,
        }
        self.game = Game.objects.get_or_create(**self.gameDict)[0]

        # create a participant
        self.participantDict = {
            'game': self.game,
            'alias': "pepe"}
        self.participant = Participant.objects.get_or_create(
            **self.participantDict)[0]

        # create a guess
        self.guessDict = {
            'participant': self.participant,
            'game': self.game,
            'question': self.question,
            'answer': self.answer,
            }
        self.guess = Guess.objects.get_or_create(**self.guessDict)[0]

    @classmethod
    def decode(cls, txt):
        """convert the html return by the client in something that may
           by printed on the screen"""
        return txt.decode("utf-8")

    def test_01a_add_participant(self):
        "participant creation errors"
        url = reverse(PARTICIPANT_LIST)

        data = {'game': self.gameDict['publicId'], 'alias': ""}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'game': self.gameDict['publicId']+1,
                'alias': "luis"}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.game.state = QUESTION
        self.game.save()
        data = {'game': self.gameDict['publicId'],
                'alias': "luis"}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_02a_add_guess(self):
        "guess creation errors"
        self.game.state = ANSWER
        self.game.save()
        url = reverse(GUESS_LIST)
        self.game.questionNo = self.game.questionNo + 1
        self.game.save()
        data = {'uuidp': self.participant.uuidP,
                'game': self.gameDict['publicId'],
                'answer': 3,
                }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = {'uuidp': 1,
                'game': self.gameDict['publicId'],
                'answer': 0,
                }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = {'uuidp': self.participant.uuidP,
                'game': self.gameDict['publicId']+1,
                'answer': 0,
                }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
