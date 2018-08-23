from django.urls import path
from . import views


urlpatterns = [
    path('api/character/', views.CharacterList.as_view()),
    path('api/abilities/', views.AbilityList.as_view())
]
