from . import views
from django.urls import path

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<int:year>", views.year_archive, name="year_archive"),
    path("<int:year>/<int:month>", views.month_archive, name="month_archive"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
]
