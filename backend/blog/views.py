from django.shortcuts import render
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/post/list.html", {"page": page_number, "posts": posts})


def post_detail(request, year, month, day, post):
    post = Post.objects.get(
        slug=post, publish__year=year, publish__month=month, publish__day=day
    )
    return render(request, "blog/post/detail.html", {"post": post})


def year_archive(request, year):
    posts = Post.published.filter(publish__year=year)
    return render(
        request, "blog/post/year_archive.html", {"posts": posts, "year": year}
    )


def month_archive(request, year, month):
    posts = Post.published.filter(publish__year=year, publish__month=month)
    return render(
        request,
        "blog/post/month_archive.html",
        {"posts": posts, "year": year, "month": month},
    )
