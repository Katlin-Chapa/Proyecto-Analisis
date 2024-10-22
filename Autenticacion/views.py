from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect


# Create your views here.
class UsuarioInicioVista(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        # Si el usuario ya está autenticado, redirigir a la página de sesión
        if request.user.is_authenticated:
            return redirect('sesion')  # Cambia 'sesion' por el nombre de tu URL de sesión
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class InicioPersonalizado(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
