from django.shortcuts import render
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView


# def post_list(request):
#     posts = Post.published.all()
#     paginator = Paginator(posts, 10)
#     page_number = request.GET.get("page")
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request, "blog/post/list.html", {"page": page_number, "posts": posts})


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


class PostListView(ListView):
    model = Post
    paginate_by = 10
    queryset = Post.published.all()
    context_object_name = "posts"
    template_name = "blog/post/list.html"


class PostDetail(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post/detail.html"

    def get_queryset(self):
        return Post.published.all()

    def get_object(self, queryset=None):
        return (
            self.get_queryset()
            .filter(
                slug=self.kwargs.get("slug"),
                publish__year=self.kwargs.get("year"),
                publish__month=self.kwargs.get("month"),
                publish__day=self.kwargs.get("day"),
            )
            .first()
        )
