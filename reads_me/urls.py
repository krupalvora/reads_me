from django.urls import path

from reads_me.views import page, PostListView, create, PostDetailView, PostCategoryView, PostTopicView, PostUpdateView, \
    PostCreateView, deactivate_post

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('about/', page.about, name='about'),
    path('create/', create, name='create'),
    path('article/<str:slug>', PostDetailView.as_view(), name='post-detail'),
    path('article/deactivate/<int:pk>', deactivate_post, name='post-deactivate'),
    path('article/create/', PostCreateView.as_view(), name='post-create'),
    path('article/update/<int:pk>', PostUpdateView.as_view(), name='post-update'),

    path('topic/<str:wikipedia_id>', PostTopicView.as_view(), name='topic-list'),
    path('category/<str:category>', PostCategoryView.as_view(), name='category-list'),
]
