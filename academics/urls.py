from django.urls import path
from . import views

urlpatterns = [
    path('subjects/', views.subjects_by_scheme_semester, name='subjects_by_scheme_semester'),
    path('subjects/create/', views.create_subject, name='create_subject'),
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/upload/', views.upload_note, name='upload_note'),
    path('notes/approve/', views.approve_note, name='approve_note'),
    path('notes/my/', views.my_notes, name='my_notes'),
    path('notes/<int:pk>/delete/', views.delete_note, name='delete_note'),
    path('notes/pending/', views.pending_notes, name='pending_notes'),
]
