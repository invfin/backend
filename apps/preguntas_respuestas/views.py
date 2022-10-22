from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView

from apps.general.tasks import prepare_notification_task
from apps.general import constants
from apps.seo.views import SEODetailView, SEOListView
from apps.preguntas_respuestas.forms import CreateQuestionForm
from apps.preguntas_respuestas.models import Answer, Question


User = get_user_model()


class QuestionsView(SEOListView):
    model = Question
    template_name = "QA_inicio.html"
    context_object_name = "questions"
    ordering = ["-created_at"]
    meta_description = "Haz una pregunta o responde a la comunidad para conseguir premios increíbles"
    meta_tags = ["finanzas, blog financiero, blog el financiera, invertir"]
    meta_title = "Resuelve tus dudas o ayuda otros inversores y gana dinero"
    is_article = True
    open_graph_type = "article"


class QuestionDetailsView(SEODetailView):
    model = Question
    template_name = "QA_details.html"
    context_object_name = "object"
    slug_field = "slug"
    update_visits = True


class CreateQuestionView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateQuestionForm
    template_name = "forms/create_question.html"
    success_message = "Pregunta creada"

    def get_context_data(self, **kwargs):
        context = super(CreateQuestionView, self).get_context_data(**kwargs)
        context["meta_title"] = "Dashboard"
        return context

    def get_initial(self, *args, **kwargs):
        initial = super(CreateQuestionView, self).get_initial(**kwargs)
        initial["title"] = "¿Cuál es tu pregunta?"
        initial["content"] = "Explica tu duda con todo lujo de detalles"
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        tags = self.request.POST["tags"].split(",")
        selfanswer = self.request.POST["selfanswereditor"]
        question = form.save()
        question.add_tags(tags)
        if selfanswer != "":
            question.add_answer(selfanswer)
            question.is_answered = True
            question.has_accepted_answer = True

        prepare_notification_task.delay(question.dict_for_task, constants.NEW_QUESTION)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class UpdateQuestionView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Question
    template_name = "forms/update_question.html"
    context_object_name = "question"
    slug_field = "slug"
    fields = ["title", "content"]
    success_message = "Pregunta actualizada"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta_title"] = "Dashboard"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        valid = False
        if self.get_object().author == self.request.user:
            valid = True
        elif self.request.user.is_superuser:
            valid = True
        return valid

    def handle_no_permission(self):
        return redirect("preguntas_respuestas:list_questions")


@login_required
def create_answer_view(request, slug):
    if request.method == "POST":
        user = request.user
        if request.user.is_anonymous:
            user = User.objects.get_or_create_quick_user(request)

        question = Question.objects.get(slug=slug)
        answer = question.add_answer(user, request.POST["content"])
        prepare_notification_task.delay(answer.dict_for_task, constants.NEW_ANSWER)
        messages.success(request, "Gracias por tu respuesta")
        return redirect(question.get_absolute_url())


@login_required
def accept_answer(request, question_id, answer_id):
    question = Question.objects.get(id=question_id)
    if request.user == question.author and question.has_accepted_answer == False:
        answer = Answer.objects.get(id=answer_id)
        if question.is_answered == False:
            question.is_answered = True

        question.has_accepted_answer = True
        question.save(update_fields=["is_answered", "has_accepted_answer"])
        answer.is_accepted = True
        answer.save(update_fields=["is_accepted"])
        answer.author.update_reputation(2)
        messages.success(request, "Gracias por tu ayuda")
        prepare_notification_task.delay(answer.dict_for_task, constants.ANSWER_ACCEPTED)
    return redirect(question.get_absolute_url())
