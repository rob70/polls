from django import forms

class EvaluateForm(forms.Form):
    evaluate = forms.IntegerField(
                        label='Evaluate', 
                        widget=forms.NumberInput(),
                        required=False
                        )


class AnswerForm(forms.Form):
    """ I understand this as en override of the initialization method before 
    the parent class is initialized anew in super() """
    # *args brukes for et ubestemt antall argumenter uten keyword
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items(): 
            print ("%s : %s" %(key, value)) 
        # options are removed from the keyword arguments
        # and returned to the options variable
        # Reason: kwargs are - objects - and must be queried to get 
        # field information
        # The data goes from a django QuerySet to python set
        # Why? Set is an unordered list 

        options = kwargs.pop("options")
        print("Type of options is: ", type(options))
        # Django class "QuerySet"
        print("Options are: ", options)
        # Options must be a list of Option objects
        choices = {(o.pk, o.evaluation) for o in options}
        print("Choices ############")
        print(choices)
        print("Type of choices is: ", type(choices))
        # returns class: 'set' Set is unordered? 
        for a in choices:
            print("elements in choices: ", a)
        # Super
        super().__init__(*args, **kwargs)
        print(" Have called super !")
        if kwargs is not None:
            print("---- These are kwargs, post super ---")
            for key, value in kwargs.items(): 
                print ("%s : %s" %(key, value))
        else:
            print("kwargs is None")
        print("Hei")
        GEEKS_CHOICES =( 
            ("1", "0"), 
            ("2", "20"), 
            ("3", "50"), 
            ("4", "80"), 
            ("5", "100"), 
        ) 
        print("Type of Geeks_choices: ", type(GEEKS_CHOICES))
        option_field = forms.ChoiceField(choices=GEEKS_CHOICES, widget=forms.RadioSelect, required=True)
        self.fields["option"] = option_field

class BaseAnswerFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["options"] = kwargs["options"][index]
        return kwargs
