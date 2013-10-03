# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from crosser_frontend.models import Scheme
from crosser_frontend.tasks import process_scheme

import sys

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
        form = UserCreationForm(initial={'username': 'UserName'})
        return render(request, 'crosser_frontend/signup.html', {'form' : form,})

def process(request, id): 
    scheme = Scheme.objects.get(pk=id)
    
    calc = scheme.freeze()
    result = process_scheme.delay(calc.id)
    calc.task_id = result.task_id
    calc.save()
    return redirect('calc', calc.id)
