from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
# Create your views here.

def post_list(request):
    posts = Post.published.all() #Este es el administrador que definimos
    return render(request,'blog/post/list.html',{'posts': posts}) # renderizar plantillas HTML con datos dinámicos

def post_detail(request, id):
    # Se puede hacer asi o
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found.")
    post = get_object_or_404(Post,id=id,status=Post.Status.PUBLISHED)
    return render(request,'blog/post/detail.html',{'post': post})
