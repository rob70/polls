from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Evaluation, QuestionCategory
from .forms import EvaluateForm 

# Create your views here.
def index(request):
    question_category_list = QuestionCategory.objects.order_by('-pub_date')[:5]
    context = {'question_category_list': question_category_list}
    return render(request, 'polls/index.html', context)

def vote(request, question_id):
    user = request.user 
    question = get_object_or_404(Question, pk=question_id)
    # Out of bounds error when this one has yet to be created.
    #evaluation_object = question.evaluation_set.filter(user=user)[0]
    

    # if POST, process the form
    if request.method == 'POST':
        # create a form instance and populate
        form = EvaluateForm(request.POST)
        # check whether it is valid:
        if form.is_valid():
            ev = form.cleaned_data['evaluate']
            try: 
                evaluation_object = question.evaluation_set.filter(user=user)[0]
            # Throws an error because it has not yet been created
                evaluation_object.evaluation = ev
                evaluation_object.save()
            except IndexError:
                question.evaluation_set.create(user=user, evaluation= ev)
                
            return HttpResponseRedirect(reverse('polls:results', args=
            (question.id, )))
    else:
        form = EvaluateForm()
        context = {'form': form}

    return render(request, 'polls:detail', context)


def results(request, question_id):
    user = request.user
    question = Question.objects.get(pk=question_id)
    print("question ", question)
    evaluation_object = question.evaluation_set.filter(user=user)[0]
    evaluation = evaluation_object.evaluation
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question, 'evaluation': evaluation}
    return render(request, 'polls/results.html', context )

def detail(request, question_id):
    user_id = request.user
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    evaluation = question.evaluation_set.filter(user = user_id)
    ev = 0
    if evaluation: 
        print("Evaluation is : ", evaluation)
        print(evaluation[0].evaluation)
        ev=evaluation[0].evaluation
    else:
        pass
    form = EvaluateForm(initial={'evaluate': ev})
    context = {
        'question': question,
        'evaluation': evaluation,
        'request': request,
        'form': form, 
    }
    return render(request, 'polls/detail.html', context)
"""
Category views
"""

def categorydetails(request, question_category_id):
    question_category = QuestionCategory.objects.get(pk=question_category_id)
    context = {
        'question_category': question_category,
    }
    return render(request, 'polls/categorydetails.html', context,)

def manage_questions(request, question_category_id):
    question_category = QuestionCategory.objects.get(pk=question_category_id)
    QuestionInlineFormSet = inlineformset_factory(QuestionCategory, Question, fields=('question_text',))
    if request.method == "POST":
        formset = QuestionInlineFormSet(request.POST, request.FILES, instance=author)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(question_category.get_absolute_url())
    else:
        formset = QuestionInlineFormSet(instance=question_category)
    return render(request, 'polls/managequestions.html', {'formset': formset})


def orignal_results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

