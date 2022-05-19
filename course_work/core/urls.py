from django.urls import path

from .views import *

urlpatterns = [
    path("accounts/register/done/", RegisterDoneView.as_view(), name="register_done"),
    path("accounts/register/", RegisterUserView.as_view(), name="register"),
    path("accounts/logout/", TSLogoutView.as_view(), name="logout"),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path("accounts/profile/add/", BBAddView.as_view(), name="profile_bb_add"),
    path("accounts/profile/delete/", DeleteUserView.as_view(), name="profile_delete"),
    path(
        "accounts/profile/change/", ChangeUserInfoView.as_view(), name="profile_change"
    ),
    path(
        "accounts/profile/change/<int:pk>/",
        BBEditView.as_view(),
        name="profile_bb_change",
    ),
    path(
        "accounts/profile/delete/<int:pk>/",
        BBDeleteView.as_view(),
        name="profile_bb_delete",
    ),
    path(
        "accounts/profile/<int:pk>/", BBDetailView.as_view(), name="profile_bb_detail"
    ),
    path(
        "accounts/outfit/change/<int:pk>/",
        OutfitEditView.as_view(),
        name="profile_outfit_change",
    ),
    path(
        "accounts/outfit/delete/<int:pk>/",
        OutfitDeleteView.as_view(),
        name="profile_outfit_delete",
    ),
    path("accounts/outfit/add/", OutfitAddView.as_view(), name="profile_outfit_add"),
    path("login/", TSLoginView.as_view(), name="login"),
    path("<int:category_pk>/<int:pk>/", BBDetailView.as_view(), name="detail"),
    path("<int:pk>/", ByCategoryView.as_view(), name="by_category"),
    path("<str:page>/", other_page, name="other"),
    path("about/", about, name="about_project"),
    path("", index, name="index"),
]

app_name = "core"
