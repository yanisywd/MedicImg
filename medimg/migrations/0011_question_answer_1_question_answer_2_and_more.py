# Generated by Django 4.1.7 on 2023-03-21 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medimg', '0010_remove_question_answer_1_remove_question_answer_2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answer_1',
            field=models.CharField(default='default_value1', max_length=255),
        ),
        migrations.AddField(
            model_name='question',
            name='answer_2',
            field=models.CharField(default='default_value2', max_length=255),
        ),
        migrations.AddField(
            model_name='question',
            name='answer_3',
            field=models.CharField(default='default_value3', max_length=255),
        ),
        migrations.AddField(
            model_name='question',
            name='answer_4',
            field=models.CharField(default='default_value4', max_length=255),
        ),
        migrations.AddField(
            model_name='question',
            name='correct_answer',
            field=models.CharField(default='correct_answer_default', max_length=255),
        ),
    ]
