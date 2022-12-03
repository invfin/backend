PLATFORM_WEB = "web"

ALL = 0
QUESTION = 1
NEWS = 2
TERM = 3
PUBLIC_BLOG = 4
COMPANY = 5
WEB = 6

FOR_CONTENT = (
    (ALL, "All"),
    (QUESTION, "Question"),
    (NEWS, "News"),
    (TERM, "Term"),
    (PUBLIC_BLOG, "PublicBlog"),
    (COMPANY, "Company"),
    (WEB, "Web"),
)

QUESTION_FOR_CONTENT = "question"
NEWS_FOR_CONTENT = "news"
TERM_FOR_CONTENT = "term"
PUBLIC_BLOG_FOR_CONTENT = "public_blog"
COMPANY_FOR_CONTENT = "company"

MODELS_FOR_CONTENT = (
    (QUESTION_FOR_CONTENT, "Question"),
    (NEWS_FOR_CONTENT, "News"),
    (TERM_FOR_CONTENT, "Term"),
    (PUBLIC_BLOG_FOR_CONTENT, "Public Blog"),
    (COMPANY_FOR_CONTENT, "Company"),
)


POST_TYPE_VIDEO = 1
POST_TYPE_IMAGE = 2
POST_TYPE_TEXT = 3
POST_TYPE_REPOST = 4
POST_TYPE_TEXT_VIDEO = 5
POST_TYPE_TEXT_IMAGE = 6
POST_TYPE_SHORTS = 7
POST_TYPE_THREAD = 8

POST_TYPE = (
    (POST_TYPE_VIDEO, "Video"),
    (POST_TYPE_IMAGE, "Image"),
    (POST_TYPE_TEXT, "Text"),
    (POST_TYPE_REPOST, "Repost"),
    (POST_TYPE_TEXT_VIDEO, "Text and video"),
    (POST_TYPE_TEXT_IMAGE, "Text and image"),
    (POST_TYPE_SHORTS, "Shorts"),
    (POST_TYPE_THREAD, "Thread"),
)
