from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='home'),
    path('archive', views.archive, name='archive'),
    path('articles/<int:article_id>', views.get_content, name='article'),
]