from django.urls import path, include

from memoire.settings import MEDIA_ROOT
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from medimg.views import TodoViewSet , TodoListViewSet
# from rest_framework import routers 

urlpatterns = [
    path('', views.home , name='home'),
    path('pagefree/', views.pagefree, name='pagefree'),
    path('menu_prof/', views.menu_prof , name='menu_prof'),
    path('menu_etudiant/', views.menu_etudiant , name='menu_etudiant'),
    path('module/<str:module_name>/', views.module_detail, name='module_detail'),
    path('register_etudiant/', views.register_etudiant , name='register_etudiant'),
    path('register_prof/', views.register_prof , name='register_prof'),
    path('quiz/<int:pk>/delete/', views.delete_quiz, name='delete_quiz'),
    
    path('<int:quiz_id>/update/', views.update_quiz, name='update_quiz'),

    path('delete/<int:question_id>/', views.delete_question, name='delete_question'),
    path('quiz/<int:quiz_id>/add_question/', views.add_question, name='add_question'),
    path('quiz/', views.quiz_view , name='quiz'),

    # choisir un quiz et le passer 
    path('showcase_quiz/', views.showcase_quiz_view , name='showcase_quiz'),  
    path('quiz/<int:quiz_id>/', views.startquiz_view, name='startquiz'),
    path('quiz/<int:quiz_id>/submit/', views.quiz_submit, name='quiz_submit'),
    path('quiz/<int:quiz_id>/result/<int:score>/<int:total_points>/', views.quiz_result, name='quiz_result'),


    path('unlock_quiz/<int:quiz_id>/', views.unlock_quiz, name='unlock_quiz'),
    path('unlock_quiz_all/<int:quiz_id>/', views.unlock_quiz_all, name='unlock_quiz_all'),

    # consulter les notes
    path('notes/', views.notes , name='notes'),
    path('user/', views.userpage , name='user'),
    path('choice/', views.choice , name='choice'),
    path('login/', views.loginpage , name='login'),
    path('logout/', views.user_logout , name='logout'),
   
   path('document/', views.document, name='document'),
   path('deletedoc/<int:pk>/', views.document_delete, name='document_delete'),
   

]+static(settings.MEDIA_URL,document_root=MEDIA_ROOT)






# app_name = 'medimg'

# urlpatterns = [
#     path('' , views.index , name='index')
# ]
