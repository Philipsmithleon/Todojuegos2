# views.py
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .models import  Juego
from .forms import JuegoForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import Http404
import logging
from django.contrib.auth.models import User
from .models import Carrito, CarritoJuegos
from django.http import HttpResponse
from django.core.mail import send_mail

logger = logging.getLogger(__name__)
# Página principal (index)
def index(request):
    return render(request, 'juegos/index.html')

# Registro
def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'juegos/registro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return render(request, 'juegos/registro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'juegos/registro.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        auth_login(request, user)
        messages.success(request, '¡Registro exitoso!')

        return redirect('index')

    return render(request, 'juegos/registro.html')


def ver_juegos_por_categoria(request, categoria):
    try:
        categoria_id = int(categoria)
        juegos = Juego.objects.filter(categoria=categoria_id)
        if not juegos.exists():
            raise Http404("No hay juegos en esta categoría")
        return render(request, 'juegos/ver_juegos_categoria.html', {'categoria_id': categoria_id, 'juegos': juegos})
    except ValueError:
        raise Http404("Categoría inválida")

# Detalle
def detalles_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    return render(request, 'juegos/detalle.html', {'juego': juego})

@user_passes_test(lambda u: u.is_superuser)
def crear_juego(request):
    if request.method == 'POST':
        form = JuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = JuegoForm()
    return render(request, 'juegos/crear_juego.html', {'form': form})

@staff_member_required
def editar_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    if request.method == 'POST':
        form = JuegoForm(request.POST, request.FILES, instance=juego)
        if form.is_valid():
            form.save()
            return redirect('ver_juegos_por_categoria', categoria=juego.categoria)
    else:
        form = JuegoForm(instance=juego)
    return render(request, 'juegos/editar_juego.html', {'form': form, 'juego': juego})

@staff_member_required
def eliminar_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    if request.method == 'POST':
        juego.delete()
        return redirect('ver_juegos_por_categoria', categoria=juego.categoria)
    return render(request, 'juegos/eliminar_juego.html', {'juego': juego})

@login_required
def perfil_usuario(request):
    usuarios = User.objects.all() if request.user.is_superuser else None
    return render(request, 'juegos/perfil.html', {'user': request.user, 'usuarios': usuarios})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.is_superuser:
                return redirect('admin:index')
            else:
                return redirect('index')
        else:
            messages.error(request, "Credenciales incorrectas. Por favor, intente de nuevo.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'juegos/login.html', {'form': form})

@login_required
def agregar_al_carrito(request, producto_id):
    # Obtener el producto o devolver un error 404 si no existe
    producto = get_object_or_404(Juego, id=producto_id)
    
    # Convertir el producto_id a cadena, ya que las claves en la sesión son strings
    producto_id_str = str(producto_id)
    
    # Obtener el carrito de la sesión, si no existe, inicializarlo como un diccionario vacío
    carrito = request.session.get('carrito', {})
    
    # Si el producto ya está en el carrito, incrementar la cantidad
    if producto_id_str in carrito:
        carrito[producto_id_str]['cantidad'] += 1
        carrito[producto_id_str] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': carrito[producto_id_str]['cantidad'],
            'total': float(producto.precio) * carrito[producto_id_str]['cantidad'],
        }
    else:
        # Agregar el producto al carrito con la cantidad inicial de 1
        carrito[producto_id_str] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': 1,
            'total': float(producto.precio),
        }
    
    # Guardar el carrito en la sesión
    request.session['carrito'] = carrito
    
    ultima_pagina = request.session.get('last_visited', 'index')
    return redirect(ultima_pagina)

def ultima_pagina(request):
    ultima_pagina = request.session.get('last_visited', 'index')  # Usa una URL absoluta por defecto
    return redirect(ultima_pagina)
    
def enviar_correo_prueba(request, correo):
    send_mail(
        'Prueba de correo',  # Asunto
        'Este es un correo de prueba.',  # Cuerpo del mensaje
        'testingdjango1x@gmail.com',  # Correo remitente
        [correo],  # Correo del destinatario
        fail_silently=False,
    )
    return HttpResponse('Correo enviado con éxito')

@login_required
def ver_carrito(request):
    # Obtener el carrito de la sesión, si no existe, inicializarlo como un diccionario vacío
    carrito = request.session.get('carrito', {})
    
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())  # Calcular el total
    
    return render(request, 'juegos/ver_carrito.html', {'carrito': carrito, 'total': total})

@login_required
def eliminar_del_carrito(request, producto_id):
    # Convertir el producto_id a cadena
    producto_id_str = str(producto_id)
    
    # Obtener el carrito de la sesión
    carrito = request.session.get('carrito', {})
    
    # Si el producto está en el carrito, eliminarlo
    if producto_id_str in carrito:
        del carrito[producto_id_str]
    
    # Actualizar el carrito en la sesión
    request.session['carrito'] = carrito
    
    return redirect('ver_carrito')

@login_required
def vaciar_carrito(request):
    request.session['carrito'] = {}  # Vaciar el carrito en la sesión
    return redirect('ver_carrito')