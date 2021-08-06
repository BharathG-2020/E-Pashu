from django.shortcuts import get_object_or_404, render

from .models import Animal, Category


def animal_all(request):
    animals = Animal.objects.prefetch_related("animal_image").filter(is_active=True)
    return render(request, "store/index.html", {"animals": animals})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    animals = Animal.objects.filter(
        category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)
    )
    return render(request, "store/category.html", {"category": category, "animals": animals})


def animal_detail(request, slug):
    animal = get_object_or_404(Animal, slug=slug, is_active=True)
    return render(request, "store/single.html", {"animal": animal})
