# Generated by Django 4.0.5 on 2022-07-22 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_category_task_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['category']},
        ),
        migrations.AddField(
            model_name='task',
            name='primary',
            field=models.BooleanField(default=False),
        ),
    ]
