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
    """
    Vista de inicio.
    
    Esta vista se encarga de mostrar la página de inicio de la aplicación.
    
    Autor: Alejandro Monterrubio
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """
        Devuelve el contexto de la vista de inicio.
        
        Este metodo se encarga de devolver el contexto de la vista de home,
        que tambien incluye los cuestionarios del usuario si este esta
        autenticado.
        
        :param self: Instancia de la clase
        :param kwargs: Argumentos clave
        
        :return: Contexto de la vista de inicio
        """
        context = super(Home, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            questionnaires = Questionnaire.objects.filter(
                user=self.request.user).order_by('-updated_at')[:5]
            context['latest_questionnaire_list'] = questionnaires
        return context


class QuestionnaireDetail(LoginRequiredMixin, DetailView):
    """
    Vista de detalle de un cuestionario.
    
    Esta vista se encarga de mostrar el detalle de un cuestionario.
    
    Autor: Alejandro Monterrubio
    """
    model = Questionnaire
    template_name = 'services/questionnaire_detail.html'
    redirect_field_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        """
        Comprueba que el usuario que hace la petición es el mismo que el
        usuario que ha creado el cuestionario.
        
        :param self: Instancia de la clase
        :param request: Petición HTTP
        :param args: Argumentos
        :param kwargs: Argumentos clave
        
        :return: Redirige a la lista de cuestionarios si el usuario no es el
        """
        questionnaire = self.get_object()
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class QuestionnaireList(LoginRequiredMixin, ListView):
    """
    Vista de lista de cuestionarios.
    
    Esta vista se encarga de mostrar la lista de cuestionarios del usuario.
    
    Autor: Alejandro Monterrubio
    """
    model = Questionnaire
    template_name = 'services/questionnaire_list.html'
    redirect_field_name = 'login'


class QuestionnaireRemove(LoginRequiredMixin, DeleteView):
    """
    Vista de eliminación de un cuestionario.
    
    Esta vista se encarga de eliminar un cuestionario.
    
    Autor: Alejandro Monterrubio
    """
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
    """
    Vista de actualización de un cuestionario.
    
    Esta vista se encarga de actualizar un cuestionario.
    
    Autor: Alejandro Monterrubio
    """
    model = Questionnaire
    template_name = 'services/questionnaire_update.html'
    fields = ['title']
    redirect_field_name = 'login'

    def get_success_url(self):
        """
        Devuelve la URL a la que se redirige al actualizar un cuestionario.
        
        Este metodo se encarga de devolver la URL a la que se redirige al
        actualizar un cuestionario.
        
        :param self: Instancia de la clase
        
        :return: URL a la que se redirige al actualizar un cuestionario
        """
        return reverse_lazy('questionnaire-detail',
                            kwargs={'pk': self.object.id})

    def dispatch(self, request, *args, **kwargs):
        """
        Comprueba que el usuario que hace la petición es el mismo que el
          
        :param self: Instancia de la clase
        :param request: Petición HTTP
        :param args: Argumentos
        :param kwargs: Argumentos clave
        
        :return: Redirige a la lista de cuestionarios si el usuario no es el
        """
        questionnaire = self.get_object()
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class QuestionnaireCreate(LoginRequiredMixin, CreateView):
    """
    Vista de creación de un cuestionario.
    
    Esta vista se encarga de crear un cuestionario.
    
    Autor: Alejandro Monterrubio
    """
    model = Questionnaire
    template_name = 'services/questionnaire_create.html'
    fields = ['title']
    redirect_field_name = 'login'

    def get_success_url(self):
        """
        Devuelve la URL a la que se redirige al crear un cuestionario.
        
        Este metodo se encarga de devolver la URL a la que se redirige al
        crear un cuestionario.
        
        :param self: Instancia de la clase
        
        :return: URL a la que se redirige al crear un cuestionario
        """
        return reverse_lazy('questionnaire-detail',
                            kwargs={'pk': self.object.id})

    def form_valid(self, form):
        """
        Comprueba que el usuario que hace la petición es el mismo que el
        
        :param self: Instancia de la clase
        :param form: Formulario
        
        :return: Devuelve el formulario
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionDetail(LoginRequiredMixin, DetailView):
    """
    Vista de detalle de una pregunta.
    
    Esta vista se encarga de mostrar el detalle de una pregunta.
    
    Autor: Alejandro Monterrubio
    """
    model = Question
    template_name = 'services/question_detail.html'
    redirect_field_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        """
        Comprueba que el usuario que hace la petición es el mismo que el
        
        :param self: Instancia de la clase
        :param request: Petición HTTP
        :param args: Argumentos
        :param kwargs: Argumentos clave
        
        :return: Redirige a la lista de cuestionarios si el usuario no es el
        """
        questionnaire = self.get_object().questionnaire
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class QuestionRemove(LoginRequiredMixin, DeleteView):
    """
    Vista de eliminación de una pregunta.
    
    Esta vista se encarga de eliminar una pregunta.
    
    Autor: Alejandro Monterrubio
    """
    model = Question
    template_name = 'services/question_remove.html'
    redirect_field_name = 'login'

    def get_success_url(self):
        """
        Devuelve la URL a la que se redirige al eliminar una pregunta.
        
        Este metodo se encarga de devolver la URL a la que se redirige al
        eliminar una pregunta.
        
        :param self: Instancia de la clase
        
        :return: URL a la que se redirige al eliminar una pregunta
        """
        return reverse_lazy('questionnaire-detail',
                            kwargs={'pk': self.object.questionnaire.id})

    def dispatch(self, request, *args, **kwargs):
        """
        Comprueba que el usuario que hace la petición es el mismo que el
        
        :param self: Instancia de la clase
        :param request: Petición HTTP
        :param args: Argumentos
        :param kwargs: Argumentos clave
        
        :return: Redirige a la lista de cuestionarios si el usuario no es el
        """
        questionnaire = self.get_object().questionnaire
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class QuestionUpdate(LoginRequiredMixin, UpdateView):
    """
    Vista de actualización de una pregunta.
    
    Esta vista se encarga de actualizar una pregunta.
    
    Autor: Alejandro Monterrubio
    """
    model = Question
    template_name = 'services/question_update.html'
    fields = ['question', 'answerTime', 'value']
    redirect_field_name = 'login'

    def get_success_url(self):
        """
        Devuelve la URL a la que se redirige al actualizar una pregunta.
        
        Este metodo se encarga de devolver la URL a la que se redirige al
        actualizar una pregunta.
        
        :param self: Instancia de la clase
        
        :return: URL a la que se redirige al actualizar una pregunta
        """
        return reverse_lazy('question-detail', kwargs={'pk': self.object.id})

    def dispatch(self, request, *args, **kwargs):
        """
        Comprueba que el usuario que hace la petición es el mismo que el
        
        :param self: Instancia de la clase
        :param request: Petición HTTP
        :param args: Argumentos
        :param kwargs: Argumentos clave
        
        :return: Redirige a la lista de cuestionarios si el usuario no es el
        """
        questionnaire = self.get_object().questionnaire
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class QuestionCreate(LoginRequiredMixin, CreateView):
    """
    Vista de creación de una pregunta.
    
    Esta vista se encarga de crear una pregunta.
    
    Autor: Alejandro Monterrubio
    """
    model = Question
    template_name = 'services/question_create.html'
    fields = ['question', 'answerTime', 'value']
    redirect_field_name = 'login'

    def get_success_url(self):
        """
        Devuelve la URL a la que se redirige al crear una pregunta.
        
        Este metodo se encarga de devolver la URL a la que se redirige al
        crear una pregunta.
        
        :param self: Instancia de la clase
        
        :return: URL a la que se redirige al crear una pregunta
        """
        return reverse_lazy('question-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        """
        Comprueba que el usuario que hace la petición es el mismo que el
        
        :param self: Instancia de la clase
        :param form: Formulario
        
        :return: Devuelve el formulario
        """
        questionnaire = get_object_or_404(
            Questionnaire, pk=self.kwargs['questionnaireid'])
        form.instance.questionnaire = questionnaire
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """
        Comprueba que el usuario que hace la petición es el mismo que el
        
        :param self: Instancia de la clase
        :param request: Petición HTTP
        :param args: Argumentos
        :param kwargs: Argumentos clave
        
        :return: Redirige a la lista de cuestionarios si el usuario no es el
        """
        questionnaire = get_object_or_404(
            Questionnaire, pk=self.kwargs['questionnaireid'])
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class AnswerCreate(LoginRequiredMixin, CreateView):
    """
    Vista de creación de una respuesta.
    
    Esta vista se encarga de crear una respuesta.
    
    Autor: Alejandro Monterrubio
    """
    model = Answer
    template_name = 'services/answer_create.html'
    fields = ['answer', 'correct']
    redirect_field_name = 'login'

    def get_success_url(self):
        """
        Devuelve la URL a la que se redirige al crear una respuesta.
        
        Este metodo se encarga de devolver la URL a la que se redirige al
        crear una respuesta.
        
        :param self: Instancia de la clase
        
        :return: URL a la que se redirige al crear una respuesta
        """
        return reverse_lazy('question-detail',
                            kwargs={'pk': self.object.question.id})

    def form_valid(self, form):
        """
        Comprueba que el usuario que hace la petición es el mismo que el
        
        :param self: Instancia de la clase
        :param form: Formulario
        
        :return: Devuelve el formulario
        """
        question = get_object_or_404(Question, pk=self.kwargs['questionid'])
        form.instance.question = question
        return super(AnswerCreate, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """
        Comprueba que el usuario que hace la petición es el mismo que el
        
        :param self: Instancia de la clase
        :param request: Petición HTTP
        :param args: Argumentos
        :param kwargs: Argumentos clave
        
        :return: Redirige a la lista de cuestionarios si el usuario no es el
        """
        question = get_object_or_404(Question, pk=self.kwargs['questionid'])
        questionnaire = question.questionnaire
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class AnswerRemove(LoginRequiredMixin, DeleteView):
    """
    Vista de eliminación de una respuesta.
    
    Esta vista se encarga de eliminar una respuesta.
    
    Autor: Alejandro Monterrubio
    """
    model = Answer
    template_name = 'services/answer_remove.html'
    redirect_field_name = 'login'

    def get_success_url(self):
        """
        Devuelve la URL a la que se redirige al eliminar una respuesta.
        
        Este metodo se encarga de devolver la URL a la que se redirige al
        eliminar una respuesta.
        
        :param self: Instancia de la clase
        
        :return: URL a la que se redirige al eliminar una respuesta
        """
        return reverse_lazy('question-detail',
                            kwargs={'pk': self.object.question.id})

    def dispatch(self, request, *args, **kwargs):
        """
        Comprueba que el usuario que hace la petición es el mismo que el
        
        :param self: Instancia de la clase
        :param request: Petición HTTP
        :param args: Argumentos
        :param kwargs: Argumentos clave
        
        :return: Redirige a la lista de cuestionarios si el usuario no es el
        """
        questionnaire = self.get_object().question.questionnaire
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class AnswerUpdate(LoginRequiredMixin, UpdateView):
    """
    Vista de actualización de una respuesta.
    
    Esta vista se encarga de actualizar una respuesta.
    
    Autor: Alejandro Monterrubio
    """
    model = Answer
    template_name = 'services/answer_update.html'
    fields = ['answer', 'correct']
    redirect_field_name = 'login'

    def get_success_url(self):
        """
        Devuelve la URL a la que se redirige al actualizar una respuesta.
        
        Este metodo se encarga de devolver la URL a la que se redirige al
        actualizar una respuesta.
        
        :param self: Instancia de la clase
        
        :return: URL a la que se redirige al actualizar una respuesta
        """
        return reverse_lazy('question-detail',
                            kwargs={'pk': self.object.question.id})

    def dispatch(self, request, *args, **kwargs):
        """
        Comprueba que el usuario que hace la petición es el mismo que el
        
        :param self: Instancia de la clase
        :param request: Petición HTTP
        :param args: Argumentos
        :param kwargs: Argumentos clave
        
        :return: Redirige a la lista de cuestionarios si el usuario no es el
        """
        questionnaire = self.get_object().question.questionnaire
        if request.user != questionnaire.user:
            return redirect('questionnaire-list')
        return super().dispatch(request, *args, **kwargs)


class GameCreate(LoginRequiredMixin, TemplateView):
    """
    Vista de creación de un juego.
    
    Esta vista se encarga de crear un juego.
    
    Autor: Alejandro Monterrubio
    """
    template_name = 'services/game_create.html'
    redirect_field_name = 'login'

    def get_context_data(self, **kwargs):
        """
        Devuelve el contexto de la vista.
        
        Este metodo se encarga de devolver el contexto de la vista.
        
        :param self: Instancia de la clase
        :param kwargs: Argumentos clave
        
        :return: Contexto de la vista
        """

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
    """
    Vista de actualización de participantes.
    
    Esta vista se encarga de actualizar los participantes de un juego.
    
    Autor: Alejandro Monterrubio
    """
    template_name = 'services/game_updateparticipant.html'
    redirect_field_name = 'login'

    def get_context_data(self, **kwargs):
        """
        Devuelve el contexto de la vista.
        
        Este metodo se encarga de devolver el contexto de la vista.
        
        :param self: Instancia de la clase
        :param kwargs: Argumentos clave
        
        :return: Contexto de la vista
        """
        context = super(UpdateParticipant, self).get_context_data(**kwargs)
        gameID = self.request.session.get('gameID')
        game = get_object_or_404(Game, publicId=gameID)
        participants = Participant.objects.filter(game=game)
        context['participants'] = participants
        context['is_owner'] = self.request.session.get('is_owner')
        return context


class CountDown(LoginRequiredMixin, TemplateView):
    """
    Vista de cuenta atrás.
    
    Esta vista se encarga de mostrar la cuenta atrás de un juego.
    
    Autor: Alejandro Monterrubio
    """
    redirect_field_name = 'login'

    def get_template_names(self):
        """
        Devuelve el nombre de la plantilla.
        
        Este metodo se encarga de devolver el nombre de la plantilla.
        
        :param self: Instancia de la clase
        
        :return: Nombre de la plantilla
        """
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
        """
        Devuelve el contexto de la vista.
        
        Este metodo se encarga de devolver el contexto de la vista.
        
        :param self: Instancia de la clase
        :param kwargs: Argumentos clave
        
        :return: Contexto de la vista
        """
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
