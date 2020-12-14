from django import forms
from django.contrib.auth.models import User
#this is for the authentication system that we've worked with before
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


#last one is the user creation form and this is provided by the django and it will help us
#handle the creation of our new users


class RegistrationForm(UserCreationForm):
    #parantez içindeki inheritance özelliğini aktarmak içindir, inherite ettiği class yani
    email = forms.EmailField()
    first_name = forms. CharField()
    last_name = forms.CharField()
    #email field orijinalde django user authentication sisteminde dahil değil sanırım
    #meta classta onu da ekledik ama username ve password1 password2 kendileri var zaten, password 1 ve 2 ikisinin eşleşip eşleşmediğini kontrol etmek için
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']



