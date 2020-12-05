from django.forms import ModelForm
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CommentForm
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
    paginate_by = 3


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


# def UnLikeview(request, pk):
#     entry = get_object_or_404(Entry, pk=pk)
#     entry.likes.remove(request.user)
#     return HttpResponseRedirect(reverse('entry-detail', args=[str(pk)]))


# @login_required
# def delete_own_comment(request, message_id):
#     comment = get_object_or_404(Comment.get_model(), pk=message_id,
#             site__pk=settings.SITE_ID)
#     if comment.user == request.user:
#         comment.is_removed = True
#         comment.save()
# # LoginRequiredMixin parametre olarak vardı buna ve homeview a
# class EntryView(DetailView):
#     model = Entry
#     template_name = 'entries/entry_detail.html'

# def post_detail(request, slug):
#     template_name = 'post_detail.html'
#     post = get_object_or_404(Post, slug=slug)
#     comments = post.comments.filter(active=True)
#     new_comment = None
#     # Comment posted
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             # Create Comment object but don't save to database yet
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.post = post
#             # Save the comment to the database
#             new_comment.save()
#     else:
#         comment_form = CommentForm()
#
#     return render(request, template_name, {'post': post,
#                                            'comments': comments,
#                                            'new_comment': new_comment,
#                                            'comment_form': comment_form})
# class EntryView(DetailView):
#     model = Entry
#     template_name = 'entries/entry_detail.html'


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
    context = {
        'entry': entry_commented,
        'comment_form': form,
        'new_comment': new_comment,
        'comments': comments,
        'total_likes': total_likes,
        'liked': liked
    }
    return render(request, 'entries/entry_detail.html', context)


class CreateEntryView(LoginRequiredMixin, CreateView, ModelForm):
    model = Entry
    template_name = 'entries/create_entry.html'
    fields = ['entry_title', 'entry_text', 'image']

    # fields = ['entry_title', 'entry_text_1', 'entry_text_2', 'image_title', 'image_two']

    def form_valid(self, form):
        form.instance.entry_author = self.request.user
        # we set the author equal to the logged in user
        return super().form_valid(form)


#
# class OwnerProtectMixin(object):
#     def dispatch(self, request, *args, **kwargs):
#         objectUser = self.get_object()
#         if objectUser.commenter != self.request.user:
#             return HttpResponseForbidden()
#         return super(OwnerProtectMixin, self).dispatch(request, *args, **kwargs)
#
#
# @method_decorator(login_required, name='dispatch')
# class CommentDeleteView(OwnerProtectMixin, DeleteView):
#     model = Comment


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


# @login_required()
# def entry_delete(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     deleted_comment= None
#     urll = comment.entry.pk
#     if request.method == 'POST':
#         deleted_comment = comment.delete()
#         # entry_url = f'entry/{urll}'
#         # return render(request, entry_url, context={'deleted_comment':deleted_comment})
#
#     return redirect(f'/entry/{urll}')


@login_required()
def delete_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)

    if request.method == 'POST':
        entry.image.delete()
        entry.delete()
        return redirect('/')


# def entry_edit(request, pk):
#     entry = get_object_or_404(Entry, pk=pk)
#     if request.method == 'POST':
#         form = CreateEntryView(request.POST, instance=entry)
#         if form.is_valid():
#             entry = form.save(commit=False)
#             entry.save()
#             return redirect('entry-detail', pk=entry.pk)
#     else:
#         form = CreateEntryView(instance=entry)
#
#         return render(request, 'entries/entry_edit.html', {'form': form})
#
#


class EditEntryView(LoginRequiredMixin, UpdateView, ModelForm):
    model = Entry
    template_name = 'entries/entry_edit.html'
    fields = ['entry_title', 'entry_text', 'image']
