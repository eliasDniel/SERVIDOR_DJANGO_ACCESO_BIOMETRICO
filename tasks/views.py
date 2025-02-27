from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.http.response import HttpResponse
from django.db import IntegrityError
from .forms import TasksForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request,'home.html',{
       
    })
def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html',{
       'form':UserCreationForm
    })
    else:
        if request.POST['password1'] ==  request.POST['password2']:
            #register user
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('tasks')
            except IntegrityError:
                return render(request,'signup.html',{
       'form':UserCreationForm,
       'error':'Usuario ya existe'
    })
        return render(request,'signup.html',{
       'form':UserCreationForm,
       'error':'Contraseñas no coinciden'
    })
@login_required
def tasks(request):
    tasks = Task.objects.filter(user = request.user,datecompleted__isnull = True)
    return render(request, 'tasks.html',{'tasks':tasks})
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user = request.user,datecompleted__isnull = False).order_by('-datecompleted')
    return render(request, 'tasks.html',{'tasks':tasks})

@login_required
def complete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
@login_required    
def delete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')  
    
@login_required 
def task_detail(request,task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task,pk=task_id,user=request.user)
        form = TasksForm(instance=task)
        return render(request,'task_detail.html',{'task':task,'form':form})
    else:
        try:
            task = get_object_or_404(Task,pk=task_id,user=request.user)
            form = TasksForm(request.POST,instance=task)
            form.save()
            return redirect('tasks')

        except ValueError:
            return render(request,'task_detail.html',{'task':task,'form':form,'error':'Error al actualizar'})
@login_required
def createTasks(request):
    if request.method == 'GET':
        return render(request,'create_tasks.html',{'form':TasksForm})
    else:
        try:
            form = TasksForm(request.POST)
            new_tasks = form.save(commit=False)
            new_tasks.user = request.user
            new_tasks.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'create_tasks.html',{'form':TasksForm,'error':'Datos Invalidos'})

@login_required
def cerrarSession(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == "GET":
        return render(request,'signin.html',{
        'form':AuthenticationForm
    })
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{
                'form':AuthenticationForm,
                'error':'Username or Password son incorrectos'
                })
        else:
            login(request,user)
            return redirect('tasks')