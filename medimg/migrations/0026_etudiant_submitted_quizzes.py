# Generated by Django 4.1.7 on 2023-04-14 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medimg', '0025_rename_est_correcte_reponseetudiant_correct_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='etudiant',
            name='submitted_quizzes',
            field=models.ManyToManyField(blank=True, to='medimg.quiz'),
        ),
    ]
