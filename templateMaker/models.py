from django.db import models
from polymorphic.models import PolymorphicModel
import os


class TemplateField(PolymorphicModel):
    name = models.CharField(max_length=50)
    multiple = models.BooleanField()

    def __str__(self):
        return self.name


class Template(models.Model):
    name = models.CharField(max_length=50)
    html_code = models.TextField(blank=True)
    fields = models.ManyToManyField(
        to=TemplateField,
        verbose_name='Template Fields',
        related_name='template_r_fields')

    def __str__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    templates = models.ManyToManyField(
        to=Template,
        verbose_name='Page Templates',
        related_name='page_r_templates')



class TypeField(PolymorphicModel):
    name = models.CharField(max_length=50)
    composite_field = models.ManyToManyField(
        to=TemplateField,
        verbose_name='Template Fields',
        related_name='template_r_fields')

    def __str__(self):
        return self.name


class TextField(TypeField):
    value = models.TextField(
        blank=True)


class IconField(TypeField):
    faIcon = models.CharField(
        max_length=50)
    faIconType = models.CharField(
        max_length=50,
        default="fab")
    isVisible = models.BooleanField(
        default=True)

    def __str__(self):
        return 'Icon ' + self.name
