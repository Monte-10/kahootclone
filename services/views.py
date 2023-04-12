from django.urls import reverse_lazy

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView, TemplateView

from models.models import (
    Answer, Game, Guess, Participant, Question, Questionnaire)

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin

from models.constants import WAITING, QUESTION, ANSWER, LEADERBOARD


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            questionnaires = Questionnaire.objects.filter(
                user=self.request.user).order_by('-updated_at')[:5]
            context['latest_questionnaire_list'] = questionnaires
        return context


class QuestionnaireDetail(LoginRequiredMixin, DetailView):
    model = Questionnaire
    template_name = 'services/questionnaire_detail.html'
    redirect_field_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        questionnaire = self.get_object()
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class QuestionnaireList(LoginRequiredMixin, ListView):
    model = Questionnaire
    template_name = 'services/questionnaire_list.html'
    redirect_field_name = 'login'


class QuestionnaireRemove(LoginRequiredMixin, DeleteView):
    model = Questionnaire
    template_name = 'services/questionnaire_remove.html'
    success_url = reverse_lazy('questionnaire-list')
    redirect_field_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        questionnaire = self.get_object()
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class QuestionnaireUpdate(LoginRequiredMixin, UpdateView):
    model = Questionnaire
    template_name = 'services/questionnaire_update.html'
    fields = ['title']
    redirect_field_name = 'login'

    def get_success_url(self):
        return reverse_lazy('questionnaire-detail',
                            kwargs={'pk': self.object.id})

    def dispatch(self, request, *args, **kwargs):
        questionnaire = self.get_object()
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class QuestionnaireCreate(LoginRequiredMixin, CreateView):
    model = Questionnaire
    template_name = 'services/questionnaire_create.html'
    fields = ['title']
    redirect_field_name = 'login'

    def get_success_url(self):
        return reverse_lazy('questionnaire-detail',
                            kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionDetail(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'services/question_detail.html'
    redirect_field_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        questionnaire = self.get_object().questionnaire
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class QuestionRemove(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'services/question_remove.html'
    redirect_field_name = 'login'

    def get_success_url(self):
        return reverse_lazy('questionnaire-detail',
                            kwargs={'pk': self.object.questionnaire.id})

    def dispatch(self, request, *args, **kwargs):
        questionnaire = self.get_object().questionnaire
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class QuestionUpdate(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'services/question_update.html'
    fields = ['question', 'answerTime', 'value']
    redirect_field_name = 'login'

    def get_success_url(self):
        return reverse_lazy('question-detail', kwargs={'pk': self.object.id})

    def dispatch(self, request, *args, **kwargs):
        questionnaire = self.get_object().questionnaire
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'services/question_create.html'
    fields = ['question', 'answerTime', 'value']
    redirect_field_name = 'login'

    def get_success_url(self):
        return reverse_lazy('question-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        questionnaire = get_object_or_404(
            Questionnaire, pk=self.kwargs['questionnaireid'])
        form.instance.questionnaire = questionnaire
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        questionnaire = get_object_or_404(
            Questionnaire, pk=self.kwargs['questionnaireid'])
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class AnswerCreate(LoginRequiredMixin, CreateView):
    model = Answer
    template_name = 'services/answer_create.html'
    fields = ['answer', 'correct']
    redirect_field_name = 'login'

    def get_success_url(self):
        return reverse_lazy('question-detail',
                            kwargs={'pk': self.object.question.id})

    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs['questionid'])
        form.instance.question = question
        return super(AnswerCreate, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs['questionid'])
        questionnaire = question.questionnaire
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class AnswerRemove(LoginRequiredMixin, DeleteView):
    model = Answer
    template_name = 'services/answer_remove.html'
    redirect_field_name = 'login'

    def get_success_url(self):
        return reverse_lazy('question-detail',
                            kwargs={'pk': self.object.question.id})

    def dispatch(self, request, *args, **kwargs):
        questionnaire = self.get_object().question.questionnaire
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class AnswerUpdate(LoginRequiredMixin, UpdateView):
    model = Answer
    template_name = 'services/answer_update.html'
    fields = ['answer', 'correct']
    redirect_field_name = 'login'

    def get_success_url(self):
        return reverse_lazy('question-detail',
                            kwargs={'pk': self.object.question.id})

    def dispatch(self, request, *args, **kwargs):
        questionnaire = self.get_object().question.questionnaire
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class GameCreate(LoginRequiredMixin, TemplateView):
    template_name = 'services/game_create.html'
    redirect_field_name = 'login'

    def get_context_data(self, **kwargs):

        context = super(GameCreate, self).get_context_data(**kwargs)
        questionnaire = get_object_or_404(
            Questionnaire, pk=self.kwargs['questionnaireid'])

        if self.request.user.is_authenticated:
            game = Game(questionnaire=questionnaire)
            game.save()
            context['game'] = game
            context['is_owner'] = (questionnaire.user == self.request.user)
            session = self.request.session
            session['gameID'] = game.publicId
            session['game_state'] = game.state
            session['is_owner'] = (questionnaire.user == self.request.user)
        return context


class UpdateParticipant(LoginRequiredMixin, TemplateView):
    template_name = 'services/game_updateparticipant.html'
    redirect_field_name = 'login'

    def get_context_data(self, **kwargs):
        context = super(UpdateParticipant, self).get_context_data(**kwargs)
        gameID = self.request.session.get('gameID')
        game = get_object_or_404(Game, publicId=gameID)
        participants = Participant.objects.filter(game=game)
        context['participants'] = participants
        context['is_owner'] = self.request.session.get('is_owner')
        return context


class CountDown(LoginRequiredMixin, TemplateView):
    redirect_field_name = 'login'

    def get_template_names(self):
        gameID = self.request.session.get('gameID')
        game = get_object_or_404(Game, publicId=gameID)
        if game.state == WAITING:
            game.state = QUESTION
            game.save()
            self.request.session['game_state'] = game.state
            return 'services/game_countdown.html'
        elif game.state == QUESTION:
            game.state = ANSWER
            game.save()
            self.request.session['game_state'] = game.state
            return 'services/game_question.html'
        elif game.state == ANSWER:
            if game.questionNo == game.questionnaire.question_set.count()-1:
                game.state = LEADERBOARD
            else:
                game.questionNo += 1
                game.state = QUESTION
            self.request.session['game_state'] = game.state
            game.save()
            return 'services/game_answer.html'
        else:
            return 'services/game_leaderboard.html'

    def get_context_data(self, **kwargs):
        context = super(CountDown, self).get_context_data(**kwargs)
        gameID = self.request.session.get('gameID')
        game = get_object_or_404(Game, publicId=gameID)
        context['game'] = game
        question = game.questionnaire.question_set.all()[game.questionNo]
        context['question'] = question
        if game.state == ANSWER:
            guesses = Guess.objects.filter(question=question, game=game)
            participants = Participant.objects.filter(game=game).count()
            correct = guesses.filter(answer__correct=True).count()
            context['percentage'] = round(
                correct/participants*100, 2) if participants > 0 else 0

        return context
