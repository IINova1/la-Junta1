from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from datetime import date, timedelta
# --- IMPORTACIONES PARA GRÁFICOS Y AGREGACIÓN ---
from django.db.models import F, Sum
from django.db.models.functions import TruncDate
import json

# Importación de modelos
from usuarios.models import Usuario
from catalogo.models import Producto
from pedidos.models import Pedido, Cliente
from proveedores.models import Proveedor
from .models import ContadorVisitas

# --------------------
# Vistas Públicas (Para todos)
# --------------------

def inicio(request):
    """
    Vista para la página de inicio pública.
    """
    contador, _ = ContadorVisitas.objects.get_or_create(nombre='sitio')
    es_visitante_nuevo = not request.session.get('visito_la_junta')

    ContadorVisitas.objects.filter(pk=contador.pk).update(
        total_visitas=F('total_visitas') + 1,
        visitantes_unicos=F('visitantes_unicos') + (1 if es_visitante_nuevo else 0),
    )

    if es_visitante_nuevo:
        request.session['visito_la_junta'] = True

    contador.refresh_from_db()
    context = {
        'visitas': contador.total_visitas
    }
    return render(request, 'core/inicio.html', context)


# ----------------------------------------
# Vistas Protegidas (SOLO PARA ADMINS)
# ----------------------------------------

@login_required
@permission_required('catalogo.view_producto', raise_exception=True)
def dashboard(request):
    # 1. Contadores Generales
    total_usuarios = Usuario.objects.count()
    total_productos = Producto.objects.count()
    total_clientes = Cliente.objects.count()
    total_proveedores = Proveedor.objects.count()
    total_pedidos_pendientes = Pedido.objects.filter(estado='Pendiente').count()
    contador_visitas, _ = ContadorVisitas.objects.get_or_create(nombre='sitio')
    
    # 2. Productos por vencer (Lógica existente)
    hoy = date.today()
    fecha_limite = hoy + timedelta(days=7)
    productos_a_vencer = Producto.objects.filter(
        caducidad__gte=hoy, 
        caducidad__lte=fecha_limite
    ).order_by('caducidad')
    
    # 3. LÓGICA PARA EL GRÁFICO DE VENTAS (Últimos 30 días)
    fecha_inicio_grafico = hoy - timedelta(days=30)
    
    # Agrupamos por día y sumamos el 'total'
    # Excluimos los cancelados para que la gráfica sea positiva
    ventas_por_fecha = Pedido.objects.filter(
        fecha_pedido__date__gte=fecha_inicio_grafico
    ).exclude(estado='Cancelado') \
     .annotate(fecha=TruncDate('fecha_pedido')) \
     .values('fecha') \
     .annotate(suma_total=Sum('total')) \
     .order_by('fecha')

    # Preparamos los datos para Chart.js (listas simples)
    fechas_grafico = []
    montos_grafico = []

    for registro in ventas_por_fecha:
        # Formato día/mes (ej: 12/10)
        fechas_grafico.append(registro['fecha'].strftime("%d/%m"))
        # Convertimos Decimal a float para que JS lo entienda
        montos_grafico.append(float(registro['suma_total']))

    context = {
        'total_usuarios': total_usuarios,
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_proveedores': total_proveedores,
        'total_pedidos_pendientes': total_pedidos_pendientes,
        'total_visitas': contador_visitas.total_visitas,
        'visitantes_unicos': contador_visitas.visitantes_unicos,
        'productos_a_vencer': productos_a_vencer,
        
        # Datos para el gráfico (convertidos a JSON string para seguridad en JS)
        'fechas_grafico': json.dumps(fechas_grafico),
        'montos_grafico': json.dumps(montos_grafico),
    }
    
    return render(request, 'core/dashboard.html', context)
