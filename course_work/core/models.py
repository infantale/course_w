from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from simple_history.models import HistoricalRecords

from .utilities import get_timestamp_path


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(
        default=True, db_index=True, verbose_name="Прошёл активацию"
    )

    # При удалении пользователя удаляются оставленные им объявления
    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


class Category(models.Model):
    name = models.CharField(
        max_length=20, db_index=True, unique=True, verbose_name="Название"
    )
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name="Порядок")
    super_category = models.ForeignKey(
        "SuperCategory",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Надкатегория",
    )


# Указываем условия фильтрации
class SuperCategoryManager(models.Manager):
    # Выбирает только записи с пустым полем super_category, т.е. надкатегории
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=True)


class SuperCategory(Category):
    objects = SuperCategoryManager()

    def __str__(self):
        return self.name

    # Прокси модель используется для изменения поведения модели, например, чтобы
    # включить дополнительные методы или различные мета параметры.
    class Meta:
        proxy = True
        ordering = ("order", "name")
        verbose_name = "Надкатегория"
        verbose_name_plural = "Надкатегории"


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=False)


class SubCategory(Category):
    objects = SubCategoryManager()

    def __str__(self):
        return "%s - %s" % (self.super_category.name, self.name)

    class Meta:
        proxy = True
        ordering = ("super_category__order", "super_category__name", "order", "name")
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class Bb(models.Model):
    category = models.ForeignKey(
        SubCategory, on_delete=models.PROTECT, verbose_name="Категория"
    )
    title = models.CharField(max_length=40, verbose_name="Товар")
    content = models.TextField(verbose_name="Описание")
    price = models.FloatField(default=0, verbose_name="Цена")
    contacts = models.TextField(verbose_name="Контакты")
    image = models.ImageField(
        blank=True, upload_to=get_timestamp_path, verbose_name="Изображение"
    )
    author = models.ForeignKey(
        AdvUser,
        on_delete=models.CASCADE,
        verbose_name="Автор объявления",
        related_name="author",
    )
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name="Выводить в списке?"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Опубликовано"
    )

    history = HistoricalRecords()
    views = models.IntegerField(default=0, verbose_name="Views amount")

    # Перед удалением текущей записи мы перебираем и вызовом метода delete()
    # удаляем все связанные дополнительные иллюстрации
    # def delete(self, *args, **kwargs):
    #     for ai in self.additionalimage_set.all():
    #         ai.delete()
    #     super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "core:detail", kwargs={"pk": self.pk, "category_pk": self.category.pk}
        )

    class Meta:
        verbose_name_plural = "Объявления"
        verbose_name = "Объявление"
        ordering = ["-created_at"]


class AddiionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name="Объявление")
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name="Изображение")

    class Meta:
        verbose_name_plural = "Дополнительные иллюстрации"
        verbose_name = "Дополнительная иллюстрация"


class Notification(models.Model):
    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    master = models.ForeignKey(
        AdvUser,
        on_delete=models.CASCADE,
        verbose_name="Notification Target",
        related_name="master",
    )
    viewed_by = models.ForeignKey(
        AdvUser,
        on_delete=models.CASCADE,
        verbose_name="Viewed by",
        null=True,
        blank=True,
    )
    bb = models.ForeignKey(
        Bb, on_delete=models.CASCADE, verbose_name="Просмотренное объявяление"
    )
