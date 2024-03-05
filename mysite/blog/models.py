from django import forms
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED) #aqui se llama a la clase padre para obtener todos los datos de bd y despues filtramos 




#Creamos el modelo que nos permitira almacenar blogs en la base de datos
class Post(models.Model):
    """
    models.TextChoices: Esta es una clase proporcionada por Django que permite definir un conjunto de opciones para un campo de texto en un modelo. 
    Se utiliza para limitar los valores posibles que puede tener un campo de texto en una base de datos.
    """
    class Status(models.TextChoices):
        #Agregamos la clase para borrador y publicado
        #El valor que se almacena es Df y para no confundirlo, para nosotros se mostrara como Draft
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish') #Este es como un varchar de hecho se traduce en asi en la base de datos
    #El atributyo de unique for date  garantiza que el slug sea único para cada fecha de publicación. Esto significa que dos publicaciones con la misma fecha de publicación no pueden tener el mismo slug
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blog_posts') #Esta VA SER LA relacion muchos a uno e iportamos la clase user ya definida por django
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager() # administrador predeterminado que te permite realizar consultas estándar en todos los objetos de la clase Post.
    published = PublishedManager() # Te dará acceso al administrador personalizado published

    class Meta:
        ordering = ['-publish'] #Esto hara que se ordene de acuerdo al campo publish, el cual es l;a fecha, y lo hara de manera descendente
        indexes = [
             models.Index(fields=['-publish']), #Esto mejorara el renmdimineto agregando indices a este campo
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        #   La funcion reverse construiye la url de manera dinamica, lo que esto hace es esto: <a href="{% url 'blog:post_detail' post.id %}">, \
        #ahora ya nadamas se llama a la funcion
        return reverse('blog:post_detail',args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    
#Una vez termninado se hacen las migraciones

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'



    