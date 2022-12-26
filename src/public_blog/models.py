from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    Model,
    OneToOneField,
    Sum,
)
from django.urls import reverse

from ckeditor.fields import RichTextField

from src.emailing.abstracts import AbstractEmail
from src.escritos.abstracts import AbstractPublishableContent
from src.general.abstracts import AbstractComment
from src.public_blog.managers import PublicBlogManager

User = get_user_model()


class WriterProfile(Model):
    user = OneToOneField(User, on_delete=SET_NULL, null=True, related_name="writer_profile")
    created_at = DateTimeField(auto_now_add=True)
    host_name = CharField(max_length=500, null=True, blank=True, unique=True)
    long_description = RichTextField(default="", config_name="writer", blank=True)
    facebook = CharField(max_length=500, null=True, blank=True)
    twitter = CharField(max_length=500, null=True, blank=True)
    instagram = CharField(max_length=500, null=True, blank=True)
    youtube = CharField(max_length=500, null=True, blank=True)
    linkedin = CharField(max_length=500, null=True, blank=True)
    tiktok = CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "User writer profile"
        db_table = "writer_profile"

    @property
    def all_self_blogs(self):
        return PublicBlog.objects.filter(author=self.user)

    @property
    def number_of_blogs(self):
        return self.all_self_blogs.count()

    @property
    def average_opening_rate(self):
        total = sum(item.opening_rate for item in self.all_self_blogs)
        return total if total else 0

    @property
    def total_visits(self):
        return self.all_self_blogs.aggregate(total_visits=Sum("total_views"))

    @property
    def total_interactions(self):
        return self.all_self_blogs.aggregate(total_interactions=Sum("total_votes"))

    @property
    def total_followers(self):
        return self.user.main_writer_followed.followers.all().count()


class FollowingHistorial(Model):
    user_following = ForeignKey(User, on_delete=SET_NULL, null=True, related_name="user_following")
    user_followed = ForeignKey(User, on_delete=SET_NULL, null=True, related_name="user_followed")
    started_following = BooleanField(default=False)
    stop_following = BooleanField(default=False)
    date = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Users following historial"
        db_table = "writer_followers_historial"


class NewsletterFollowers(Model):
    # TODO change related_name to followers
    user = OneToOneField(
        User,
        on_delete=SET_NULL,
        null=True,
        related_name="main_writer_followed",
    )
    followers = ManyToManyField(User, blank=True)

    class Meta:
        verbose_name = "Base de seguidores del blog"
        db_table = "writer_followers_newsletters"


class PublicBlog(AbstractPublishableContent):
    send_as_newsletter = BooleanField(default=False)
    content = RichTextField(config_name="writer")
    upvotes = ManyToManyField(User, blank=True, related_name="user_upvote_blog")
    downvotes = ManyToManyField(User, blank=True, related_name="user_downvote_blog")
    published_correctly = BooleanField(default=False)
    date_to_publish = DateTimeField(null=True, blank=True)
    objects = PublicBlogManager()

    class Meta:
        ordering = ["total_views"]
        verbose_name = "Public blog post"
        db_table = "blog_post"

    def get_absolute_url(self) -> str:
        return self.custom_url

    @property
    def custom_url(self) -> str:
        absolute_url = reverse("public_blog:blog_details", kwargs={"slug": self.slug})
        return f"{self.author.custom_url}{absolute_url}"

    @property
    def has_newsletter(self) -> bool:
        return self.public_blog_newsletter.exists()

    @property
    def number_comments(self) -> int:
        return self.comments_related.all().count()

    @property
    def opening_rate(self):
        result = 0
        if self.public_blog_newsletter.email_related.exists():
            total = self.public_blog_newsletter.email_related.all().count()
            opened = self.public_blog_newsletter.email_related.filter(opened=True).count()
            result = total / opened if opened != 0 else 0
        return result


class PublicBlogAsNewsletter(AbstractEmail):
    blog_related = OneToOneField(PublicBlog, on_delete=SET_NULL, null=True, related_name="public_blog_newsletter")


class PublicBlogComment(AbstractComment):
    content_related = ForeignKey(PublicBlog, on_delete=CASCADE, null=True, related_name="comments_related")

    class Meta:
        verbose_name = "Blog's comment"
        db_table = "blog_comments"


# class EmailPublicBlog(BaseTrackEmail):
#     email_related = ForeignKey(
#         PublicBlogAsNewsletter,
#         null=True,
#         blank=True,
#         on_delete=SET_NULL,
#         related_name="email_related",
#     )

#     class Meta:
#         verbose_name = "Email from public blog"
#         db_table = "emails_public_blog"
