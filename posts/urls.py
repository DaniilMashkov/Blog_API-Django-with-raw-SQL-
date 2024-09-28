from django.urls import path

from posts.apps import PostsConfig
from posts.views import PostDetailView, PostListView

app_name = PostsConfig.name

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
