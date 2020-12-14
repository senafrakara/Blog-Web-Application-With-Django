from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

from . import views
from .views import HomeView, EntryView, CreateEntryView, comment_delete, delete_entry, EditEntryView, Likeview, \
    FavoriteView

urlpatterns = [
                  path('', HomeView.as_view(), name='blog-home'),
                  path('entry/<int:pk>/', EntryView, name='entry-detail'),
                  path('create_entry/', CreateEntryView.as_view(success_url='/'), name='create_entry'),
                  path('delete-comment/<int:pk>', comment_delete, name='delete-comment'),
                  path('delete-entry/<int:pk>', delete_entry, name='delete-entry'),
                  path('entry/<int:pk>/edit/', EditEntryView.as_view(), name='entry-edit'),
                  path('like/<int:pk>', Likeview, name='like_entry'),
                  path('favorite/<int:pk>', FavoriteView, name='favorite_entry'),
                  path('search/', views.search, name='search'),
                  path('aboutus/', views.aboutus, name='aboutus'),
                  path('contactus/', views.contactus, name='contactus'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
