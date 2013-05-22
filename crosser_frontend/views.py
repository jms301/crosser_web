# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #login the user
            user_name = request.POST['username']
            user_pass = request.POST['password1']
            user  = authenticate(username=user_name, password=user_pass)
            if user is not None:
                login(request,user)    
            return HttpResponseRedirect('/')
        return render(request, 'crosser_frontend/signup.html', {'form' : form,})
    else:
        form = UserCreationForm()
        return render(request, 'crosser_frontend/signup.html', {'form' : form,})

