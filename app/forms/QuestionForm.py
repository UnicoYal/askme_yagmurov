from app.models import Question
from django import forms

class AskForm(forms.ModelForm):
  class Meta:
    model = Question
    fields = ['title', 'body', 'tags']
