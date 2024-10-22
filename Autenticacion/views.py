from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views import View
from .forms import SupportForm
from django.conf import settings



# Create your views here.
class UsuarioInicioVista(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm

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


class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'  # Nombre de tu plantilla
    email_template_name = 'password_reset_email.html'  # Plantilla del correo electrónico
    subject_template_name = 'password_reset_subject.txt'  # Plantilla del asunto del correo
    success_url = reverse_lazy('password_reset_done')  # Redirige después de enviar el correo


class SupportView(View):
    def get(self, request):
        form = SupportForm()
        return render(request, 'support.html', {'form': form})

    def post(self, request):
        form = SupportForm(request.POST)
        if form.is_valid():
            # Aquí envías el correo usando send_mail
            send_mail(
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['jmunozp7@miumg.edu.gt'],  # Cambia esto por el correo de soporte
            )
            return render(request, 'login.html')  # Cambia a la página que quieras mostrar después
        return render(request, 'support.html', {'form': form})  # Vuelve a mostrar el formulario con errores