from django.urls import path

from .views import (
    CreatePublicBlogPostView,
    PublicBlogDetailsView,
    PublicBlogsListView,
    UpdateBlogNewsletterView,
    UpdatePublicBlogPostView,
    writerOwnBlogsListView,
    create_newsletter_for_blog,
    following_management_view,
    user_become_writer_view,
)

app_name = "public_blog"

subdomains_urls = [
    path("p/<slug>/", PublicBlogDetailsView.as_view(), name="blog_details"),
    path("management/escritos/<slug>/", writerOwnBlogsListView.as_view(), name="manage_blogs"),
    path("create-newsletter-blog/<slug>/", create_newsletter_for_blog, name="create_newsletter_blog"),
    path("update-newsletter-blog/<pk>/", UpdateBlogNewsletterView.as_view(), name="update_newsletter_blog"),
    path("create-blog/", CreatePublicBlogPostView.as_view(), name="create_blog"),
    path("update-blog/<pk>/", UpdatePublicBlogPostView.as_view(), name="update_blog"),
]

urlpatterns = [
    path("blog-financiero/", PublicBlogsListView.as_view(), name="blog_list"),
    path("become-writer/", user_become_writer_view, name="user_become_writer"),
    path("start-following-writer/", following_management_view, name="following_management_view"),
] + subdomains_urls
