from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    #To order the fields
    fields = ["pub_date", "question_text"] 

    inlines = [ChoiceInline]
    
    # Adds more information fields
    list_display = ("question_text", "pub_date", "was_published_recently") 

    # Adds the option to filter the questions based on the pub_date
    list_filter = ["pub_date"]

    # Adds a search field for questions
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)