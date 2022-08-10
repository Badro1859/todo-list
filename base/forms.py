
from dataclasses import field
from pyexpat import model
from django import forms

from base.models import Category


class TaskForm(forms.Form):
    pass


class CategoryForm(forms.Form):

    class Meta:
        model = Category
        fields = ['name']
