from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rest_framework import parsers, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView

from src.api.models import EndpointsCategory, Key, ReasonKeyRequested
from src.api.serializers import AuthKeySerializer
from src.seo.outils.visiteur_meta import SeoInformation
from src.seo.views import SEOListView


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
        response = {"Respuesta": "Autentifícate o crea un perfil para tener tu llave"}
        response_status = status.HTTP_204_NO_CONTENT
        if request.user.is_authenticated:
            if key := Key.objects.return_if_key(user=request.user):
                response = {"Respuesta": f"Tu llave: {key}"}
                response_status = status.HTTP_202_ACCEPTED
        return Response(response, status=response_status)


obtain_auth_key = ObtainAuthKey.as_view()


class APIDocumentation(SEOListView):
    model = EndpointsCategory
    template_name = "explorar/api_documentation.html"
    context_object_name = "endpoints_categories"
    meta_description = "La mejor y más completa API de información financiera y económica"
    meta_tags = "finanzas", "blog financiero", "blog el financiera", "invertir", "API"
    meta_title = "API documentación"
    meta_category = "API"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        key = "*****************"
        if self.request.user.is_authenticated:
            key = Key.objects.key_for_docs(self.request.user)
        context["show_api_key"] = key != "*****************"
        context["key"] = key
        return context


@login_required
def request_API_key(request):
    if request.method == "POST":
        if description := request.POST.get("description"):
            ReasonKeyRequested.objects.create(user=request.user, description=description)
            key = Key.objects.create(
                user=request.user, ip=SeoInformation.get_client_ip(request), limit=250
            )
            messages.success(request, f"Gracias, tu clave ya está disponible {key.key}")
        else:
            messages.error(request, "Oups, parece que hay un error con tu motivo")
    return redirect(request.META.get("HTTP_REFERER"))
