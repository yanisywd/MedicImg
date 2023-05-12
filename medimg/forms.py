from django import forms
# from .models import Personne
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from medimg.models import Answer, Document, Etudiant, Professeur, Question, Quiz

class CreateUserForm(UserCreationForm):
     email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    #  group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
     class Meta: 
         model = User 
         fields =  ['username' , 'email' , 'password1' , 'password2',]
         widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
         
# class ProfesseurForm(UserCreationForm):

#     module = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))


#     class Meta:
#         model = User
#         fields = ['username', 'email', 'module', 'password1', 'password2']
#         widgets = {
#            'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
#             'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
#         }
class ProfesseurForm(UserCreationForm):
    module_choices = (
        ('Radiographie', 'Radiographie'),
        ('Tomodensitométrie', 'Tomodensitométrie'),
        ('IRM', 'IRM'),
        ('Échographie', 'Échographie'),
        ('Scintigraphie', 'Scintigraphie'),
        ('Angiographie', 'Angiographie'),
    )
    module = forms.ChoiceField(choices=module_choices, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'module', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class ProfesseurProfileForm(ModelForm):
    class Meta:
        model = Professeur
        fields = '__all__'
        exclude = ['user']

class EtudiantForm(ModelForm):
    class Meta:
        model = Etudiant
        fields = '__all__'
        exclude = ['user','submitted_quizzes']



# class QuizForm(forms.ModelForm):
#     duration = forms.IntegerField(label='Duration (minutes)')
#     class Meta:
#         model = Quiz
#         fields = ('name','duration')
class QuizForm(forms.ModelForm):
    MODULE_CHOICES = [
        ('Radiographie', 'Radiographie'),
        ('Tomodensitométrie', 'Tomodensitométrie'),
        ('IRM', 'IRM'),
        ('Échographie', 'Échographie'),
        ('Scintigraphie', 'Scintigraphie'),
        ('Angiographie', 'Angiographie'),
    ]

    module = forms.ChoiceField(choices=MODULE_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Quiz
        fields = ['name', 'duration', 'module']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'answer_1','points', 'answer_2', 'answer_3', 'answer_4', 'correct_answer', 'image']
        widgets = {
            'correct_answer': forms.HiddenInput,
        }
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("L'image est obligatoire.")




class DocumentForm(forms.ModelForm):
    MODULE_CHOICES = [
        ('Radiographie', 'Radiographie'),
        ('Tomodensitométrie', 'Tomodensitométrie'),
        ('IRM', 'IRM'),
        ('Échographie', 'Échographie'),
        ('Scintigraphie', 'Scintigraphie'),
        ('Angiographie', 'Angiographie'),
    ]
    module = forms.ChoiceField(choices=MODULE_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Document
        fields = ('title','module', 'description', 'file')