from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.forms import ModelForm
from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CommentForm, ContactForm
from .models import Entry, Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import *
from django.http import HttpResponseRedirect


# Nursena Karakulah -----------------------------------------
class HomeView(ListView):
    model = Entry
    template_name = 'entries/index.html'
    context_object_name = "blog_entries"
    ordering = ['-entry_date']
    paginate_by = 9
    # page is paginated with 9, after 9 entry second page is created and continue so on


@login_required()
def Likeview(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    # pk is sent to this func and func gets entry with this pk, if there is no such entry returns 404
    liked = False
    if entry.likes.filter(pk=request.user.pk).exists():
        # if request user is in likes of this entry, then when user clicked unlike button, user is removed from likes list of entry
        entry.likes.remove(request.user)
    else:
        # otherwise user is added into likes of entry
        entry.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('entry-detail', args=[str(pk)]))


def EntryView(request, pk):
    try:
        entry_commented = get_object_or_404(Entry, pk=pk)
        comments = entry_commented.comments.filter(active=True)

    except Entry.DoesNotExist:
        raise Http404('Data does not exist')
    new_comment = None
    comment_user = request.user

    if request.method == 'POST':
        # if form is completed and clicked on comment button, then form is created with info of fields, new comment created and saved into database
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment = Comment(commenter=comment_user,
                                  comment_content=form.cleaned_data['comment_content'],
                                  entry=entry_commented)
            new_comment.save()

        #    return redirect(request.path)
    else:
        # otherwise emtpy comment form is created
        form = CommentForm()
    total_likes = entry_commented.total_likes()
    # to get total likes of entry

    liked = False
    if entry_commented.likes.filter(pk=request.user.pk).exists():
        liked = True
        # if user is liked this entry and send this info to the view as content

    favorite = False
    if entry_commented.favorites.filter(pk=request.user.pk).exists():
        favorite = True
        # if user is added into favorite list this entry,and send this info to the view as content

    context = {
        'entry': entry_commented,
        'comment_form': form,
        'new_comment': new_comment,
        'comments': comments,
        'total_likes': total_likes,
        'liked': liked,
        'favorite': favorite,
    }
    # context is a dictionary and saves all info of that view inside
    return render(request, 'entries/entry_detail.html', context)


class CreateEntryView(LoginRequiredMixin, CreateView, ModelForm):
    model = Entry
    template_name = 'entries/create_entry.html'
    fields = ['entry_title', 'entry_text', 'image']

    # we set the fields of the create entry form by using django createview, we extends it. Also this view is required authenticated user, LoginRequiredMixin provide this checking

    def form_valid(self, form):
        form.instance.entry_author = self.request.user
        # we set the author equal to the logged in user
        return super().form_valid(form)


@login_required()
def delete_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    # get the entry with pk which is sent to the this function
    if request.method == 'POST':
        # When user clicked on delete entry button, a modal displayed. If user clickec on delete button on that model, firstly image of the entry is deleted and then entry is deleted. User directed to the homepage.
        entry.image.delete()
        entry.delete()
        return redirect('/')


class EditEntryView(SuccessMessageMixin, generic.UpdateView, ModelForm):
    model = Entry
    template_name = 'entries/entry_edit.html'
    fields = ['entry_title', 'entry_text', 'image']
    # edit entry form fields are set
    success_url = "entry_detail/???pk???"

    def get_success_url(self, **kwargs):
        # returns success url when an entry is editted
        return reverse("entry-detail", kwargs={'pk': self.object.pk})

    success_message = "Your entry updated."
    # succes message is sent to the success url, entry detail page if entry is editted.


@login_required()
def FavoriteView(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    favorite = False
    # same logic with like entry. if user is favorited to thie entry then if it is clicked remove button, user is removed from favorites list of that entry
    if entry.favorites.filter(id=request.user.id).exists():
        entry.favorites.remove(request.user)
    else:
        # otherwise user is added into favorites list
        entry.favorites.add(request.user)
        favorite = True

    return HttpResponseRedirect(reverse('entry-detail', args=[str(pk)]))


def search(request):
    status = None
    if request.method == 'GET':
        name = request.GET.get('search')
        # gets the query, text of search
        try:
            status = Entry.objects.all().filter(
                Q(entry_title__icontains=name) |
                Q(entry_author__username__icontains=name)
            )
            # checks if query contains entry title or entry author and returns results in index.html with context called blog_entries
            return render(request, 'entries/index.html', {'blog_entries': status})
        except:
            return render(request, "entries/index.html", {'blog_entries': status})
    else:
        # if result is empty then returns empty page
        return render(request, 'entries/index.html', {})


# Nursena Karakulah -----------------------------------------


# Kübra Felek
def aboutus(request):
    return render(request, 'entries/aboutus.html', {})


def contactus(request):
    if request.method == 'GET':
        form = ContactForm()
        # creates empty contact form
    else:
        form = ContactForm(request.POST)
        # if user is completed the form and clicked add comment button, it creates a comment with data coming from user and displays the message comes from user in console
        if form.is_valid():
            username = form.cleaned_data['username']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(username, from_email, message, ['senafrakara@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found. ')
            return render(request, 'entries/contactus.html', {'username': username})
    return render(request, 'entries/contactus.html', {'form': form})


@login_required()
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # takes comment with sent pk

    deleted_comment = None
    urll = comment.entry.pk
    if request.method == 'POST':
        # if method is post then comment deleted. User must be logged in to delete comment
        deleted_comment = comment.delete()

    return redirect(f'/entry/{urll}')
# Kübra Felek
