from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import DetailView

from entries.models import Profile, Entry
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.

#Kübra Felek --------------------
def register(request):
    if request.method == 'POST':
        #if the post is created and form is completed, thats mean the form is posted, and if it returns is_valid true and the info is saved into db
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # if form data is valid then save it into the database
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            profile = Profile.objects.create(user=user, )
            profile.save()
            login(request, user)
            return redirect('blog-home')

    else:
        # if anything is not posted, thats mean the form is not competed, here a form is created. new empty form is created.
        form = RegistrationForm()

    # context dictionary is created in here and it will contain the name form that contains the value for this form that we've created above here
    # and once we create that this we can pass this in as the third argument in the below return statement
    # so we can actually access the form within our template and this template is register.html within our users dictionary
    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        # here there is same form logic with registration
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('blog-home')

        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })


class UserAccountSettingsView(generic.UpdateView):
    form_class = UserChangeForm
    #UserChangeForm is the form of the authentication system of the django.
    template_name = 'users/user_account_settings.html'
    #it takes this html file as ui
    success_url = reverse_lazy('blog-home')

    def get_object(self):
        return self.request.user

#Kübra Felek ----------------



#Nursena Karakulah --------
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'users/user_profile_page.html'

    def get_context_data(self, *args, **kwargs):

        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile,
                                      pk=self.kwargs['pk'])  # to get a specific user. kwargs['pk'] coming from urls.py
        entries = Entry.objects.filter(entry_author_id=page_user.user.id)
        #with context we pass some elements such as in here we pass user and its entries to display user profile page
        context = {'page_user': page_user, 'entries': entries}
        return context


class EditProfilePageView(SuccessMessageMixin, generic.UpdateView):
    model = Profile
    template_name = 'users/edit_profile_page.html'
    #this template is used for edit profile function and the model in here our Profile model. Generic Updateview of django is used in here and the fiels are determined by us.
    fields = ['bio', 'profile_pic', 'website_url', 'faceboook_url', 'twitter_url', 'instagram_url', 'pinterest_url']
    success_url = "user_profile/???pk???"

    def get_success_url(self, **kwargs):
        #to get the sucess url this method is used and with url user-profile, pk of the user is sent and a succesfull message is sent also to the user_profile page
        return reverse("user_profile", kwargs={'pk': self.object.pk})

    success_message = "Your profile updated."


def favorite_list(request):
    favorites = Entry.objects.filter(favorites=request.user)
    context = {'favorites': favorites}
    #this method returns the favorites of the that user and displays it in favroite_list.html
    return render(request, 'users/favorite_list.html', context)

#Nursena Karakulah --------