from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from character import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'character', views.CharacterViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'abilities', views.AbilityViewSet)
router.register(r'effects', views.AbilityEffectViewSet)
router.register(r'classes', views.PlayerClassesViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls))
]
