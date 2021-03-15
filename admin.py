from django.contrib import admin

# Register your models here.
from .models import Question, QuestionCategory

admin.site.register(Question)
admin.site.register(QuestionCategory)