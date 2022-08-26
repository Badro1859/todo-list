
from django import forms

from base.models import Task, Category


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': "task title"})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'rows': 2, 'placeholder': "task description"})

    class Meta:
        model = Task
        exclude = ['user']


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']
