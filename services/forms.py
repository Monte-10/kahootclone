from django import forms

class QuestionnaireForm(forms.Form):
    title = forms.CharField(max_length=150)