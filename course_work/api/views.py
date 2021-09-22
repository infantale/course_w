from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework import authentication, permissions, generics
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from core.models import Bb, AdvUser
from .serializers import *


class BBSView(generics.ListAPIView):
    """Вывод 10 последних объявлений"""
    queryset = Bb.objects.filter(is_active=True)[:10]
    serializer_class = BbSerializer


class UserOutfitsView(generics.ListAPIView):
    """Вывод образов и id текущего пользователя"""
    queryset = Outfit.objects.all()
    serializer_class = OutfitSerializer


def page_outfits(request):
    return render(request, 'main/outfits.html')


class BbDetailView(RetrieveAPIView):
    queryset = Bb.objects.filter(is_active=True)
    serializer_class = BbDetailSerializer


class PostLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Outfit, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
            likesCount = obj.likes.count()
        data = {'updated': updated, 'liked': liked, 'counter': likesCount}
        return Response(data)
