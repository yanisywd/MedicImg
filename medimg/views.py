from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.forms import inlineformset_factory
from medimg.forms import CreateUserForm, ProfesseurForm
from django.urls import reverse
from django.forms import formset_factory
from django.http import HttpResponseForbidden
from django.contrib.sessions.backends.db import SessionStore

# from medimg.admin import PersonneAdmin
from .models import *
from .forms import  CreateUserForm, DocumentForm, EtudiantForm,ProfesseurForm, ProfesseurProfileForm, QuestionForm, QuizForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages

from django.contrib.auth import authenticate , login ,logout 
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user , allowed_user
from django.contrib.auth.models import Group

from medimg import forms 


def pagefree(request):
    return render(request, 'pagefree.html')
# login_required(login_url='login')
@allowed_user(allowed_roles=['etudiant','admin','professeur'])
def home(request):
    if hasattr(request.user, 'professeur'):
        return render(request, 'menu_prof.html')
    elif hasattr(request.user, 'etudiant'):
        return render(request, 'menu_etudiant.html')
    else:
        raise ValueError("User is not a professeur or etudiant.")

@allowed_user(allowed_roles=['etudiant','admin'])
def menu_etudiant(request):
    etudiant = Etudiant.objects.get(user=request.user)
    notes_etudiant = Note.objects.filter(etudiant=etudiant)
    modules = Professeur.MODULE_CHOICES
    quiz_par_module = {}

    for module in modules:
        quizs = Quiz.objects.filter(module=module[0])
        quiz_infos = []

        for quiz in quizs:
            note_etudiant = next((note for note in notes_etudiant if note.quiz == quiz), None)
            if note_etudiant:
                reponses_etudiant = ReponseEtudiant.objects.filter(etudiant=etudiant, question__quiz=quiz).order_by('-date')
                quiz_infos.append({
                    'quiz': quiz,
                    'total': quiz.total,
                    'note': note_etudiant.note,
                    'status': 'Passé',
                    'reponses_etudiant': reponses_etudiant
                })
            else:
                quiz_infos.append({
                    'quiz': quiz,
                    'note': None,
                    'total': None,
                    'status': 'Non passé',
                    'reponses_etudiant': []
                })

        quiz_par_module[module[0]] = quiz_infos

    context = {
        'quiz_par_module': quiz_par_module,
    }

    return render(request, 'menu_etudiant.html', context)


@allowed_user(allowed_roles=['admin','professeur'])
def menu_prof(request):
    

    return render(request, 'menu_prof.html')


def module_detail(request, module_name):
    quizzes = Quiz.objects.filter(module=module_name)
    documents = Document.objects.filter(module=module_name)

    context = {
        'module_name': module_name,
        'quizzes': quizzes,
        'documents': documents,
    }
    return render(request, 'module_detail.html', context)


def notes(request):
    quizzes = Quiz.objects.filter(professeur=request.user)
    notes = Note.objects.filter(quiz__in=quizzes)

    # Liste des étudiants pour la liste déroulante de suggestions
    etudiants = Etudiant.objects.order_by('name')

    # Liste des quiz pour la liste déroulante de suggestions
    quizzes = Quiz.objects.order_by('name')

    # Filtre par étudiant
    etudiant_filter = request.GET.get('etudiant')
    if etudiant_filter:
        notes = notes.filter(etudiant_id=etudiant_filter)

    # Filtre par quiz
    quiz_filter = request.GET.get('quiz')
    if quiz_filter:
        notes = notes.filter(quiz__name__icontains=quiz_filter)

    # Filtre par note
    note_filter = request.GET.get('note')
    if note_filter:
        if note_filter == 'meilleures':
            notes = notes.order_by('-note')
        elif note_filter == 'pires':
            notes = notes.order_by('note')
        else:
            notes = notes.filter(note=note_filter)

    reponses = ReponseEtudiant.objects.filter(etudiant__in=etudiants).select_related('question', 'etudiant')

    return render(request, 'notes.html', {'notes': notes, 'etudiants': etudiants, 'quizzes': quizzes, 'reponses': reponses})



def choice(request):
    return render(request, 'choice.html')


@unauthenticated_user
def register_prof(request):
     form = ProfesseurForm()
     if request.method =='POST':
          form = ProfesseurForm(request.POST)
          if form.is_valid():
               user = form.save()
               username = form.cleaned_data.get('username')
               messages.success(request, 'Account was created for ' + username)
               group = Group.objects.get(name='professeur')
               user.groups.add(group)
               Professeur.objects.create(
                    user=user,
                    name=username,
                    email=form.cleaned_data.get('email'),
                    module=form.cleaned_data.get('module'),
               )
               return redirect('login')   
     context ={'form':form}
     return render(request, 'register_prof.html',context)

@unauthenticated_user
def register_etudiant(request):
     form = CreateUserForm()
     if request.method =='POST':
          form = CreateUserForm(request.POST)
          if form.is_valid():
               user = form.save()
               username = form.cleaned_data.get('username')
               messages.success(request, 'Account was created for ' + username)
               group = Group.objects.get(name='etudiant')
               user.groups.add(group)
               Etudiant.objects.create(
                    user=user,
                    name=username,
                    email=form.cleaned_data.get('email'),
               )
               return redirect('login')   
     context ={'form':form}
     return render(request, 'register_etudiant.html',context)


@unauthenticated_user
def loginpage(request):  
     if request.method =='POST':
          username=request.POST.get('username')
          password=request.POST.get('password')
          user = authenticate(request , username=username, password=password)
          if user is not None :
               login(request, user)
               if hasattr(user, 'etudiant'):
                return redirect('menu_etudiant')
               if hasattr(user, 'professeur'):
                return redirect('menu_prof')
          else: 
               messages.info(request, 'username or password is incorrect ! ')
          
     context ={}
     return render(request, 'login.html',context)



def user_logout(request): 
    #  dans le logout je supprime tout le contenue des session 
    #  request.session.flush()
    #  request.session.clear()
     logout(request)
     return redirect('login')


def userpage(request):
    user = request.user
    
    if hasattr(user, 'etudiant'):
        profile = user.etudiant
        form = EtudiantForm(instance=profile)
    elif hasattr(user, 'professeur'):
        profile = user.professeur
        form = ProfesseurProfileForm(instance=profile)
    else:
        raise ValueError("User is not an etudiant or professeur.")
    
    if request.method == 'POST':
        form = EtudiantForm(request.POST, request.FILES, instance=profile) if hasattr(user, 'etudiant')else ProfesseurProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    
    context = {
        'form': form,
        'profile': profile,
    }
    
    return render(request, 'user.html', context)


def quiz_view(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.professeur = request.user
            quiz.save()
            return redirect('quiz',)
    else:
        form = QuizForm()
    quizzes = Quiz.objects.all()
    students = Etudiant.objects.filter(submitted_quizzes__isnull=False).distinct()
    return render(request, 'quiz.html', {'quizzes': quizzes, 'form': form, 'students': students})


from django.http import HttpResponseNotAllowed

def unlock_quiz(request, quiz_id):
    if request.method == "POST":
        student_id = request.POST['student_id']
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        student = get_object_or_404(Etudiant, pk=student_id)

        if quiz.professeur == request.user:
            student.submitted_quizzes.remove(quiz)
            student.save()
            return redirect('quiz')

    return HttpResponseNotAllowed(['POST'])
def unlock_quiz_all(request, quiz_id):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, pk=quiz_id)

        if quiz.professeur == request.user:
            students = Etudiant.objects.filter(submitted_quizzes=quiz)
            for student in students:
                student.submitted_quizzes.remove(quiz)
                student.save()
            return redirect('quiz')

    return HttpResponseNotAllowed(['POST'])



def showcase_quiz_view(request):
    quizzes = Quiz.objects.all()
    quiz_notes = {}
    for quiz in quizzes:
        notes = {}
        for note in quiz.note_set.all():
            notes[note.etudiant] = note.note
        quiz_notes[quiz] = notes

    quiz_status = request.user.etudiant.quiz_and_submitted_status()

    return render(request, 'showcase_quiz.html', {'quiz_notes': quiz_notes, 'quiz_status': quiz_status})



def startquiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()
    etudiant = request.user.etudiant

    if request.method == 'POST':
        return redirect('quiz_submit', quiz_id=quiz_id)

    if etudiant.submitted_quizzes.filter(pk=quiz_id).exists():
        return HttpResponseForbidden("Vous avez déjà soumis ce quiz.")
    else:    
        return render(request, 'startquiz.html', {'quiz': quiz, 'questions': questions})

   

def quiz_submit(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()
    etudiant = request.user.etudiant
    score = 0
    total_points = 0 
    for question in questions:
        total_points += question.points 
        answer = request.POST.get('answer_{}'.format(question.id))
        correct = answer == question.correct_answer
        if correct:
             score += question.points 

        reponse_etudiant = ReponseEtudiant(etudiant=etudiant, question=question, reponse=answer, correct=correct,date=timezone.now())
        reponse_etudiant.save()
    
    note, created = Note.objects.get_or_create(quiz=quiz, etudiant=etudiant)
    note.etudiant_name = etudiant.name
    note.note = score
    note.date = timezone.now()
    note.save()

    submitted_quizzes = request.session.get('submitted_quizzes', [])
    submitted_quizzes.append(quiz_id)
    request.session['submitted_quizzes'] = submitted_quizzes

    request.session['quiz_id'] = quiz.pk

    scores = request.session.get('scores', {})
    scores[quiz_id] = score
    request.session['scores'] = scores

    total_points_dict = request.session.get('total_points', {})
    total_points_dict[quiz_id] = total_points
    request.session['total_points'] = total_points_dict

    etudiant.submitted_quizzes.add(quiz)
    etudiant.save()

    request.session.save()
    print("submit quiz ")
    print(request.session.items())
   
    return redirect('quiz_result', quiz_id=quiz_id, score=score, total_points=total_points)


def quiz_result(request, quiz_id, score, total_points):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    print(total_points)
    quiz.total=total_points
    quiz.save()
    if score >= len(quiz.questions.all()) / 2:
        message = "Bravo, vous avez réussi le quiz {} !".format(quiz.name)
    else:
        message = "Dommage, vous n'avez pas réussi le quiz {}.".format(quiz.name)
    return render(request, 'quiz_result.html', {'quiz': quiz, 'score': score, 'message': message, 'total_points': total_points})



def delete_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    quiz.delete()
    return redirect('quiz')

def update_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if quiz.professeur != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.professeur = request.user
            quiz.save()
            return redirect('quiz')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'update_quiz.html', {'form': form, 'quiz': quiz})




def delete_question(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, id=question_id)
        question.delete()
        return redirect(reverse('add_question', kwargs={'quiz_id': question.quiz.id}))

def add_question(request, quiz_id):
    print("hehehehehehehhehehh")
    quiz = Quiz.objects.get(pk=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            correct_answer = request.POST.get('correct_answer')
            if correct_answer == 'default_value1':
                question.correct_answer = question.answer_1
            elif correct_answer == 'default_value2':
                question.correct_answer = question.answer_2
            elif correct_answer == 'default_value3':
                question.correct_answer = question.answer_3
            elif correct_answer == 'default_value4':
                question.correct_answer = question.answer_4
            question.save()
            return redirect('add_question', quiz_id=quiz_id)
    else:
        form = QuestionForm()

    questions = Question.objects.filter(quiz=quiz)

    context = {
        'quiz': quiz,
        'form': form,
        'questions': questions
    }
    return render(request, 'add_question.html', context)






def document(request):
    documents = Document.objects.filter(uploaded_by=request.user.professeur)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user.professeur
            document.save()
            return redirect('document')
    else:
        form = DocumentForm()
    return render(request, 'document.html', {'documents': documents, 'form': form})


def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk, uploaded_by=request.user.professeur)
    if request.method == 'POST':
        document.delete()
        return redirect('document')
    return render(request, 'confirm.html', {'document': document})




# def notes(request):
     
#     quizzes = Quiz.objects.filter(professeur=request.user)
#     notes = Note.objects.filter(quiz__in=quizzes)

#     # Liste des étudiants pour la liste déroulante de suggestions
#     etudiants = Etudiant.objects.order_by('name')

#     # Liste des quiz pour la liste déroulante de suggestions
#     quizzes = Quiz.objects.order_by('name')

#     # Filtre par étudiant
#     etudiant_filter = request.GET.get('etudiant')
#     if etudiant_filter:
#         notes = notes.filter(etudiant_id=etudiant_filter)

#     # Filtre par quiz
#     quiz_filter = request.GET.get('quiz')
#     if quiz_filter:
#         notes = notes.filter(quiz__name__icontains=quiz_filter)

#     # Filtre par note
#     note_filter = request.GET.get('note')
#     if note_filter:
#         if note_filter == 'meilleures':
#             notes = notes.order_by('-note')
#         elif note_filter == 'pires':
#             notes = notes.order_by('note')
#         else:
#             notes = notes.filter(note=note_filter)

#     return render(request, 'notes.html', {'notes': notes, 'etudiants': etudiants, 'quizzes': quizzes})


# for showcasing quizes
# def showcase_quiz_view(request):
#     quizzes = Quiz.objects.all()
#     quiz_notes = {}
#     for quiz in quizzes:
#         notes = {}
#         for note in quiz.note_set.all():
#             notes[note.etudiant] = note.note
#         quiz_notes[quiz] = notes

#     return render(request, 'showcase_quiz.html', {'quiz_notes': quiz_notes})


# showcase the quiz 

# def startquiz_view(request, quiz_id):   
#     quiz = get_object_or_404(Quiz, pk=quiz_id)
#     questions = quiz.questions.all()
#     if request.method == 'POST':
#         return redirect('quiz_submit', quiz_id=quiz_id)
#     print(request.session.items())
#     print("oooolalal ")
#     if quiz_id in request.session.get('submitted_quizzes', []):
#          return HttpResponseForbidden("Vous avez déjà soumis ce quiz.")
#     else:    
#      return render(request, 'startquiz.html', {'quiz': quiz, 'questions': questions})

# def quiz_submit(request, quiz_id):
#     quiz = get_object_or_404(Quiz, pk=quiz_id)
#     questions = quiz.questions.all()
#     etudiant = request.user.etudiant
#     score = 0
#     total_points = 0 
#     for question in questions:
#         total_points += question.points 
#         answer = request.POST.get('answer_{}'.format(question.id))
#         if answer == question.correct_answer:
#              score += question.points 
#     note, created = Note.objects.get_or_create(quiz=quiz, etudiant=etudiant)
#     note.etudiant_name = etudiant.name
#     note.note = score
#     note.save()

    

#     submitted_quizzes = request.session.get('submitted_quizzes', [])
#     submitted_quizzes.append(quiz_id)
#     request.session['submitted_quizzes'] = submitted_quizzes

#     request.session['quiz_id'] = quiz.pk

#     scores = request.session.get('scores', {})
#     scores[quiz_id] = score
#     request.session['scores'] = scores

#     total_points_dict = request.session.get('total_points', {})
#     total_points_dict[quiz_id] = total_points
#     request.session['total_points'] = total_points_dict

#     request.session.save()
#     print("submit quiz ")
#     print(request.session.items())
   
#     return redirect('quiz_result', quiz_id=quiz_id, score=score, total_points=total_points)
