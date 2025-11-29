from django.contrib import admin
from .models import Producto
from django.contrib.auth.models import User # Importamos User para poder crear usuarios de prueba

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """
    Personalización del sitio administrativo para el modelo Producto.
    """
    # Campos que se muestran en la lista de productos
    list_display = ('nombre', 'precio', 'stock', 'fecha_creacion')
    # Campos por los que se puede filtrar
    list_filter = ('fecha_creacion', 'stock')
    # Campos de búsqueda
    search_fields = ('nombre', 'descripcion')
    # Campos de solo lectura
    readonly_fields = ('fecha_creacion',)

    # --- LÓGICA DE PERMISOS PERSONALIZADA ---

    def has_delete_permission(self, request, obj=None):
        """
        Sobrescribe el permiso de eliminación.
        Solo permite eliminar si el usuario es un superusuario.
        """
        # Si el usuario es un superusuario, se le permite eliminar.
        # Esto cumple con el requisito de "solo el administrador pueda eliminar".
        if request.user.is_superuser:
            return True
        # Para todos los demás usuarios (incluyendo Administradores y Gestores de Grupos),
        # se respeta el permiso normal asignado por Django (que asumimos será False para eliminar).
        return super().has_delete_permission(request, obj)

    def get_actions(self, request):
        """
        Si el usuario no es superusuario, elimina la acción masiva de 'delete_selected'.
        """
        actions = super().get_actions(request)
        # Si el usuario NO es superusuario, eliminamos la opción de eliminación masiva
        if not request.user.is_superuser and 'delete_selected' in actions:
            del actions['delete_selected']
        return actions