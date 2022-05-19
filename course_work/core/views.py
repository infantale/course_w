from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from django.views.generic import (
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    CreateView,
)
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from api.models import Outfit
from .forms import ChangeUserInfoForm, RegisterUserForm, BbForm, OutfitForm
from .models import AdvUser, Bb, SubCategory

import datetime


def index(request):
    bbs = Bb.objects.filter(is_active=True)[:10]
    context = {"bbs": bbs}
    return render(request, "main/index.html", context)


def about(request):
    return render(request, "main/about.html")


def other_page(request, page):
    try:
        template = get_template("main/" + page + ".html")
    except TemplateDoesNotExist:
        raise Http404

    return HttpResponse(template.render(request=request))


# ВЫНЕС В РЕСТ
class BBDetailView(DetailView):
    """Вывод полной информации об объявлении"""

    context_object_name = "bb"
    model = Bb
    template_name = "main/detail.html"


class ByCategoryView(ListView):
    """Вывод объявлений по категориям"""

    model = Bb
    paginate_by = 2
    template_name = "main/by_rubric.html"

    def get_queryset(self):
        queryset = Bb.objects.filter(is_active=True, category=self.kwargs["pk"])
        return queryset


class ProfileView(LoginRequiredMixin, ListView):
    """Показать страницу профиля пользователя"""

    model = Bb
    template_name = "main/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bbs"] = Bb.objects.filter(author=self.request.user.pk)
        context["outfits"] = Outfit.objects.filter(author=self.request.user.pk)
        return context


# Не работает с form_class
class BBAddView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Создание объявления"""

    model = Bb
    template_name = "main/profile_bb_add.html"
    fields = ["category", "title", "content", "price", "contacts", "image", "is_active"]
    success_message = "Объявление успешно добавлено"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.created_at = datetime.datetime.now()
        return super().form_valid(form)


class BBEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Редактирование объявления"""

    model = Bb
    template_name = "main/profile_bb_change.html"
    form_class = BbForm
    success_message = "Объявление изменено"


class BBDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление объявления"""

    model = Bb
    success_url = reverse_lazy("core:profile")
    template_name = "main/profile_bb_delete.html"


# Не работает c form_class
class OutfitAddView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Создание образа"""

    model = Outfit
    template_name = "main/profile_outfit_add.html"
    fields = ["title", "price", "image"]
    success_url = reverse_lazy("core:profile")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class OutfitEditView(LoginRequiredMixin, UpdateView):
    """Редактирование образа"""

    model = Outfit
    template_name = "main/profile_outfit_change.html"
    form_class = OutfitForm
    success_message = "Образ изменен"


class OutfitDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление образа"""

    model = Outfit
    success_url = reverse_lazy("core:profile")
    template_name = "main/profile_outfit_delete.html"


class TSLoginView(LoginView):
    template_name = "main/login.html"


class TSLogoutView(LogoutView):
    template_name = "main/logout.html"


# LoginRequiredMixin допускает к странице только авторизованных пользователей
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = "main/change_user_info.html"
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy("core:profile")
    success_message = "Данные пользователя изменены"

    # Извлекаем ключ пользователя и сохраняем его в атрибуте user_id
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    # Извлекаем исправляемую запись
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = "main/register_user.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy("core:register_done")


class RegisterDoneView(TemplateView):
    template_name = "main/register_done.html"


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = "main/delete_user.html"
    success_url = reverse_lazy("core:index")

    # Сохранили ключ текущего пользователя
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, "Пользователь удалён")
        return super().post(request, *args, **kwargs)

    # Нашли удаляемого пользователя
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
