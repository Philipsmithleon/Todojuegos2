from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomLogoutView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import JuegoViewSet, PedidoViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Creamos un router que se encargará de las rutas de los ViewSets
router = DefaultRouter()
router.register(r'juegos', JuegoViewSet)  # Registrar el ViewSet de Producto
router.register(r'pedidos', PedidoViewSet)

urlpatterns = [
    path('', views.index, name='home'),
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('categoria/<int:categoria>/', views.ver_juegos_por_categoria, name='ver_juegos_por_categoria'),
    path('juego/<int:juego_id>/', views.detalles_juego, name='detalles_juego'),
    path('crear_juego/', views.crear_juego, name='crear_juego'),
    path('editar_juego/<int:juego_id>/', views.editar_juego, name='editar_juego'),
    path('eliminar_juego/<int:juego_id>/', views.eliminar_juego, name='eliminar_juego'),
    path('login/', views.login_view, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='juegos/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='juegos/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='juegos/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='juegos/password_reset_complete.html'), name='password_reset_complete'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('redirigir/', views.ultima_pagina, name='ultima_pagina'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),  # Incluir las rutas del router en la URL base 'api/'
    path('pedidos/', views.ListaPedidosView.as_view(), name='lista_pedidos'),
    path('pedidos/crear/', views.CrearPedidoView.as_view(), name='crear_pedido'),
    path('pedidos/editar/<int:pk>/', views.EditarPedidoView.as_view(), name='editar_pedido'),
    path('pedidos/eliminar/<int:pk>/', views.EliminarPedidoView.as_view(), name='eliminar_pedido'),
    path('chiste/', views.ChisteView.as_view(), name='chiste'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
