from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages

def gestionar_usuarios(request):
    users = User.objects.all()  # Obtener todos los usuarios
    return render(request, 'lista_usuarios.html', {'users': users})

def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'Usuario eliminado con éxito.')
    return redirect('gestionar_usuarios')  # Redirigir a la vista de gestión de usuarios
