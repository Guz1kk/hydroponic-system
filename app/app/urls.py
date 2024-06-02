from django.urls import path
from . import views


urlpatterns = [
    path('systems', views.SystemsView.as_view(), name='all system operations')
]
