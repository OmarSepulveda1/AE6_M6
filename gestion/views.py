from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Producto
from django.core.exceptions import PermissionDenied

def landing_page(request):
    """
    Renderiza la página de bienvenida.
    """
    return render(request, 'gestion/landing.html')

@staff_member_required
def lista_productos_protegida(request):
    """
    Vista protegida para el personal de la empresa (staff).
    Muestra la lista de todos los productos.
    """
    productos = Producto.objects.all()
    return render(request, 'gestion/lista_productos.html', {'productos': productos})

@staff_member_required
def intentar_eliminar_producto(request, pk):
    """
    Vista que maneja el intento de eliminación de un producto.
    
    - El decorador @staff_member_required asegura que solo el personal del
      sitio administrativo pueda acceder a esta ruta.
    - La lógica interna usa request.user.has_perm para verificar el permiso 'delete'.
    - Si el permiso no existe, se lanza PermissionDenied (error 403).
    """
    # 1. Obtener el producto o lanzar 404 si no existe
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        # 2. Verificar si el usuario tiene permiso para eliminar (gestion.delete_producto)
        # o si es un superusuario.
        if request.user.has_perm('gestion.delete_producto') or request.user.is_superuser:
            # ACCESO CONCEDIDO: El usuario tiene permiso
            producto.delete()
            # Usamos messages para notificar al usuario en el siguiente request
            messages.success(request, f"Producto '{producto.nombre}' eliminado correctamente.")
            # Redirigir al índice del admin (o a la página principal)
            return redirect('/admin/gestion/producto/') 
        else:
            # ACCESO DENEGADO: El usuario NO tiene permiso de eliminación
            # Forzamos un error 403 (Acceso Denegado) explícito.
            raise PermissionDenied("No tienes permiso para eliminar este producto.")

    # 3. Mostrar la página de confirmación (Método GET)
    # Nota: En Django real, usarías render(request, 'gestion/confirmar_eliminar.html', {'producto': producto})
    # Aquí usamos un HttpResponse simple para no depender de templates.
    return HttpResponse(f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h1 style="color: #333;">Confirmar Eliminación</h1>
            <p>¿Estás seguro de que deseas eliminar el producto: <strong>{producto.nombre}</strong>?</p>
            <form method="POST">
                <!-- Token CSRF es NECESARIO para peticiones POST en Django -->
                <input type="hidden" name="csrfmiddlewaretoken" value="{request.COOKIES.get('csrftoken', 'NO_CSRF_TOKEN')}">
                <button type="submit" style="background-color: #dc3545; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer;">Eliminar Producto</button>
            </form>
            <br>
            <a href="/admin/gestion/producto/" style="color: #007bff; text-decoration: none;">Cancelar y Volver al Listado</a>
        </div>
    """)