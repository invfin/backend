BASE_ESCRITO_PUBLISHED = 1
BASE_ESCRITO_DRAFT = 2
BASE_ESCRITO_SCHEDULED = 3
BASE_ESCRITO_NEED_REVISION = 4

BASE_ESCRITO_STATUS = (
    (BASE_ESCRITO_PUBLISHED, 'Publicado'),
    (BASE_ESCRITO_DRAFT, 'Borrador'),
    (BASE_ESCRITO_SCHEDULED, 'Programado'),
    (BASE_ESCRITO_NEED_REVISION, 'Necesita revisión')
)

NOTIFY_TO_ALL = "all"
NOTIFY_TO_RELATED = "related"
NOTIFY_TO_SINGLE = "single"


NEW_BLOG_POST = 'Nuevo blog'
NEW_COMMENT = 'Nuevo comentario'
NEW_VOTE = 'Nuevo voto'
NEW_FOLLOWER = 'Nuevo seguidor'
NEW_QUESTION = 'Nueva pregunta'
NEW_ANSWER = 'Nueva respuesta'
ANSWER_ACCEPTED = 'Respuesta aceptada'
PURCHASE_SUCCESSFUL = 'Compra efectuada'


NOTIFICATIONS_TYPE = (
    (NEW_BLOG_POST, 'Nuevo blog'),
    (NEW_COMMENT, 'Nuevo comentario'),
    (NEW_VOTE, 'Nuevo voto'),
    (NEW_FOLLOWER, 'Nuevo seguidor'),
    (NEW_QUESTION, 'Nueva pregunta'),
    (NEW_ANSWER, 'Nueva respuesta'),
    (ANSWER_ACCEPTED, 'Respuesta aceptada'),
    (PURCHASE_SUCCESSFUL, 'Compra efectuada'),
)

EMAIL_FOR_PUBLIC_BLOG = "public_blog"
EMAIL_FOR_NOTIFICATION = "notification"
EMAIL_FOR_WEB = "web"
