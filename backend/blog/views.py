from django.shortcuts import render
from .models import Post
from .forms import CommentForm, EmailPostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail

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

    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )


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


# class PostDetail(DetailView):
#     model = Post
#     context_object_name = "post"
#     template_name = "blog/post/detail.html"

#     def get_queryset(self):
#         return Post.published.all()

#     def get_object(self, queryset=None):
#         return (
#             self.get_queryset()
#             .filter(
#                 slug=self.kwargs.get("slug"),
#                 publish__year=self.kwargs.get("year"),
#                 publish__month=self.kwargs.get("month"),
#                 publish__day=self.kwargs.get("day"),
#             )
#             .first()
#         )

#     def show_comments(self, request):
#         post = self.get_object()
#         comments = post.comments.filter(active=True)

#         new_comment = None

#         if self.request.method == "POST":
#             comment_form = CommentForm(data=self.request.POST)
#             if comment_form.is_valid():
#                 new_comment = comment_form.save(commit=False)
#                 new_comment.post = post
#                 new_comment.save()
#         else:
#             comment_form = CommentForm()

#         return render(
#             request,
#             "blog/post/detail.html",
#             {
#                 "post": post,
#                 "comments": comments,
#                 "new_comment": new_comment,
#                 "comment_form": comment_form,
#             },
#         )


def post_share(request, post_id):
    # post = Post.published.get(id=post_id)
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, "your_email@example.com", [cd["to"]])
            sent = True

    else:
        form = EmailPostForm()

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )
