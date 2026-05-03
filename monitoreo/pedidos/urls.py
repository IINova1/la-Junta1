from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    # --- URLs para el Carrito de Compras ---
    path('tienda/', views.ver_productos, name='ver_productos'),
    path('carrito/agregar/<int:pk>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('pedido/realizar/', views.realizar_pedido, name='realizar_pedido'),
    path('pedido/exitoso/', views.pedido_exitoso, name='pedido_exitoso'),
    path('exportar_excel/', views.exportar_pedidos_excel, name='exportar_pedidos_excel'),
    
    # --- URLs de Admin para Pedidos ---
    path('pedidos/', views.pedido_list, name='pedido_list'),
    path('pedidos/<int:pk>/cambiar_estado/', views.pedido_update_status, name='pedido_update_status'),
    path('pedidos/<int:pk>/', views.pedido_detail, name='pedido_detail'),

    # --- URLs de Admin para Cliente ---
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/crear/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', views.cliente_delete, name='cliente_delete'),
]