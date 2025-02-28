from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.http.response import HttpResponse
from django.db import IntegrityError
from .forms import TasksForm,ClienteForm,MembresiaForm
from .models import Task,Cliente,Membresia
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages 
from django.db import models


# Create your views here.

#VISTA HOME
def home(request):
    return render(request,'home.html',{
       
    })
@login_required
def clientes(request):
    clientes = Cliente.objects.all().order_by('id')
    return render(request, 'clientes.html',{'clientes':clientes})
@login_required
def membresias(request):
    membresias = Membresia.objects.all().order_by('id')
    clientes = Cliente.objects.all().order_by('id')
    
    # Calcular la cantidad total
    total_membresias = membresias.count()
    total_clientes = clientes.count()
    
    # Calcular ingresos y egresos
    ingresos = membresias.filter(tipo__in=['VIP', 'Premium', 'Familiar']).aggregate(total=models.Sum('precio'))['total'] or 0
    egresos = membresias.exclude(tipo__in=['VIP', 'Premium', 'Familiar']).aggregate(total=models.Sum('precio'))['total'] or 0

    return render(request, 'membresias.html', {
        'membresias': membresias,
        'clientes': clientes,
        'total_membresias': total_membresias,
        'total_clientes': total_clientes,
        'ingresos': ingresos,
        'egresos': egresos
    })


@login_required
def crear_cliente(request):
    if request.method == 'GET':
        return render(request, 'crear_cliente.html', {'form': ClienteForm})
    else:
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado con éxito.')
            return render(request, 'crear_cliente.html', {
                'form': ClienteForm,
                'redirect_url': reverse('clientes')  # URL a la que redirigir
            })
        else:
            messages.error(request, 'Error al crear el cliente. Revisa los campos.')
            return render(request, 'crear_cliente.html', {'form': form})

@login_required 
def cliente_detail(request,cliente_id):
    if request.method == 'GET':
        cliente = get_object_or_404(Cliente,pk=cliente_id)
        form = ClienteForm(instance=cliente)
        return render(request,'cliente_detail.html',{'cliente':cliente,'form':form})
    else:
    
        cliente = get_object_or_404(Cliente,pk=cliente_id)
        form = ClienteForm(request.POST,instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado con éxito.')
            return render(request, 'cliente_detail.html', {
            'form': ClienteForm,
            'redirect_url': reverse('clientes')  # URL a la que redirigir
        })
        else:
            messages.error(request, 'Datos Invalidos')
            return render(request, 'cliente_detail.html', {
            'form': ClienteForm,
             # URL a la que redirigir
        })
                

@login_required 
def view_cliente(request,cliente_id):
    cliente = get_object_or_404(Cliente,pk=cliente_id)
    return render(request,'view_cliente.html',{'cliente':cliente})

    



@login_required 
def membresia_detail(request,membresia_id):
    if request.method == 'GET':
        membresia = get_object_or_404(Membresia,pk=membresia_id)
        form = MembresiaForm(instance=membresia)
        return render(request,'membresia_detail.html',{'membresia':membresia,'form':form})
    else:
        membresia = get_object_or_404(Membresia,pk=membresia_id)
        form = MembresiaForm(request.POST,instance=membresia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membresia actualizada con éxito.')
            return render(request, 'membresia_detail.html', {
            'form': MembresiaForm,
            'redirect_url': reverse('membresias')  # URL a la que redirigir
        })
        else:
            messages.error(request, 'Membresia actualizada con éxito.')
            return render(request, 'membresia_detail.html', {
            'form': MembresiaForm,
        })

@login_required
def crear_membresia(request):
    if request.method == 'GET':
        return render(request,'crear_membresias.html',{'form':MembresiaForm})
    else:
        form = MembresiaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membresia creada con éxito.')
            return render(request, 'crear_membresias.html', {
                'form': MembresiaForm,
                'redirect_url': reverse('membresias')  # URL a la que redirigir
            })
        else:
            messages.error(request, 'Error al crear la membresia. Revisa los campos.')
            return render(request, 'crear_membresias.html', {'form': form})
    
       
def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html',{
       'form':UserCreationForm
    })
    else:
        if request.POST['password1'] ==  request.POST['password2']:
            user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
            if user is not None:
                user.save()
                login(request,user)
                messages.success(request,f'Usuario {request.user.username} creado exitosamente!!')
                return render(request, 'signup.html', {
                'form': MembresiaForm,
                'redirect_url': reverse('membresias')  # URL a la que redirigir
            })
            else:
                messages.error(request,'Usuario ya existe')
                return render(request,'signup.html',{
       'form':UserCreationForm
    })
        else:
            messages.error(request,'Contraseñas no coinciden')
            return render(request,'signup.html',{
       'form':UserCreationForm
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
def delete_cliente(request,cliente_id):
    cliente = get_object_or_404(Cliente,pk=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes')  


@login_required    
def delete_membresia(request,membresia_id):
    membresia = get_object_or_404(Membresia,pk=membresia_id)
    if request.method == 'POST':
        membresia.delete()
        return redirect('membresias')
    
    
    
    
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
            messages.error(request,'Credenciales incorrectas')
            return render(request,'signin.html',{
                'form':AuthenticationForm,
                
                })
        else:
            login(request,user)
            messages.success(request,f'Bienvenido {request.user.username}')
            return render(request, 'signin.html', {
                'form': MembresiaForm,
                'redirect_url': reverse('membresias')  # URL a la que redirigir
            })