from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('items', views.index, name='index'),
    # path('categories', views.index, name='index'),

    # path('refrigerators', views.index, name='index'),

]