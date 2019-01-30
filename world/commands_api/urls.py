from django.urls import path
from . import views


urlpatterns = [
    path('api/commands/', views.CommandsListCreate.as_view())
]
