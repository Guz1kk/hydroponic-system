from django.urls import path
from . import views


urlpatterns = [
    path('systems', views.SystemsView.as_view(), name='all system operations'),
    
    path('<int:systemID>', views.SingleSystemView.as_view(), name='single sytem CRUD')
]
