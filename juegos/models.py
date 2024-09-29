from django.db import models
from django.contrib.auth.models import User


class Juego(models.Model):
    CATEGORIAS = [
        (1, 'Terror'),
        (2, 'Acción'),
        (3, 'Carreras'),
        (4, 'Deportes'),
        (5, 'Supervivencia'),
        (6, 'Mundo Abierto'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='juegos/')
    categoria = models.IntegerField(choices=CATEGORIAS)

    def __str__(self):
        return self.nombre
    
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
    
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    juegos = models.ManyToManyField(Juego, through='CarritoJuegos')
    
    def __str__(self):
        return f'Carrito de {self.usuario.username}'

class CarritoJuegos(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.cantidad} x {self.juego.nombre}'
    
class Pedido(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    
    cantidad = models.IntegerField(default=1)

    fecha = models.DateTimeField(auto_now_add=True)
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Pedido {self.id} - {self.juego.nombre} por {self.usuario.username}"
    
class Descuento(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'Código: {self.codigo} - {self.porcentaje}%'
    
    def es_valido(self):
        from django.utils import timezone
        ahora = timezone.now()
        return self.activo and self.fecha_inicio <= ahora <= self.fecha_fin