from django.contrib import admin
from django.utils.html import mark_safe
from . import models
from .models import Document, Etudiant, ReponseEtudiant, User

from django.utils.html import format_html



# class ProfesseurAdmin(admin.ModelAdmin): 
#     list_display=('name','email','module','profile_pic',)
# admin.site.register(models.Professeur, ProfesseurAdmin) 

# class EtudiantAdmin(admin.ModelAdmin): 
#     list_display=('name','email','profile_pic',)
# admin.site.register(models.Etudiant, EtudiantAdmin) 

class QuizAmin(admin.ModelAdmin): 
    list_display=('name','professeur','module','total',)
    actions = ['delete_selected']
admin.site.register(models.Quiz, QuizAmin)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title','module', 'uploaded_by', 'uploaded_at', 'file_link')

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{0}">Télécharger</a>', obj.file.url)
        else:
            return '-'
    file_link.short_description = 'Fichier'

admin.site.register(Document, DocumentAdmin)

class ReponseEtudiantAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'question', 'reponse', 'correct')
    list_filter = ('etudiant', 'question', 'correct')
    search_fields = ('etudiant__name', 'question__question_text', 'reponse')

admin.site.register(ReponseEtudiant, ReponseEtudiantAdmin)

class QuestionAdmin(admin.ModelAdmin): 
    list_display = ('text', 'quiz','image_preview', 'answer_1', 'answer_2', 'answer_3', 'answer_4','points', 'correct_answer',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.image.url,
                width=100,
                height=75,
            ))
        else:
            return '(No image)'

    image_preview.short_description = 'Image'
admin.site.register(models.Question, QuestionAdmin)


class NoteAdmin(admin.ModelAdmin):
    list_display=('etudiant', 'quiz_name', 'note')
    
    def quiz_name(self, obj):
        return obj.quiz.name
    quiz_name.short_description = 'Quiz'

admin.site.register(models.Note, NoteAdmin)


class AnswerAdmin(admin.ModelAdmin): 
    list_display=('question','text','is_correct',)
admin.site.register(models.Answer, AnswerAdmin) 


class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'phone', 'email', 'profile_pic', 'submitted_quizzes_list')
    list_filter = ('user',)
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('user',)

    def submitted_quizzes_list(self, obj):
        return ", ".join([quiz.name for quiz in obj.submitted_quizzes.all()])
    submitted_quizzes_list.short_description = "Submitted Quizzes"

admin.site.register(Etudiant, EtudiantAdmin)







# class PersonneAdmin(admin.ModelAdmin): 
#     list_display=('name','email','profile_pic',)
# admin.site.register(models.Personne, PersonneAdmin) 

# admin.site.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display=('username',)
# admin.site.register(models.User, UserAdmin)


# class BannerAdmin(admin.ModelAdmin): 
#     list_display=('alt_text','image_tag')
# admin.site.register(models.Banners, BannerAdmin)

# class ServiceAdmin(admin.ModelAdmin): 
#     list_display=('title',)
# admin.site.register(models.Service, ServiceAdmin) 

# class PageAdmin(admin.ModelAdmin): 
#     list_display=('title',)
# admin.site.register(models.Page, PageAdmin) 

# class FaqAdmin(admin.ModelAdmin): 
#     list_display=('quest',)
# admin.site.register(models.Faq, FaqAdmin) 

# class EnquiryAdmin(admin.ModelAdmin): 
#     list_display=('full_name','email','detail','send_time')
# admin.site.register(models.Enquiry, EnquiryAdmin) 

# class GalleryAdmin(admin.ModelAdmin): 
#     list_display=('title','image_tag')
# admin.site.register(models.Gallery, GalleryAdmin) 

# class GalleryImageAdmin(admin.ModelAdmin): 
#     list_display=('alt_text','image_tag')
# admin.site.register(models.GalleryImage, GalleryImageAdmin) 

# class PlanAdmin(admin.ModelAdmin): 
#     list_display=('title','price','max_member','highlight_status',)
#     list_editable=('highlight_status','max_member')
# admin.site.register(models.Plan, PlanAdmin) 

# listdiplay : les champ qui seront afficher en db 
# en faite tout ce qui est ici sert a editer le cli de la db

# class FeaturePlanAdmin(admin.ModelAdmin): 
#     list_display=('title','theplans')
#     def theplans(self,obj):
#         return " | ".join([sub.title for sub in obj.plan.all()])
# admin.site.register(models.FeaturePlan, FeaturePlanAdmin) 




