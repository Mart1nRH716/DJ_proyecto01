from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm #Asi se importan las cosas
# Create your views here.

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3 #YA implementa la paginacion por defecto
    template_name = 'blog/post/list.html'
    
    #####Esto es equivalente a lo de abajo########
def post_list(request):
    post_list = Post.published.all() #Este es el administrador que definimos
    paginator = Paginator(post_list, 5) # Pagination con 3 posts por pagina, recibe la funcion 
    page_number = request.GET.get('page', 1) #El numero de paginacion por parametro si no llega nada, lo mandamos al inicio
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request,'blog/post/list.html',{'posts': posts}) # renderizar plantillas HTML con datos dinámicos

def post_detail(request, year, month, day, post):
    
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day)
    return render(request,'blog/post/detail.html',{'post': post}) #Aqui todas entran al directorio templates/blog/post y asi nos vamos


def post_share(request, post_id):
    # Obtener el objeto Post con el id dado, o devolver un error 404 si no existe
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    
    # Verificar si la solicitud es de tipo POST
    if request.method == 'POST':
        # Si es una solicitud POST, inicializar el formulario con los datos de la solicitud
        form = EmailPostForm(request.POST)
        
        # Verificar si el formulario es válido
        if form.is_valid():
            # Si el formulario es válido, obtener los datos limpios del formulario
            cd = form.cleaned_data #guardamos los datos 
    else:
        # Si la solicitud no es de tipo POST, mandamos el formulario vacio
        form = EmailPostForm() 
    # Renderizar la plantilla 'blog/post/share.html' con el objeto Post y el formulario
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})

 