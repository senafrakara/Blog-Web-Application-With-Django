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
    likes = models.ManyToManyField(User, related_name='blog_entries')
    # entry_title = models.CharField(max_length=50)
    # entry_text_1 = models.TextField()
    # entry_text_2 = models.TextField()
    # entry_date = models.DateTimeField(
    #     auto_now_add=True)
    # # this will automatically take and time when the entry is created
    # entry_author = models.ForeignKey(User,
    #                                  on_delete=models.CASCADE)
    # image_title = models.ImageField(upload_to='images/', default='default-title-img.png')
    # image_two = models.ImageField(upload_to='images/', null=True, blank=True)

    # second arg is the on_delete argument which defines what happens when an object reference is deleted
    # so we'll yse model cascade which would not leave all the posts associated with a user
    # if that user is deleted from the system
    class Meta:
        verbose_name_plural = "Entries"

    def __str__(self):
        # bu metotla birlikte admin tarafında işleri biraz daha kolaylaştırmak
        # için entry nin title ını isim olarak döndüreceğiz.
        # Entry object (1) değil de entrynin title ı neyse onu gösterecek
        return self.entry_title + '|' + str(self.entry_author)

    def get_absolute_url(self):
        return reverse('entry-detail', args=[str(self.pk)])

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='comments')
    comment_content = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.comment_content} by {self.commenter}'
