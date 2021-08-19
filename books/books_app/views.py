from django.shortcuts import render, redirect
from .models import User, Book
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashedpassword = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hashedpassword)
        new_user = User.objects.create(
            fname = request.POST['fname'],
            lname = request.POST['lname'],
            email = request.POST['email'],
            password = hashedpassword
        )
    request.session['user_id'] = new_user.id
    return redirect('/home')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['logemail'])
        request.session['user_id'] = user.id
        return redirect('/home')

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        "users": user,
        "books": Book.objects.all()
    }
    return render(request, 'home.html', context)

def add_book(request):
    uploaded_by = User.objects.get(id=request.session['user_id'])
    errors = Book.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/home')
    else:
        new_book = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            uploaded_by = uploaded_by,
        )
    new_book.users_who_like.add(uploaded_by)
    return redirect('/home')

def details(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    context = {
        "book": book,
        "user": user,
    }
    return render(request, 'details.html', context)

def edit(request, book_id):
    errors = Book.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect(f'/details/{book_id}')
    else:
        edit = Book.objects.get(id=book_id)
        edit.title = request.POST['title']
        edit.desc = request.POST['desc']
        edit.save()
    return redirect('/home')

def delete(request, book_id):
    delete = Book.objects.get(id=book_id)
    delete.delete()
    return redirect('/home')

def favorite(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    book.users_who_like.add(user)
    return redirect(f'/details/{book_id}')

def unfavorite(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    book.users_who_like.remove(user)
    return redirect('/home')

def unfavorite_again(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    book.users_who_like.remove(user)
    return redirect(f'/details/{book_id}')

def logout(request):
    request.session.clear()
    return redirect('/')
# Create your views here.
