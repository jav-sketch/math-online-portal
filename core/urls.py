from django.urls import path
# from .views import HomeView
from . import views


appname = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    # path('', HomeView.as_view(), name="index"),
]
