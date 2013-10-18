# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test

from crosser_frontend.models import Scheme, Calculation
from crosser_frontend.tasks import process_scheme
#from kombu import Connection as BrokerConnection   
#from django.conf import settings

#import celery.worker.control
import celery 
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

@login_required
def process(request, id): 

    scheme = Scheme.objects.get(pk=id)
    
    calc = scheme.freeze()
    result = process_scheme.delay(calc.id)
    calc.task_id = result.task_id
    calc.save()
    return redirect('calc', calc.id)

@user_passes_test(lambda u: u.is_superuser)
def kill_task(request, id): 
    calc = Calculation.objects.get(pk=id)
    celery.current_app.control.revoke(calc.task_id, terminate=True)
    return redirect('task_admin')

@user_passes_test(lambda u: u.is_superuser)
def task_admin(request): 

    nodes = celery.current_app.control.inspect()
    active = nodes.active() 
    pending = nodes.reserved()
    print(active)
    for key, tasks in active.items():
        for task in tasks: 
            task['id'] = Calculation.objects.get(task_id=task['id'])

    for key, tasks in pending.items():
        for task in tasks: 
            task['id'] = Calculation.objects.get(task_id=task['id'])

    return render(request, 'crosser_frontend/task_admin.html', 
            {'active' : active, 'pending' : pending})
