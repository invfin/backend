from typing import Tuple, Type, List, Union

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import QuerySet

from rest_framework import parsers, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, ParseError, APIException, NotFound

from apps.seo.outils.visiteur_meta import SeoInformation
from apps.seo.views import SEOListView

from .models import EndpointsCategory, Key, ReasonKeyRequested
from .serializers import AuthKeySerializer


class ObtainAuthKey(APIView):
    throttle_classes = []
    permission_classes = []
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser]
    serializer_class = AuthKeySerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        key, created = Key.objects.get_or_create(user=user)
        return Response({"token": key.key})

    def get(self, request, *args, **kwargs):
        response = {"Respuesta": f"Autentifícate o crea un perfil para tener tu llave"}
        response_status = status.HTTP_204_NO_CONTENT
        if request.user.is_authenticated:
            key = Key.objects.return_if_key(user=request.user)
            if key:
                response = {"Respuesta": f"Tu llave: {key}"}
                response_status = status.HTTP_202_ACCEPTED
        return Response(response, status=response_status)


obtain_auth_key = ObtainAuthKey.as_view()


class BaseAPIView(APIView):
    """
    TODO
    Maybe change the url_parameters to a dict
    Example:
        {"ticker", "company__ticker"}
        key being the url parameter to look for and the value, the filter to apply to the queryset

    A class to sharea across API views.

    Attributes
    ----------
    model: Type
        the model query

    queryset: Tuple[Type, bool]
        a custom queryset with a bool to know if it's for many or not

    serializer_class: Type
        the serializer

    url_parameters: List[str]
        a list with the availables parameters for the url

    fk_lookup_model: str
        a string that reference a models foreign key (Ex: company__ticker)

    limited: bool
        a bool to define if the queryset needs to be sliced according to the user subs

    Methods
    -------
    save_request()
        saves the request

    get_object()
        get the objects or the queryset and if it's for many or not

    final_responses()
        return the final response

    find_query_value()
        check the url for the parameters

    check_limitation()
        checks if the queryset has to be sliced

    generate_queryset()
        generates the queryset to render

    get()
        overrides the base get request
    """

    model: Tuple[Type, bool] = ()
    queryset: Tuple[Type, bool] = ()
    serializer_class: Type = None
    url_parameters: List[str] = []
    fk_lookup_model: str = ""
    limited: bool = False
    model_to_track: Union[Type, str] = None
    is_excel: bool = False

    def get_model_to_track(self) -> Union[Type, None]:
        """
        TODO maybe instead of saving the model saved we should also saved the endpoint requested

        Raises:
            NotImplementedError: model_to_track is set to None by default, if we don't want to save the request
            we should pass "ignore" otherwise it will rise and error

        Returns:
            Union[Type, None]: It could return an actual model to be looked up and saved or None if we want to ignore it
        """
        if self.model_to_track:
            if type(self.model_to_track) == str:
                queryed_model = self.model_to_track
            else:
                queryed_model = self.model_to_track.__name__
            if queryed_model == "ignore":
                return None
            object_name = f"{queryed_model}RequestAPI"
            return apps.get_model("api", object_name, require_ready=True)
        raise NotImplementedError('You need to set a "model_to_track"')

    def get_object_searched(self, queryset: Union[Type, QuerySet]) -> Type:
        search = queryset
        if type(queryset).__name__ == "BaseStatementQuerySet" or type(queryset) == list:
            search = None
            if "ticker" in self.url_parameters and queryset[0]._meta.app_label == "empresas":
                search = queryset[0].company
            else:
                raise ParseError("Ha habido un problema con tu búsqueda, asegúrate de haber introducido un valor")
        return search

    def save_request(self, queryset: Union[Type, QuerySet], path: str, ip: str) -> None:
        request_model = self.get_model_to_track()
        if request_model:
            search = self.get_object_searched(queryset)
            obj_data = dict(
                ip=ip,
                key=self.request.auth,
                user=self.request.user,
                path=path,
                search=search,
            )
            if hasattr(request_model, "is_excel"):
                obj_data.update({"is_excel": self.is_excel})
            request_model.objects.create(**obj_data)

    def final_responses(self, serializer, queryset: QuerySet, path: str, ip: str) -> Response:
        if status.is_success:
            self.save_request(queryset, path, ip)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return APIException("Lo siento ha habido un problema, vuelve a intentarlo en un momento")

    def find_query_value(self, query_dict: dict) -> Union[Tuple[str, str], Tuple[None, None]]:
        for url_query_param, url_query_value in query_dict.items():
            if url_query_param in self.url_parameters and url_query_value:
                return url_query_param, url_query_value
        return None, None

    def check_limitation(self, queryset: QuerySet) -> QuerySet:
        if self.request.auth.has_subscription is False:
            queryset = queryset[:10]
        return queryset

    def get_object(self) -> Tuple[Union[Type, QuerySet], bool]:
        """
        Parameters
        ----------
        self: regular self
            Regular self

        Returns
        -------
        res: tuple
            returns a tuple with the model to query or a queryset
        """
        if self.queryset:
            return self.queryset
        elif self.model:
            return self.model
        elif not self.model and not self.queryset:
            return self.serializer_class.Meta.model, False

    def generate_queryset(
        self, model_or_callable: Union[Type, QuerySet], many: bool, url_query_param: str, url_query_value: str
    ):
        """
        Parameters
        ----------
        model_or_queryset: Union[Type, QuerySet]
            A model class or a model's manager

        Returns
        -------
        obj_or_queryset: Union[Type, QuerySet]
            Return a specific object or a queryset according to the users lookup

        TODO
        --------
            Improve lookup
        """
        lookup_data = dict()
        if self.url_parameters or self.fk_lookup_model:
            if not url_query_value:
                raise ParseError("No has introducido ninguna búsqueda")
            if self.fk_lookup_model:
                lookup_data = {f"{self.fk_lookup_model}": url_query_value}
            elif self.url_parameters:
                lookup_data = {url_query_param: url_query_value}

        if self.queryset:
            obj_or_queryset = model_or_callable(**lookup_data)
            if not obj_or_queryset:
                raise NotFound("Tu búsqueda no ha devuelto ningún resultado")
        else:
            try:
                obj_or_queryset = model_or_callable.objects.get(**lookup_data)
            except model_or_callable.DoesNotExist:
                raise NotFound("Tu búsqueda no ha devuelto ningún resultado")

        return obj_or_queryset

    def get(self, request) -> Response:
        model_or_callable, many = self.get_object()
        query_dict = request.query_params.dict()
        url_query_param, url_query_value = self.find_query_value(query_dict)
        if url_query_param == "ticker":
            url_query_value = url_query_value.upper()
        queryset = self.generate_queryset(model_or_callable, many, url_query_param, url_query_value)
        if self.limited:
            queryset = self.check_limitation(queryset)
        serializer = self.serializer_class(queryset, many=many)
        return self.final_responses(
            serializer, queryset, request.build_absolute_uri(), SeoInformation.get_client_ip(request)
        )


class APIDocumentation(SEOListView):
    model = EndpointsCategory
    template_name = "explorar/api_documentation.html"
    context_object_name = "endpoints_categories"
    meta_description = "La mejor y más completa API de información financiera y económica"
    meta_tags = ["finanzas", "blog financiero", "blog el financiera", "invertir", "API"]
    meta_title = "API documentación"
    meta_category = "API"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        key = "*****************"
        if self.request.user.is_authenticated:
            key = Key.objects.key_for_docs(self.request.user)
        context["show_api_key"] = True if key != "*****************" else False
        context["key"] = key
        return context


@login_required
def request_API_key(request):
    if request.method == "POST":
        description = request.POST.get("description")
        if description:
            ReasonKeyRequested.objects.create(user=request.user, description=description)
            key = Key.objects.create(user=request.user, ip=SeoInformation.get_client_ip(request), limit=250)
            messages.success(request, f"Gracias, tu clave ya está disponible {key.key}")
        else:
            messages.error(request, f"Oups, parece que hay un error con tu motivo")
    return redirect(request.META.get("HTTP_REFERER"))
