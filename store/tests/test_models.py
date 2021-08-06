from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from store.models import Animal, Category


class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name="django", slug="django")

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), "django")

    def test_category_url(self):
        """
        Test category model slug and URL reverse
        """
        data = self.data1
        response = self.client.post(reverse("store:category_list", args=[data.slug]))
        self.assertEqual(response.status_code, 200)


class TestAnimalsModel(TestCase):
    def setUp(self):
        Category.objects.create(name="django", slug="django")
        User.objects.create(username="admin")
        self.data1 = Animal.objects.create(
            category_id=1,
            title="django beginners",
            created_by_id=1,
            slug="django-beginners",
            price="20.00",
            image="django",
        )
        self.data2 = Animal.animals.create(
            category_id=1,
            title="django advanced",
            created_by_id=1,
            slug="django-advanced",
            price="20.00",
            image="django",
            is_active=False,
        )

    def test_animals_model_entry(self):
        """
        Test animal model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Animal))
        self.assertEqual(str(data), "django beginners")

    def test_animals_url(self):
        """
        Test animal model slug and URL reverse
        """
        data = self.data1
        url = reverse("store:animal_detail", args=[data.slug])
        self.assertEqual(url, "/django-beginners")
        response = self.client.post(reverse("store:animal_detail", args=[data.slug]))
        self.assertEqual(response.status_code, 200)

    def test_animals_custom_manager_basic(self):
        """
        Test animal model custom manager returns only active animals
        """
        data = Animal.animals.all()
        self.assertEqual(data.count(), 1)
