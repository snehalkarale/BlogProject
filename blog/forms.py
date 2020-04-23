from django import forms
from .models import Comment

class EmailSendForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.Form):
    class Meta:
        model = Comment
        field = ('name','email','body')