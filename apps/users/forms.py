from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm

from django import forms
from django.conf import settings
from django.contrib.auth import forms as admin_forms, get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .models import Profile

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {"username": {"unique": _("This username has already been taken.")}}


class UserSignupForm(SignupForm):
    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        user.create_new_user(request)

        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


class UserForm(forms.ModelForm):
    username = forms.CharField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]

    def __init__(self, instance, *args, **kwargs) -> None:
        super().__init__(instance=instance, *args, **kwargs)


class UserProfileForm(forms.ModelForm):
    edad = forms.DateField(
        label="Cumpleaños",
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(attrs={"class": "datetimepicker1"}),
    )

    class Meta:
        model = Profile
        fields = ["edad", "ciudad", "pais", "foto_perfil", "bio"]
