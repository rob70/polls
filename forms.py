from django import forms

class EvaluateForm(forms.Form):
    evaluate = forms.IntegerField(
                        label='Evaluate', 
                        widget=forms.NumberInput(),
                        required=False
                        )

