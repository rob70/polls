from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime




# Create your models here.
class QuestionCategory(models.Model):
    category_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=datetime.now)
    def __str__(self):
        return self.category_text

class Question(models.Model):
    question_category = models.ForeignKey(QuestionCategory, default=1, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=datetime.now)
    def __str__(self):
        return self.question_text



""" 
Source for choices solution: 
https://www.merixstudio.com/blog/django-models-declaring-list-available-choices-right-way/
"""
class Evaluation(models.Model):
    """" An evaluation of each question as an integer 
    submitted by a user """
    INGEN = 0
    NOE = 20
    GANSKE = 50
    TILFREDSTILLENDE = 70
    TOPP = 100
    EVALUATION = (
        (INGEN, _('Ingen kunnskaper')),
        (NOE, _('Noe kjennskap')),
        (GANSKE, _('Trenger repetisjon')),
        (TILFREDSTILLENDE, _('Behersker dette')),
        (TOPP, _('Alt i orden')),
    )
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True,
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    #choice = models.ForeignKey(Choice, on_delete=models.CASCADE)    
    evaluation = models.IntegerField(default=0, choices=EVALUATION)
    def __str__(self):
        return str(self.evaluation)