from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("", views.animal_all, name="store_home"),
    path("<slug:slug>", views.animal_detail, name="animal_detail"),
    path("shop/<slug:category_slug>/", views.category_list, name="category_list"),
]
