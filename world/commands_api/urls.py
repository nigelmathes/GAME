from django.urls import path
from . import views


urlpatterns = [
    path('api/commands/', views.CommandsListCreate.as_view()),
    path('api/input_command/', views.MatchCommands.as_view())
]
