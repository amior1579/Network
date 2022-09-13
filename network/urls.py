
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all_posts", views.all_posts, name="all_posts"),
    path("my_account/<str:user>", views.my_account, name="my_account"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("add_post", views.add_post, name="add_post"),
    path("follower", views.follower, name="follower"),
    path("following_posts", views.following_posts, name="following_posts"),
    path("like", views.like, name="like"),
    path("like_post", views.like_post, name="like_post"),

    path("update_post/<int:id>", views.update_post, name="update_post"),


    # API Routes
    path("posts", views.posts, name="posts"),
    path("posts/<int:id>", views.posts_id, name="posts_id"),
    # path("api", views.api, name="api"),


]
