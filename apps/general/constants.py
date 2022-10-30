from typing import Dict


EXTRA_DATA_DICT_KEY_OLD_URLS = "previous_urls"

DEFAULT_EXTRA_DATA_DICT: Dict = {
    EXTRA_DATA_DICT_KEY_OLD_URLS: [],
}

BASE_ESCRITO_PUBLISHED = 1
BASE_ESCRITO_DRAFT = 2
BASE_ESCRITO_SCHEDULED = 3
BASE_ESCRITO_NEED_REVISION = 4

BASE_ESCRITO_STATUS = (
    (BASE_ESCRITO_PUBLISHED, "Publicado"),
    (BASE_ESCRITO_DRAFT, "Borrador"),
    (BASE_ESCRITO_SCHEDULED, "Programado"),
    (BASE_ESCRITO_NEED_REVISION, "Necesita revisión"),
)

ESCRITO_STATUS_MAP = {
    BASE_ESCRITO_PUBLISHED: "Publicado",
    BASE_ESCRITO_DRAFT: "Borrador",
    BASE_ESCRITO_SCHEDULED: "Programado",
    BASE_ESCRITO_NEED_REVISION: "Necesita revisión",
}


NOTIFY_TO_ALL = "all"
NOTIFY_TO_RELATED = "related"
NOTIFY_TO_SINGLE = "single"


NEW_BLOG_POST = "Nuevo blog"
NEW_COMMENT = "Nuevo comentario"
NEW_VOTE = "Nuevo voto"
NEW_FOLLOWER = "Nuevo seguidor"
NEW_QUESTION = "Nueva pregunta"
NEW_ANSWER = "Nueva respuesta"
ANSWER_ACCEPTED = "Respuesta aceptada"
PURCHASE_SUCCESSFUL = "Compra efectuada"


NOTIFICATIONS_TYPE = (
    (NEW_BLOG_POST, "Nuevo blog"),
    (NEW_COMMENT, "Nuevo comentario"),
    (NEW_VOTE, "Nuevo voto"),
    (NEW_FOLLOWER, "Nuevo seguidor"),
    (NEW_QUESTION, "Nueva pregunta"),
    (NEW_ANSWER, "Nueva respuesta"),
    (ANSWER_ACCEPTED, "Respuesta aceptada"),
    (PURCHASE_SUCCESSFUL, "Compra efectuada"),
)

EMAIL_FOR_PUBLIC_BLOG = "public_blog"
EMAIL_FOR_NOTIFICATION = "notification"
EMAIL_FOR_WEB = "web"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81"
        " Safari/537.36"
    ),
    "Accept-Encoding": "gzip, deflate",
}

REQUESTS_MAX_RETRIES = 10

PERIOD_1_QUARTER = 1
PERIOD_2_QUARTER = 2
PERIOD_3_QUARTER = 3
PERIOD_4_QUARTER = 4
PERIOD_FOR_YEAR = 5

PERIODS_QUARRTERS = (
    (PERIOD_1_QUARTER, "1 Quarter"),
    (PERIOD_2_QUARTER, "2 Quarter"),
    (PERIOD_3_QUARTER, "3 Quarter"),
    (PERIOD_4_QUARTER, "4 Quarter"),
)

PERIODS = (
    *PERIODS_QUARRTERS,
    (PERIOD_FOR_YEAR, "For Year"),
)
