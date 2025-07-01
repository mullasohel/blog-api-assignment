from django.urls import path
from .views import PostListCreateView, AuthorListCreateView, PostRetrieveUpdateDeleteView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='posts'),
    path('posts/<int:pk>/', PostRetrieveUpdateDeleteView.as_view(), name='post-detail'),
    path('authors/', AuthorListCreateView.as_view(), name='authors'),
]
