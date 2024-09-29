from rest_framework import serializers
from .models import Juego, Pedido

class JuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juego
        fields = ['id','nombre', 'categoria', 'precio', 'descripcion','imagen']
        
class PedidoSerializer(serializers.ModelSerializer):
    # El campo 'producto' espera el ID del producto, el campo 'usuario' es de solo lectura
    juego = serializers.PrimaryKeyRelatedField(queryset=Juego.objects.all())
    usuario = serializers.StringRelatedField(read_only=True)  # Solo lectura, representado por el nombre de usuario

    class Meta:
        model = Pedido
        fields = ['id', 'juego', 'cantidad', 'fecha', 'usuario']  # Campos a incluir en la API
        read_only_fields = ['usuario', 'fecha']  # El usuario y la fecha no se envían en el cuerpo de la solicitud

    # Sobrescribimos el método create para asignar automáticamente el usuario autenticado
    def create(self, validated_data):
        # Asignamos el usuario autenticado al pedido
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['usuario'] = request.user

        return super().create(validated_data)