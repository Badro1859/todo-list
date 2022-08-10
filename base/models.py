import datetime
from django.db import models

from user.models import CustomUser


class Category(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(default=datetime.date.today)

    complete = models.BooleanField(default=False)
    primary = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['category']
