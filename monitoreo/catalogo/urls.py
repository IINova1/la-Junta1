from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    # Categorías
    path('', views.categoria_list, name='categoria_list'),
    path('categoria/nuevo/', views.categoria_create, name='categoria_create'),
    path('categoria/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categoria/<int:pk>/eliminar/', views.categoria_delete, name='categoria_delete'),
    path('categoria/exportar/', views.categoria_export_excel, name='categoria_export_excel'),

    # Productos
    path('producto/', views.producto_list, name='producto_list'),
    path('producto/nuevo/', views.producto_create, name='producto_create'),
    path('producto/importar-eleventa/', views.producto_import_eleventa, name='producto_import_eleventa'),
    path('producto/<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('producto/<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),
    path('producto/<int:pk>/', views.producto_detail, name='producto_detail'),
    path('producto/exportar/', views.producto_export_excel, name='producto_export_excel'),
]
