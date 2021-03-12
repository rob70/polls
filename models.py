from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _



# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')




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