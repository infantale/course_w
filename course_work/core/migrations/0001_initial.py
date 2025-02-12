# Generated by Django 3.2 on 2022-05-11 16:53

import core.utilities
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdvUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "is_activated",
                    models.BooleanField(
                        db_index=True, default=True, verbose_name="Прошёл активацию"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        max_length=20,
                        unique=True,
                        verbose_name="Название",
                    ),
                ),
                (
                    "order",
                    models.SmallIntegerField(
                        db_index=True, default=0, verbose_name="Порядок"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Bb",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=40, verbose_name="Товар")),
                ("content", models.TextField(verbose_name="Описание")),
                ("price", models.FloatField(default=0, verbose_name="Цена")),
                ("contacts", models.TextField(verbose_name="Контакты")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        upload_to=core.utilities.get_timestamp_path,
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        db_index=True, default=True, verbose_name="Выводить в списке?"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Опубликовано"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор объявления",
                    ),
                ),
            ],
            options={
                "verbose_name": "Объявление",
                "verbose_name_plural": "Объявления",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="AddiionalImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=core.utilities.get_timestamp_path,
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "bb",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.bb",
                        verbose_name="Объявление",
                    ),
                ),
            ],
            options={
                "verbose_name": "Дополнительная иллюстрация",
                "verbose_name_plural": "Дополнительные иллюстрации",
            },
        ),
        migrations.CreateModel(
            name="SubCategory",
            fields=[],
            options={
                "verbose_name": "Подкатегория",
                "verbose_name_plural": "Подкатегории",
                "ordering": (
                    "super_category__order",
                    "super_category__name",
                    "order",
                    "name",
                ),
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.category",),
        ),
        migrations.CreateModel(
            name="SuperCategory",
            fields=[],
            options={
                "verbose_name": "Надкатегория",
                "verbose_name_plural": "Надкатегории",
                "ordering": ("order", "name"),
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.category",),
        ),
        migrations.AddField(
            model_name="category",
            name="super_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="core.supercategory",
                verbose_name="Надкатегория",
            ),
        ),
        migrations.AddField(
            model_name="bb",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="core.subcategory",
                verbose_name="Категория",
            ),
        ),
    ]
