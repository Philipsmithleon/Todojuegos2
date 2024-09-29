from django import forms 
from .models import Juego
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from .models import Pedido

class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ['nombre', 'categoria', 'precio', 'descripcion', 'imagen']
        
class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['juego', 'cantidad']


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')

    def post(self, request):
        logout(request)
        return redirect('index')