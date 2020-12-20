from django import forms
from .models import Comment, Entry


# Kübra Felek
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_content',)
        #required form field is only comment content. Only registered user can add comment and comments are saved with this users


class ContactForm(forms.Form):
    username = forms.CharField(required=True)
    from_email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    #form fields are created
# Kübra Felek
