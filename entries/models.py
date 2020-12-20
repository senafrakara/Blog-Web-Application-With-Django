from django.db import models
from django.contrib.auth.models import User  # this is the django's authentication system

# Create your models here.
from django.urls import reverse


class Entry(models.Model):
    entry_title = models.CharField(max_length=50)
    entry_text = models.TextField()
    entry_date = models.DateTimeField(
        auto_now_add=True)
    # this will automatically take and time when the entry is created
    entry_author = models.ForeignKey(User,
                                     on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/',
                              blank=False)  # default image url is deleted because image field made required by the way
    likes = models.ManyToManyField(User, related_name='blog_entries', blank=True, null=True)
    favorites = models.ManyToManyField(User, related_name='entry_favorites', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Entries"

    def __str__(self):
        #this returns as string entry title and entry author instead of return object(1)
        return self.entry_title + '|' + str(self.entry_author)

    def get_absolute_url(self):
        #returns entry pk to get url like entry_detail/3
        return reverse('entry-detail', args=[str(self.pk)])

    def total_likes(self):
        #takes like count of that entry
        return self.likes.count()


class Profile(models.Model):
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='images/', blank=True, null=True)
    website_url = models.CharField(max_length=255, null=True, blank=True)
    faceboook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    pinterest_url = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='comments')
    comment_content = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']
        #order comments according to the reverse created date

    def __str__(self):
        #returns  comment content and commenter
        return f'{self.comment_content} by {self.commenter}'
