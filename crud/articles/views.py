from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, CommentForm
from .models import Article, Comment

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-id')
    context = {
        'articles':articles
    }
    return render(request,'articles/index.html',context)

@login_required
def create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:index')
    else:
        form = ArticleForm()
    context = {
        'form':form
    }
    return render(request,'articles/form.html',context)

@login_required
def detail(request,article_id):
    article = get_object_or_404(Article, id = article_id)
    comments = Comment.objects.order_by('-id')
    form = CommentForm()
    context = {
        'article':article,
        'comments':comments,
        'form':form,
    }
    return render(request,'articles/detail.html',context)

@login_required
def update(request,article_id):
    article = get_object_or_404(Article, id = article_id)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance = article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail',article_id)
    else:
        form = ArticleForm(instance = article)
    context = {
        'form' : form
    }
    return render(request, 'articles/form.html', context)

@login_required
def delete(request, article_id):
    article = get_object_or_404(Article, id = article_id)
    article.delete()
    return redirect('articles:index')

@login_required
def comment_create(request,article_id):
    article = get_object_or_404(Article, id = article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
    return redirect('articles:detail', article_id)


def comment_delete(request,article_id,comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('articles:detail', article_id)


def comment_update(request,article_id,comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance = comment)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article_id)
    else:
        form = CommentForm(instance = comment)
    context = {
        'form':form
    }
    return render(request, 'articles/form.html', context)

