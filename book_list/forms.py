from .models import Book
from django import forms
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_length(isbn):
    length = len(str(isbn))
    if length != 10 and length != 13:
        raise ValidationError(
            _('%(isbn)s must have 10 or 13 numbers'), params={'isbn': isbn})


class SearchForm(forms.Form):
    title = forms.CharField(required=False, validators=[MaxLengthValidator(50)])
    author = forms.CharField(required=False, validators=[MaxLengthValidator(50)])
    isbn = forms.IntegerField(required=False, validators=[validate_length, MinValueValidator(0)])


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
