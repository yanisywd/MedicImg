# Generated by Django 4.1.7 on 2023-04-05 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medimg', '0021_document_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]