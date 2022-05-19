from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = "api"
# Создаём Router и регистрируем ViewSet
router = DefaultRouter()
router.register(r"bbs", BbsViewSet)
router.register(r"outfits", OutfitsViewSet)
router.register(r"users", UsersViewSet)
# router.register(r'userOutfits', UsersViewSet)

urlpatterns = [
    url("", include(router.urls)),
    # path('bbs/<int:pk>/', BbDetailView.as_view()),
    path("outfit/<int:pk>/like/", PostLikeAPIToggle.as_view(), name="like-api-toggle"),
    path("outfits_page/", page_outfits, name="page_outfits"),
]

# urlpatterns += router.urls
