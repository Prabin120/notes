from django.urls import path
from .views import NoteListCreateView, NoteDetailView,NoteSearchView,NoteShare

urlpatterns = [
    path('notes', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:id>', NoteDetailView.as_view(), name='note-detail'),
    path('notes/<int:id>/share', NoteShare.as_view(), name='note-share'),
    path('search', NoteSearchView.as_view(), name='note-search'),
]