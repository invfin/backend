from typing import Type

from django.utils.html import format_html, strip_tags

from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.socialmedias import constants as socialmedias_constants
from apps.socialmedias.models import BlogSharedHistorial
from apps.socialmedias.outils.content_creation import ContentCreation


class PublicBlogContentCreation(ContentCreation):
    model_class = PublicBlog
    shared_model_historial = BlogSharedHistorial
    for_content = [socialmedias_constants.PUBLIC_BLOG]

    def create_content(self):
        return strip_tags(format_html(self.object.resume))


class TermContentCreation(ContentCreation):
    model_class = Term
    for_content = [socialmedias_constants.TERM]

    def get_object(self) -> Type:
        return self.model_class._default_manager.term_ready_newsletter()

    def get_object_content(self, **kwargs):
        """Creates a basic content for a term's newsletter or post.
        The content will be used for both newsletters and socialmedia posts

        Returns
        -------
            _type_
                The content created
        """
        link = self.create_url()
        line_break = "\n" if self.platform == socialmedias_constants.PLATFORM_WEB else "<br>"
        description = (
            f"{self.object.resume} {line_break}Si quieres conocer más a fondo puedes leer la definición entera {link}."
            f" {line_break}Estos son los puntos claves que encontrarás:"
        )
        for index, term_content in enumerate(self.object.term_content_parts.all()):
            description = f"{description}{index}.-{term_content.title}{line_break}"
        return description


class QuestionContentCreation(ContentCreation):
    model_class = Question
    for_content = [socialmedias_constants.QUESTION]
    """
    Preparar algo del estilo:
        title: la pregunta
        description: pregunta completa si hay + "las mejores respuestas por el momento son:" self.answers_set si hay
            "han aportado las siguientes"
    """

    def get_object_title(self) -> str:
        return strip_tags(format_html(self.object.title))

    def get_object_content(self, **kwargs):
        return strip_tags(format_html(self.object.content))
