from django.shortcuts import render
from .models import Post


def post_list(request):
    posts = Post.published.all()
    return render(request, "blog/post/list.html", {"posts": posts})


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
