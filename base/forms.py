from django import forms
from django.forms import ModelForm,DateTimeInput
from .models import login_user,Polls_details,Choice_poll

class loginform(ModelForm):
    username = forms.CharField(label='username',
    widget = forms.TextInput(attrs={'class': 'form-cont\
    rol '}))
    password = forms.CharField(label='password',
    widget = forms.TextInput(attrs={'class': 'form-cont\
    rol '}))

    class Meta:

        model=login_user
        fields='__all__'

class createpoll(ModelForm):
    Date_end = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model=Polls_details
        fields=['Question','Desc','Date_end']

class createchoices(ModelForm):

    class Meta:
        model=Choice_poll
        fields=['choices']