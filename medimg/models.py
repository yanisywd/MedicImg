
from django.utils import timezone
from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User , AbstractUser , Group


class Quiz(models.Model):
    name = models.CharField(max_length=200)
    duration = models.IntegerField(default=0)
    module = models.CharField(max_length=200, null=True)
    professeur = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total  = models.IntegerField(default=0)
class Professeur(models.Model):
    MODULE_CHOICES = [
        ('Radiographie', 'Radiographie'),
        ('Tomodensitométrie', 'Tomodensitométrie'),
        ('IRM', 'IRM'),
        ('Échographie', 'Échographie'),
        ('Scintigraphie', 'Scintigraphie'),
        ('Angiographie', 'Angiographie'),
    ]
    name = models.CharField(max_length=200, null=True)
    user = models.OneToOneField(User,null=True,blank=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    module = models.CharField(max_length=200, null=True, choices=MODULE_CHOICES)
    profile_pic = models.ImageField(null=True,default='default.png' ,blank=True)
    def save(self, *args, **kwargs):
        if self.user:
            self.user.username = self.name
            self.user.save()
        super(Professeur, self).save(*args, **kwargs)

class Etudiant(models.Model):
    name = models.CharField(max_length=200, null=True)
    user = models.OneToOneField(User,null=True,blank=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(null=True,default='default.png' ,blank=True)
    submitted_quizzes = models.ManyToManyField(Quiz, blank=True)
    def save(self, *args, **kwargs):
        if self.user:
            self.user.username = self.name
            self.user.save()
        super(Etudiant, self).save(*args, **kwargs)
    # avec la methode str la representation de l objet etudiant sera le nom de letudiant
    def __str__(self):
        return self.name
    def quiz_and_submitted_status(self):
        quizzes = Quiz.objects.all()
        quiz_status = []
        for quiz in quizzes:
            submitted = self.submitted_quizzes.filter(pk=quiz.pk).exists()
            quiz_status.append((quiz, submitted))
        return quiz_status
    def remove_submitted_quiz(self, quiz):
        self.submitted_quizzes.remove(quiz)
        self.save()
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    image = models.ImageField(null=True, blank=True)
    text = models.TextField()
    answer_1 = models.CharField( max_length=255, default='default_value1')
    answer_2 = models.CharField( max_length=255, default='default_value2')
    answer_3 = models.CharField( max_length=255, default='default_value3')
    answer_4 = models.CharField( max_length=255, default='default_value4')
    correct_answer = models.CharField(max_length=255, default='correct_answer_default')
    points = models.PositiveIntegerField(default=1)
    
    




class Document(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(Professeur, on_delete=models.CASCADE)
    module = models.CharField(max_length=200, null=True)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Note(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    note = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)



class ReponseEtudiant(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reponse = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.etudiant} - {self.question} - {self.reponse} - {self.correct}"



class StudentAnswer(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=10)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.etudiant} - {self.question}"
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

class amirouche(models.Model):
    cz = models.CharField(max_length=200)

class hamza(models.Model):
    name = models.CharField(max_length=200)
class hichem(models.Model):
    name = models.CharField(max_length=200)




