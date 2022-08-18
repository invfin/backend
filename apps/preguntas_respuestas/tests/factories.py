from model_bakery import baker

from apps.preguntas_respuestas.models import (
Answer,
AnswerComment,
QuesitonComment,
Question,
)

from apps.users.tests.factories import regular_user


answer = baker.make(Answer)
answer_comment = baker.make(
    AnswerComment,
    author=regular_user,
    content_related=answer
)
question = baker.make(Question)
question_comment = baker.make(
    QuesitonComment,
    author=regular_user,
    content_related=question
)
