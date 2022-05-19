from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .forms import SubCategoryForm
from .models import (
    AdvUser,
    SuperCategory,
    SubCategory,
    Bb,
    AddiionalImage,
    Notification,
)


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ("__str__", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    fields = (
        ("username", "email"),
        ("first_name", "last_name"),
        ("is_staff", "is_superuser"),
        "groups",
        "user_permissions",
        ("last_login", "date_joined"),
    )
    readonly_fields = ("last_login", "date_joined")


class SubCategoryInline(admin.TabularInline):
    model = SubCategory


class SuperCategoryAdmin(admin.ModelAdmin):
    exclude = ("super_category",)
    inlines = (SubCategoryInline,)


class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryForm


class AddiionalImageInline(admin.TabularInline):
    model = AddiionalImage


class BbResource(resources.ModelResource):
    class Meta:
        model = Bb
        exclude = ("history",)

    def dehydrate_author(self, bb):
        author_email = getattr(bb.author, "email", "unknown")
        return author_email


class BbAdmin(ImportExportModelAdmin):
    resource_class = BbResource
    list_display = ("category", "title", "content", "author", "created_at")
    fields = (
        ("category", "author"),
        "title",
        "content",
        "price",
        "contacts",
        "image",
        "is_active",
    )
    inlines = (AddiionalImageInline,)


class OutfitAdmin(admin.ModelAdmin):
    fields = ("author", "title", "price", "image")


class NotificationAdmin(admin.ModelAdmin):
    pass


admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(SuperCategory, SuperCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Bb, BbAdmin)
admin.site.register(Notification, NotificationAdmin)
