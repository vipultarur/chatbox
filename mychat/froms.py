from django import forms
from django.forms import ModelForm
from mychat.models import ChatMessage


class ChatMessageForm(forms.ModelForm):
    body=forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control form-control-lg" ,
        "placeholder":"Type message",
        "id":"messageInput",
        "autocomplete":"off",
        }))
    class Meta:
        model=ChatMessage
        fields=["body"]