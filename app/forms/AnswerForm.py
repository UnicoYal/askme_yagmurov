from app.models import Answer
from django import forms

class CreateForm(forms.ModelForm):
  class Meta:
    model = Answer
    fields = ['body']
    labels = {
      'body': 'Enter your answer',
    }
