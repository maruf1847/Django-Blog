from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post
from d_marketing.models import Subscribing


def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search.html', context)


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_subscribe = Subscribing()
        new_subscribe.email = email
        new_subscribe.save()

    context = {
        'object_list': featured,
        'latest_post': latest
    }
    return render(request, 'index.html', context)


def blog(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request = request.GET.get('page')
    try:
        paginated_queryset = paginator.page(page_request)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(1)

    context = {
        'most_recent': most_recent,
        'posts': paginated_queryset,
        'category_count': category_count
    }
    return render(request, 'blog.html', context)


def post(request, id):
    post = get_object_or_404(Post, id=id)
    context = {
        'post': post
    }
    return render(request, 'post.html', context)