from django.urls import path, include
from . import views

app_name = 'encyclo'

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.content, name="content"),
    path("encyclopedia/new.html", views.new, name="new"),
    path("encyclopedia/edit.html", views.edit, name="edit"),
    path("encyclopedia/save", views.save, name="save"),
    path("encyclopedia/random", views.rand, name="random")
]
