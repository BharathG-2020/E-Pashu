from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    Category Table implimented with MPTT.
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class AnimalType(models.Model):
    """
    AnimalType Table will provide a list of the different types
    of animals that are for sale.
    """

    name = models.CharField(verbose_name=_("Animal Name"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Animal Type")
        verbose_name_plural = _("Animal Types")

    def __str__(self):
        return self.name


class AnimalSpecification(models.Model):
    """
    The Animal Specification Table contains animal
    specifiction or features for the animal types.
    """

    animal_type = models.ForeignKey(AnimalType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Animal Specification")
        verbose_name_plural = _("Animal Specifications")

    def __str__(self):
        return self.name


class Animal(models.Model):
    """
    The Animal table contining all animal items.
    """

    animal_type = models.ForeignKey(AnimalType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("Required"),
        max_length=255,
    )
    owner_name = models.CharField(max_length=50, default="No Owner Name Specified")
    contact = models.CharField(max_length=10, default="NA")
    animal_id = models.CharField(max_length=12, default="NA")
    GENDER_CHOICES = (
        (u"Male", u"Male"),
        (u"Female", u"Female"),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="please select")
    age = models.CharField(max_length=50, default="0")
    description = models.TextField(verbose_name=_("description"), help_text=_("Required"), blank=True)
    address = models.TextField(verbose_name=_("address"), help_text=_("Required"), blank=True)
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name=_("Regular price"),
        help_text=_("Maximum 10,00,000.00"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 10,00,000.00."),
            },
        },
        max_digits=9,
        decimal_places=2,
    )
    # discount_price = models.DecimalField(
    #     verbose_name=_("Discount price"),
    #     help_text=_("Maximum 10,00,000.00"),
    #     error_messages={
    #         "name": {
    #             "max_length": _("The price must be between 0 and 10,00,000.00."),
    #         },
    #     },
    #     max_digits=9,
    #     decimal_places=2,
    # )
    is_active = models.BooleanField(
        verbose_name=_("Animal visibility"),
        help_text=_("Change animal visibility"),
        default=True,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Animal")
        verbose_name_plural = _("Animals")

    def get_absolute_url(self):
        return reverse("store:animal_detail", args=[self.slug])

    def __str__(self):
        return self.title


class AnimalSpecificationValue(models.Model):
    """
    The Animal Specification Value table holds each of the
    animals individual specification or bespoke features.
    """

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    specification = models.ForeignKey(AnimalSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("Animal specification value (maximum of 255 words"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Animal Specification Value")
        verbose_name_plural = _("Animal Specification Values")

    def __str__(self):
        return self.value


class AnimalImage(models.Model):
    """
    The Animal Image table.
    """

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="animal_image")
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a animal image"),
        upload_to="images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Animal Image")
        verbose_name_plural = _("Animal Images")
