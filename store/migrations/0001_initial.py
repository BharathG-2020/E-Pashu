# Generated by Django 3.1.7 on 2021-03-02 14:12

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.CharField(
                        help_text="Required and unique", max_length=255, unique=True, verbose_name="Category Name"
                    ),
                ),
                ("slug", models.SlugField(max_length=255, unique=True, verbose_name="Category safe URL")),
                ("is_active", models.BooleanField(default=True)),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="store.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Animal",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(help_text="Required", max_length=255, verbose_name="title")),
                ("description", models.TextField(blank=True, help_text="Not Required", verbose_name="description")),
                ("slug", models.SlugField(max_length=255)),
                (
                    "regular_price",
                    models.DecimalField(
                        decimal_places=2,
                        error_messages={"name": {"max_length": "The price must be between 0 and 999.99."}},
                        help_text="Maximum 999.99",
                        max_digits=5,
                        verbose_name="Regular price",
                    ),
                ),
                (
                    "discount_price",
                    models.DecimalField(
                        decimal_places=2,
                        error_messages={"name": {"max_length": "The price must be between 0 and 999.99."}},
                        help_text="Maximum 999.99",
                        max_digits=5,
                        verbose_name="Discount price",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, help_text="Change animal visibility", verbose_name="Animal visibility"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created at")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Updated at")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to="store.category")),
            ],
            options={
                "verbose_name": "Animal",
                "verbose_name_plural": "Animals",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="AnimalSpecification",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="Required", max_length=255, verbose_name="Name")),
            ],
            options={
                "verbose_name": "Animal Specification",
                "verbose_name_plural": "Animal Specifications",
            },
        ),
        migrations.CreateModel(
            name="AnimalType",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.CharField(help_text="Required", max_length=255, unique=True, verbose_name="Animal Name"),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Animal Type",
                "verbose_name_plural": "Animal Types",
            },
        ),
        migrations.CreateModel(
            name="AnimalSpecificationValue",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "value",
                    models.CharField(
                        help_text="Animal specification value (maximum of 255 words",
                        max_length=255,
                        verbose_name="value",
                    ),
                ),
                ("animal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="store.animal")),
                (
                    "specification",
                    models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to="store.animalspecification"),
                ),
            ],
            options={
                "verbose_name": "Animal Specification Value",
                "verbose_name_plural": "Animal Specification Values",
            },
        ),
        migrations.AddField(
            model_name="animalspecification",
            name="animal_type",
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to="store.animaltype"),
        ),
        migrations.CreateModel(
            name="AnimalImage",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "image",
                    models.ImageField(
                        default="images/default.png",
                        help_text="Upload a animal image",
                        upload_to="images/",
                        verbose_name="image",
                    ),
                ),
                (
                    "alt_text",
                    models.CharField(
                        blank=True,
                        help_text="Please add alturnative text",
                        max_length=255,
                        null=True,
                        verbose_name="Alturnative text",
                    ),
                ),
                ("is_feature", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "animal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="animal_image", to="store.animal"
                    ),
                ),
            ],
            options={
                "verbose_name": "Animal Image",
                "verbose_name_plural": "Animal Images",
            },
        ),
        migrations.AddField(
            model_name="animal",
            name="animal_type",
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to="store.animaltype"),
        ),
    ]
