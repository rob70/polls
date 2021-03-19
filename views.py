from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Evaluation, QuestionCategory
from .forms import EvaluateForm, AnswerForm, BaseAnswerFormSet
from django.forms import inlineformset_factory, formset_factory


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

# Add questions
def manage_questions(request, question_category_id):
    question_category = QuestionCategory.objects.get(pk=question_category_id)
    QuestionInlineFormSet = inlineformset_factory(QuestionCategory, Question, fields=('question_text',))
    if request.method == "POST":
        formset = QuestionInlineFormSet(request.POST, request.FILES, instance=question_category)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(question_category.get_absolute_url())
    else:
        formset = QuestionInlineFormSet(instance=question_category)
    return render(request, 'polls/managequestions.html', {'formset': formset})


def submit(request, question_category_id):
    """Testing Survey-taker submit their completed survey."""
    print(" Start view ######################")
    user = request.user
    try:
        survey = QuestionCategory.objects.prefetch_related("question_set__evaluation_set").get(
            pk=question_category_id
        )
    except QuestionCategory.DoesNotExist:
        raise Http404()
    """
    try:
        sub = survey.submission_set.get(pk=sub_pk, is_complete=False)
    except Submission.DoesNotExist:
        raise Http404()  """

    questions = survey.question_set.all()
    # options is a QuerySet of Evaluation objects for each question
    options = [q.evaluation_set.filter(user=user) for q in questions]
    form_kwargs = {"empty_permitted": False, "options": options}
    print("--- THIS IS FORM_KWARGS FROM THE VIEW ---")
    print(form_kwargs)
    AnswerFormSet = formset_factory(AnswerForm, extra=len(questions), formset=BaseAnswerFormSet)
    if request.method == "POST":
        formset = AnswerFormSet(request.POST, form_kwargs=form_kwargs)
        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    Evaluation.objects.create(
                        evaluation = form.cleaned_data["option"], 
                        question_id=sub_pk,
                    )

                sub.is_complete = True
                sub.save()
            return redirect("survey-thanks", pk=survey_pk)

    else:
        formset = AnswerFormSet(form_kwargs=form_kwargs)

    question_forms = zip(questions, formset)
    print("Type question_forms", type(question_forms))
    print(" End view ######################")
    return render(
        request,
        "polls/submit.html",
        {"survey": survey, "question_forms": question_forms, "formset": formset},
    )


def orignal_results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

