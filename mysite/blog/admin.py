from django.contrib import admin
from .models import Post

# Register your models here.

# admin.site.register(Post) #Aqui hay quye registar todos nuetsros modelos para que django pueda encontrarlos
@admin.register(Post) #ESta es la forma moderna de registar modelos
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status'] #efine qué campos del modelo Post se mostrarán en la lista de elementos del panel de administración
    list_filter = ['status', 'created', 'publish', 'author'] #Agregar filtros en el panel de administracion 
    search_fields = ['title', 'body'] #Define los campos que se utilizan para la busqueda
    prepopulated_fields = {'slug': ('title',)} # permite prellenar automaticamente ciertos campos basados en otros campos
    raw_id_fields = ['author'] #Esta propiedad cambia la forma en que se representan los campos relacionados en el panel de administración, es decir, se ve el id del autor ahora
    date_hierarchy = 'publish' # Esta propiedad especifica que se debe agregar una jerarquía de fechas en la barra lateral del panel de administración
    ordering = ['status', 'publish'] # define el orden en el que se mostrarán los elementos en el panel de administración