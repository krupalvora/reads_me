from django.urls import path

from reads_me.views import page, PostListView, create

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('about/', page.about, name='about'),
    path('create/', create, name='create'),
]
