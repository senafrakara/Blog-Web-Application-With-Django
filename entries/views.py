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


# Create your views here.


class HomeView(ListView):
    model = Entry
    template_name = 'entries/index.html'
    context_object_name = "blog_entries"
    ordering = ['-entry_date']
    paginate_by = 9


@login_required()
def Likeview(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    liked = False
    if entry.likes.filter(pk=request.user.pk).exists():
        entry.likes.remove(request.user)
    else:
        entry.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('entry-detail', args=[str(pk)]))


def EntryView(request, pk):
    try:
        #   entry_commented = Entry.objects.get(pk=pk)
        entry_commented = get_object_or_404(Entry, pk=pk)
        comments = entry_commented.comments.filter(active=True)

    except Entry.DoesNotExist:
        raise Http404('Data does not exist')
    new_comment = None
    comment_user = request.user

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment = Comment(commenter=comment_user,
                                  comment_content=form.cleaned_data['comment_content'],
                                  entry=entry_commented)
            new_comment.save()

        #    return redirect(request.path)
    else:
        form = CommentForm()
    total_likes = entry_commented.total_likes()

    liked = False
    if entry_commented.likes.filter(pk=request.user.pk).exists():
        liked = True

    favorite = False
    if entry_commented.favorites.filter(pk=request.user.pk).exists():
        favorite = True

    context = {
        'entry': entry_commented,
        'comment_form': form,
        'new_comment': new_comment,
        'comments': comments,
        'total_likes': total_likes,
        'liked': liked,
        'favorite': favorite,
    }
    return render(request, 'entries/entry_detail.html', context)


class CreateEntryView(LoginRequiredMixin, CreateView, ModelForm):
    model = Entry
    template_name = 'entries/create_entry.html'
    fields = ['entry_title', 'entry_text', 'image']

    def form_valid(self, form):
        form.instance.entry_author = self.request.user
        # we set the author equal to the logged in user
        return super().form_valid(form)


@login_required()
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    deleted_comment = None
    urll = comment.entry.pk
    if request.method == 'POST':
        deleted_comment = comment.delete()
        # entry_url = f'entry/{urll}'
        # return render(request, entry_url, context={'deleted_comment':deleted_comment})

    return redirect(f'/entry/{urll}')


@login_required()
def delete_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)

    if request.method == 'POST':
        entry.image.delete()
        entry.delete()
        return redirect('/')


class EditEntryView(SuccessMessageMixin, generic.UpdateView, ModelForm):
    model = Entry
    template_name = 'entries/entry_edit.html'
    fields = ['entry_title', 'entry_text', 'image']
    # template_name_suffix = '_update_form'
    success_url = "entry_detail/???pk???"

    def get_success_url(self, **kwargs):
        return reverse("entry-detail", kwargs={'pk': self.object.pk})

    success_message = "Your entry updated."


@login_required()
def FavoriteView(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    favorite = False
    if entry.favorites.filter(id=request.user.id).exists():
        entry.favorites.remove(request.user)
    else:
        entry.favorites.add(request.user)
        favorite = True

    return HttpResponseRedirect(reverse('entry-detail', args=[str(pk)]))


def search(request):
    status = None
    if request.method == 'GET':
        name = request.GET.get('search')
        try:
            status = Entry.objects.all().filter(
                Q(entry_title__icontains=name) |
                Q(entry_author__username__icontains=name)
            )
            return render(request, 'entries/index.html', {'blog_entries': status})
        except:
            return render(request, "entries/index.html", {'blog_entries': status})
    else:
        return render(request, 'entries/index.html', {})


def aboutus(request):
    return render(request, 'entries/aboutus.html', {})


def contactus(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
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
