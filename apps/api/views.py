from typing import Tuple, Type, List

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import QuerySet, Model

from rest_framework import parsers, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, ParseError, APIException

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
    A class to sharea across APIViews.

    Attributes
    ----------
    model: Type
        the model query
    custom_queryset: Type
        a custom queryset to query
    custom_query: Tuple[Type, bool]
        a custom queryset with a bool to know if it's for many or not
    serializer_class: Type
        the serializer
    query_name: List[str]
        a list with the availables params for the url
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

    model: Type = None
    custom_queryset: Type = None
    custom_query: Tuple[Type, bool] = ()
    serializer_class: Type = None
    query_name: List[str] = []
    fk_lookup_model: str = ""
    limited: bool = False

    def save_request(self, key, queryset, path: str, ip: str):
        queryed_model = self.serializer_class.Meta.model.__name__
        if "Term" not in queryed_model and queryed_model != "PublicBlog":
            queryed_model = "Company"
        object_name = f"{queryed_model}RequestAPI"
        request_model = apps.get_model("api", object_name, require_ready=True)
        search = queryset
        if type(queryset).__name__ == "QuerySet":
            search = None
            if "ticker" in self.query_name and queryset and queryset[0]._meta.app_label == "empresas":
                search = queryset[0].company
            else:
                raise ParseError("Ha habido un problema con tu búsqueda, asegúrate de haber introducido un valor")
        request_data = {
            "ip": ip,
            "key": key,
            "user": key.user,
            "path": path,
            "search": search,
        }
        if queryed_model == "Company":
            is_excel = False
            if "company-information/excel-api" in path:
                is_excel = True
            request_data["is_excel"] = is_excel
        obj = request_model.objects.create(**request_data)
        return obj

    def get_object(self) -> Tuple:
        if self.custom_query:
            return self.custom_query[0], self.custom_query[1]
        if self.model:
            return self.model, False
        if self.custom_queryset:
            return self.custom_queryset, True
        try:
            if self.queryset:
                return self.queryset, True
        except:
            pass
        if not self.model and not self.custom_queryset and not self.custom_query:
            return self.serializer_class.Meta.model, False

    def final_responses(self, serializer, api_key, queryset, path, ip) -> Response:
        if status.is_success:
            self.save_request(api_key, queryset, path, ip)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return APIException("Lo siento ha habido un problema")

    def find_query_value(self, query_dict: dict) -> Tuple:
        for query_param, query_value in query_dict.items():
            if query_param in self.query_name and query_value:
                return query_param, query_value
        return None, None

    def check_limitation(self, key, queryset):
        if key.has_subscription is False:
            queryset = queryset[:10]
        return queryset

    def generate_queryset(self, model: Type, many: bool, query_param: str, query_value: str):
        """
        Parameters
        ----------
        foo: sequence of ints
        The list of integers to sum up.

        Returns
        -------
        res: int
        sum of elements of foo

        See also
        --------
        cumsum:  compute cumulative sum of elemenents
        """
        if many is False:
            if query_value:
                if self.custom_query:
                    queryset = model.get(**{query_param: query_value})
                else:
                    try:
                        queryset = model.objects.get(**{query_param: query_value})
                    except model.DoesNotExist:
                        raise ParseError("Tu búsqueda no ha devuelto ningún resultado")
            else:
                raise ParseError("No has introducido ninguna búsqueda")
        else:
            if self.fk_lookup_model:
                queryset = model.objects.filter(**{f"{self.fk_lookup_model}": query_value})
            else:
                if self.custom_queryset:
                    queryset = model
                else:
                    queryset = model.objects.all()
        return queryset

    def get(self, request):
        model, many = self.get_object()
        query_dict = request.GET.dict()
        api_key = query_dict.pop("api_key", None)
        if not api_key:
            raise AuthenticationFailed(
                "Tu clave es incorrecta, asegúrate que está bien escrita depués de api_key=<clave> o pide tu clave"
                " desde tu perfil"
            )
        key = Key.objects.get(key=api_key)
        query_param, query_value = self.find_query_value(query_dict)
        if query_param == "ticker":
            query_value = query_value.upper()
        queryset = self.generate_queryset(model, many, query_param, query_value)
        if self.limited:
            queryset = self.check_limitation(key, queryset)
        serializer = self.serializer_class(queryset, many=many)
        return self.final_responses(
            serializer, key, queryset, request.build_absolute_uri(), SeoInformation.get_client_ip(request)
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
