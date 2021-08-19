from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('home', views.home),
    path('add_book', views.add_book),
    path('details/<int:book_id>', views.details),
    path('edit/<int:book_id>', views.edit),
    path('favorite/<int:book_id>', views.favorite),
    path('unfavorite/<int:book_id>', views.unfavorite),
    path('unfavorite/again/<int:book_id>', views.unfavorite_again),
    path('logout', views.logout),
    path('delete/<int:book_id>', views.delete)
]