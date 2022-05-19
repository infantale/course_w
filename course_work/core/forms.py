from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import AdvUser, SuperCategory, SubCategory, Bb, AddiionalImage
from api.models import Outfit


class ChangeUserInfoForm(forms.ModelForm):
    class Meta:
        model = AdvUser
        fields = ("username", "first_name", "last_name")


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data["password1"]
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 and password2 and password1 != password2:
            errors = {
                "password2": ValidationError(
                    "Введённые пароли не совпадают", code="password_mismatch"
                )
            }
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        user.is_activated = True

        if commit:
            user.save()

        return user

    class Meta:
        model = AdvUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
        )


class SubCategoryForm(forms.ModelForm):
    super_category = forms.ModelChoiceField(
        queryset=SuperCategory.objects.all(),
        empty_label=None,
        label="Надкатегория",
        required=True,
    )

    class Meta:
        model = SubCategory
        fields = "__all__"


class BbForm(forms.ModelForm):
    class Meta:
        model = Bb
        fields = "__all__"
        widgets = {"author": forms.HiddenInput}


class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ("title", "price", "image", "author")
        widgets = {"author": forms.HiddenInput}


# Наборы форм (formsets) используются, когда форма должна обработать несколько
# моделей. Django также предоставляет наборы форм, к-рые можно использовать
# для обработки абора объектов, принадлежащих общему внешнему ключу.
AIFormSet = inlineformset_factory(Bb, AddiionalImage, fields="__all__")
