from django.urls import path

from reads_me.views import page, PostListView, create, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('about/', page.about, name='about'),
    path('create/', create, name='create'),
    path('article/<str:slug>', PostDetailView.as_view(), name='post-detail'),
    path('topic/<str:wikipedia_id>', PostDetailView.as_view(), name='topic-list'),
]
