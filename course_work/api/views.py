from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import authentication, permissions, filters
from django.shortcuts import render, get_object_or_404

from core.models import Bb, AdvUser

from .models import Outfit
from .serializers import *
from .tasks import send_notification


def page_outfits(request):
    return render(request, "main/outfits.html")


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
        data = {"updated": updated, "liked": liked, "counter": likesCount}
        return Response(data)


class BbsViewSet(ModelViewSet):
    queryset = Bb.objects.filter(is_active=True)
    serializer_class = BbSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["content"]
    filterset_fields = ["title", "price", "created_at"]

    @action(methods=["GET"], detail=False)
    def for_sale(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(
            Q(title__icontains="прода") | Q(content__icontains="прода")
        )
        serializer = BbSerializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user != instance.author:
            send_notification.apply_async((self.request.user.pk, instance.pk))
        serializer = BbDetailSerializer(instance)
        return Response(serializer.data)


class OutfitsViewSet(ModelViewSet):
    queryset = Outfit.objects.all()
    serializer_class = OutfitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "price"]

    @action(methods=["GET"], detail=False)
    def my_outfits(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(author=self.request.user.pk)
        serializer = OutfitSerializer(qs, many=True)
        return Response(serializer.data)


class UsersViewSet(ModelViewSet):
    queryset = AdvUser.objects.all()

    def get_serializer_class(self):
        if self.action == "change_password":
            return ChangePasswordSerializer
        else:
            return AdvUserSerializer

    @action(methods=["PATCH"], detail=True)
    def change_password(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance, serializer.validated_data)

        return Response(serializer.data)
