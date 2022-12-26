from itertools import chain

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from src.public_blog.forms import WriterProfileForm
from src.seo.views import SEOTemplateView, SEODetailView, FormView

from .forms import UserForm, UserProfileForm
from .models import Profile

User = get_user_model()


class UserDetailView(LoginRequiredMixin, SEOTemplateView):
    template_name = "private/inicio.html"

    def get_meta_title(self, instance: object = None):
        return f"Bienvenido {self.request.user.username}"


class UserPublicProfileDetailView(SEODetailView):
    template_name = "public/profile.html"
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "current_profile"

    def get_meta_title(self, instance: object = None):
        return instance.username

    def get_meta_description(self, instance: object = None):
        return instance.user_profile.bio


def invitation_view(request, invitation_code):
    perfil = Profile.objects.get(ref_code=invitation_code)
    request.session["recommender"] = perfil.id
    return redirect("account_signup")


class UpdateProfileView(LoginRequiredMixin, SEOTemplateView):
    meta_title = "Tu perfil"
    template_name = "private/settings.html"

    def get_writer(self):
        if self.request.user.is_writer:
            return self.request.user.writer_profile
        return None

    def update_picture(self, new_profile):
        old_picture = self.request.user.user_profile.foto_perfil
        new_picture = new_profile.foto_perfil
        if new_picture != old_picture:
            new_profile.transform_photo(new_picture)
        return None

    def validate_forms(self, profile_form, form, writer_form):
        validation = profile_form.is_valid() and form.is_valid()
        if writer_form:
            validation = validation and writer_form.is_valid()
        return validation

    def get_writer_form(self, data=None):
        writer = self.get_writer()
        if writer:
            return WriterProfileForm(data=data, instance=writer)
        return None

    def get_context_data(self, **kwargs):
        kwargs.update(
            {
                "profile_form": UserProfileForm(instance=self.request.user.user_profile),
                "form": UserForm(instance=self.request.user),
                "writer_form": self.get_writer_form(),
            }
        )
        return super().get_context_data(**kwargs)

    def save_forms(self, profile_form, form, writer_form):
        profile_form.save()
        form.save()
        if writer_form:
            writer_form.save()

    def forms_are_valid(self, profile_form, form, writer_form):
        new_profile = profile_form.save(commit=False)
        self.update_picture(new_profile)
        self.save_forms(profile_form, form, writer_form)
        messages.success(self.request, "Perfil actualizado")
        return redirect("users:update")

    def forms_are_invalid(self, profile_form, form, writer_form):
        return self.render_to_response(
            self.get_context_data(
                profile_form=profile_form,
                form=form,
                writer_form=writer_form,
            ),
        )

    def post(self, request, *args, **kwargs):
        profile_form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user.user_profile)
        form = UserForm(data=request.POST, instance=request.user)
        writer_form = self.get_writer_form(request.POST)
        if self.validate_forms(profile_form, form, writer_form):
            return self.forms_are_valid(profile_form, form, writer_form)
        return self.forms_are_invalid(profile_form, form, writer_form)


class UserHistorialView(LoginRequiredMixin, SEOTemplateView):
    template_name = "private/historial.html"
    meta_description = "Tu historial en la plataforma"

    def get_meta_title(self, instance: object = None):
        slug = self.kwargs["slug"]
        return f"Historial de {slug}"

    def get_object(self, slug):
        user = self.request.user
        if slug == "Aportes":
            content = user.corrector.all()
            url = "escritos:glosario"
        elif slug == "Comentarios":
            questions_coms = user.quesitoncomment_set.all()
            answers_coms = user.answercomment_set.all()
            content = list(chain(answers_coms, questions_coms))
            url = "preguntas_respuestas:list_questions"
        else:
            content = user.usercompanyobservation_set.all()
            url = "screener:screener_inicio"
        return {"content": content, "slug": slug, "url": reverse(url)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]
        context.update(self.get_object(slug))
        return context
