NEW_BLOG_POST = 'Nuevo blog'
NEW_COMMENT = 'Nuevo comentario'
NEW_VOTE = 'Nuevo voto'
NEW_FOLLOWER = 'Nuevo seguidor'
NEW_QUESTION = 'Nueva pregunta'
NEW_ANSWER = 'Nueva respuesta'
ANSWER_ACCEPTED = 'Respuesta aceptada'
PURCHASE_SUCCESSFUL = 'Compra efectuada'
COMMENT_PURCHASED_PRODUCT = 'Comenta tu úlitma compra'

NOTIFICATIONS_TYPE = (
    (NEW_BLOG_POST, 'Nuevo blog'),
    (NEW_COMMENT, 'Nuevo comentario'),
    (NEW_VOTE, 'Nuevo voto'),
    (NEW_FOLLOWER, 'Nuevo seguidor'),
    (NEW_QUESTION, 'Nueva pregunta'),
    (NEW_ANSWER, 'Nueva respuesta'),
    (ANSWER_ACCEPTED, 'Respuesta aceptada'),
    (PURCHASE_SUCCESSFUL, 'Compra efectuada'),
    (COMMENT_PURCHASED_PRODUCT, '¿Qué opinas de tu última compra?')
)

EMAIL_FOR_PUBLIC_BLOG = "public_blog"
EMAIL_FOR_NOTIFICATION = "notification"
EMAIL_FOR_WEB = "web"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate'
}

REQUESTS_MAX_RETRIES = 10
