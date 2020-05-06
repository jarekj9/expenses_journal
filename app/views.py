from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
#for auth:
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate, login
#for registration:
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

import app.main
import datetime


#filter only users, that are members of group
def is_member(user):
    return user.groups.filter(name='accessGroup').exists()

#better form, can use instead of UserCreationForm
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=50)
    last_name = forms.CharField(required=True, max_length=50)

    #Meta inspects the current model of the class User, then ensures that 6 of the fields inside of it are there
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
class NoteForm(forms.Form):
    allcategories = Categories.objects.values_list('id','category')
    date = forms.DateField(initial=datetime.date.today)
    value = forms.FloatField() 
    category = forms.CharField(widget=forms.Select(choices=allcategories))
    description = forms.CharField(max_length=100)

class CategoryForm(forms.Form):
    category = forms.CharField(max_length=100)

def addnote(request):   
    if request.method == "POST":     
        form = NoteForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            value = form.cleaned_data['value']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            note = Journal(login=request.user, date=date, value=value, category=category, description=description)  #Categories.objects.get(id=category)
            note.save()
            return redirect("/")
        else:
            return HttpResponse("Wrong user input")
    else:
        return HttpResponse("No POST request")


def deletenote(request):
    if request.method == "POST":
        id = request.POST.get('id')
        Journal.objects.filter(id=id).delete()
        return redirect("/")
    else:
        return HttpResponse("No POST request")

def addcategory(request):
    form = CategoryForm(request.POST)
    if request.method == "POST":     
        if form.is_valid():
            category = form.cleaned_data['category']
            newcategory = Categories(login=request.user, category=category)
            newcategory.save()
            return redirect("/")
        else:
            return HttpResponse("Wrong user input")
    else:
        return render(request, "journal_add_category.html", {'categoryform':form})

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)   			#can use simpler: UserCreationForm
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("/")

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request = request,
                          template_name = "registration/signup.html",
                          context={"form":form})

    form = UserRegisterForm
    return render(request = request,
                  template_name = "registration/signup.html",
                  context={"form":form})
 
            
def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

    
@login_required
@user_passes_test(is_member)
def index(request):
    noteform = NoteForm()
    all_records = app.main.main()
    
    return render(request, "journal_add_note.html", {"all_records":app.main.main(), 'noteform':noteform, 'message':''})


