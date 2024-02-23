from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator
# Create your views here.

def post_list(request):
    post_list = Post.published.all() #Este es el administrador que definimos
    paginator = Paginator(post_list, 5) # Pagination con 3 posts por pagina, recibe la funcion 
    page_number = request.GET.get('page', 1) #El numero de paginacion por parametro si no llega nada, lo mandamos al inicio
    posts = paginator.page(page_number)
    return render(request,'blog/post/list.html',{'posts': posts}) # renderizar plantillas HTML con datos dinámicos

def post_detail(request, year, month, day, post):
    # Se puede hacer asi o
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found.")
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day)
    return render(request,'blog/post/detail.html',{'post': post}) #Aqui todas entran al directorio templates/blog/post y asi nos vamos
