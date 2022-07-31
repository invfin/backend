from model_bakery import baker

from apps.public_blog.models import (
EmailPublicBlog,
FollowingHistorial,
NewsletterFollowers,
PublicBlog,
PublicBlogAsNewsletter,
PublicBlogComment,
WritterProfile,
)
from django.contrib.auth import get_user_model

User = get_user_model()


writter_profile = baker.make(
    WritterProfile,
    user=baker.make(User, is_writter=True)
)

public_blog = baker.make(
    PublicBlog,
    author=writter_profile
)
follower_historial = baker.make(FollowingHistorial)
newsletter_followers = baker.make(NewsletterFollowers)

public_blog_as_newsletter = baker.make(
    PublicBlogAsNewsletter,
    blog_related=public_blog
)
public_blog_comment = baker.make(
    PublicBlogComment,
    content_related=public_blog
)
email_public_blog = baker.make(
    EmailPublicBlog,
    email_related=public_blog_as_newsletter
)