from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from ..models import Question, Evaluation, QuestionCategory
from ..forms import EvaluateForm, AnswerForm, BaseAnswerFormSet
from django.forms import inlineformset_factory, formset_factory
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required

# Create your views here.
""" Anonymous users' view """

def index(request):
    if request.user.is_authenticated:
        """ Landing page authenticated users """
        question_category_list = QuestionCategory.objects.order_by('-pub_date')[:5]
        context = {'question_category_list': question_category_list}
    else:

        """ Landing page anonymous users """
        #question_category_list = QuestionCategory.objects.order_by('-pub_date')[:5]
        #context = {'question_category_list': question_category_list}
        context = {}
    return render(request, 'polls/index.html', context)


"""
Teacher views

"""

#help function
def is_member(user):
    #return user.groups.filter(name='Member').exists()
    return user.is_staff


@login_required
@user_passes_test(is_member)
def teacher_page(request):
    pass
    

@login_required
def categorydetails(request, question_category_id):
    question_category = QuestionCategory.objects.get(pk=question_category_id)
    context = {
        'question_category': question_category,
    }
    return render(request, 'polls/categorydetails.html', context,)

@login_required
#@user_passes_test(is_member, login_url='/polls/login/')
@permission_required('polls.add_question', raise_exception=True)
def manage_questions(request, question_category_id):
    """ Legg til eller endre spørsmål """
    question_category = QuestionCategory.objects.get(pk=question_category_id)
    QuestionInlineFormSet = inlineformset_factory(QuestionCategory, Question, fields=('question_text',))
    if request.method == "POST":
        print(" request method = post")
        formset = QuestionInlineFormSet(request.POST, request.FILES, instance=question_category)
        if formset.is_valid():
            print(" Formset is valid")
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(question_category.get_absolute_url())
        else: 
            print(formset.errors)
    else:
        formset = QuestionInlineFormSet(instance=question_category)
    return render(request, 'polls/managequestionswfields.html', {'formset': formset})

@login_required
def submit(request, question_category_id):
    """Testing Survey-taker submit their completed survey."""
    print(" Start view ######################")
    category = QuestionCategory.objects.get(pk=question_category_id)
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
    eva_obj = Evaluation.objects.filter(user=user)
    # Creating a list of dictionaries. This permits me to use the same
    # keyword in the keyword:value pairs.
    evaluation_data = [{'option': l.evaluation}
                    for l in eva_obj]
    
    list = [{ 'option': 20}, {'option': 50 }]
    print(" ########### evaluation_data ####", evaluation_data)
    if evaluation_data:
        print(type(evaluation_data[0]['option'])) 
    
    form_kwargs = {"empty_permitted": False}
    print("--- THIS IS FORM_KWARGS FROM THE VIEW ---")
    print(form_kwargs)
    AnswerFormSet = formset_factory(AnswerForm, extra=len(questions)-len(evaluation_data))
    content = []
    if request.method == "POST":
        print("###########POST-START###########")
        formset = AnswerFormSet(request.POST, form_kwargs=form_kwargs)
        if formset.is_valid():
            print("formset is valid")
            content.append("formset is valid")

            # with transaction.atomic():
            parent_child_merge = zip(questions, eva_obj)
            x = 0
            for form in formset:
                
                print("loop number :", x )
                opt = form.cleaned_data.get("option")
                q = questions[x]
                print(" question q er: ", q.question_text)
                try:
                    evaluation_object = eva_obj[x]
                    evaluation_object.evaluation = opt
                    evaluation_object.save()
                except IndexError:
                    e = Evaluation(question = q, user = user, evaluation = opt)
                    e.save()



                #print("form is: ", form)
                print("option is :", opt)
                #print(form.cleaned_data["option"])
                x = x+1
            for q, e in parent_child_merge:
                print (q.question_text, e.evaluation)
                content.append(q)
                content.append(e)
                
                """ Evaluation.objects.create(
                    evaluation = form.cleaned_data["option"], 
                    #question_id=sub_pk,
                ) """
            return HttpResponseRedirect(reverse('polls:cat_results', args=(1, )))
            print("###########POST-END###########")
            
    else:
        formset = AnswerFormSet(form_kwargs=form_kwargs, initial = evaluation_data)
    print("$$$$$$$$ formset $$$$$$$")
    for form in formset:
        print(form)
    question_forms = zip(questions, formset)
    print("#### question_forms #####")
    """ for questions, formset in question_forms:
        print("Q",questions, "F", formset )
     """
    #print("q_form = ", questions, formset)
    print("Type question_forms", type(question_forms))
    print(" End view ######################")
    return render(
        request,
        "polls/submit.html",
        {"survey": survey, "question_forms": question_forms, "formset": formset, 'category': category,},
    )

def category_results(request, question_category_id):
    
    question_category = QuestionCategory.objects.get(pk=question_category_id)
    user = request.user
    try:
        results = QuestionCategory.objects.prefetch_related("question_set__evaluation_set").get(
            pk=question_category_id
        )
    except QuestionCategory.DoesNotExist:
        raise Http404()
    # look up the questions
    questions = results.question_set.all()
    # look up existing evaluations for the user
    options = [q.evaluation_set.filter(user=user) for q in questions]
    # Choosing first evaluation object from evaluation query set associated with the user
    #evaluation_object = question.evaluation_set.filter(user=user)[0]
    # The concrete evaluation from the object
    eva_obj = Evaluation.objects.filter(user=user)
    evaluation_data = [{'option': l.evaluation}
                    for l in eva_obj]
    q_and_e = zip(questions, evaluation_data)
    context = {'questions': questions, 
                'evaluation_data': evaluation_data,
                'q_and_e': q_and_e,
                'question_category': question_category,
                }
    return render(request, 'polls/category_results.html', context )

def student_overview(request):
    # start or edit test
    question_categories = QuestionCategory.objects.all() 
    context = {'question_categories': question_categories}
    return render(request, 'polls/mypage.html', context)


""" Below this line only singe question views"""
def orignal_results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

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