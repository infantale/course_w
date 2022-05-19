from django.contrib import admin

from .models import Outfit


class OutfitAdmin(admin.ModelAdmin):
    readonly_fields = ("likes",)


class UserOutfitRelationAdmin(admin.ModelAdmin):
    pass


# Register your models here.

admin.site.register(Outfit, OutfitAdmin)
# admin.site.register(UserOutfitRelation, UserOutfitRelationAdmin)
