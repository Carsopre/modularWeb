from django.db import models
from django.forms import ModelForm
from polymorphic.models import PolymorphicModel
import os


class MediaIcon(models.Model):
    name = models.CharField(max_length=50)
    faIcon = models.CharField(max_length=50)
    faIconType = models.CharField(max_length=50, default="fab")
    isVisible = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MediaImage(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(
        blank=True
    )
    img = models.ImageField(upload_to='uploads/imgs/')

    def __str__(self):
        return self.title


class ContentPageType(models.Model):
    INTRO_PAGE = 'IP'
    BLOG_PAGE = 'BP'
    OUTRO_PAGE = 'OP'
    FIELD_TYPES = [
        (INTRO_PAGE, 'Intro'),
        (BLOG_PAGE, 'Blog'),
        (OUTRO_PAGE, 'Outro'),
    ]


class ScaffoldPage(models.Model):
    slug = models.SlugField(
        max_length=25,
        unique=True)
    title = models.CharField(
        max_length=50)

    def __str__(self):
        return self.title

    def get_page(slug_page):
        return ScaffoldPage.objects.filter(
            slug=slug_page).first()

    def get_content_pages(self):
        content_pages = CompositePage.objects.filter(
            scaffold_page=self).all()
        return [
            (mcp.page_order, mcp.content_page)
            for mcp in content_pages]


class FlexiblePage(models.Model):
    slug = models.SlugField(
        max_length=25,
        unique=True)

    title = models.CharField(
        max_length=50)

    body = models.TextField(
        blank=True)

    page_type = models.CharField(
        max_length=2,
        choices=ContentPageType.FIELD_TYPES,
        default=ContentPageType.INTRO_PAGE
    )

    fields = models.ManyToManyField(
        'BaseField',
        blank=True,
        related_name='has_fields',
        through='FlexiblePageField')

    background = models.ForeignKey(
        MediaImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.title

    def get_page(slug_page):
        return FlexiblePage.objects.filter(
            slug=slug_page).first()

    @property
    def background_url(self):
        if self.background is None:
            return ''
        return self.background.img.url

    @property
    def main_fields(self):
        return self.__get_landing_fields(
            of_type=LandingPageField.MAINFIELD)

    @property
    def sub_fields(self):
        return self.__get_landing_fields(
            of_type=LandingPageField.SUBFIELD)

    @property
    def internal_links(self):
        return [
            lp.internal_link
            for lp in self.fields.all()
            if isinstance(lp.tofield, PageLink) and
            lp.to_field.internal_link]

    @property
    def external_links(self):
        return [
            lp.internal_link
            for lp in self.fields.all()
            if isinstance(lp.tofield, PageLink) and
            not lp.to_field.internal_link]


class BaseField(PolymorphicModel):
    name = models.CharField(
        max_length=50)
    text_value = models.CharField(
        max_length=250,
        blank=True)

    def __str__(self):
        return self.name


class PageLink(BaseField):
    icon_field = models.ForeignKey(
        to=MediaIcon,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    internal_link = models.ForeignKey(
        to=FlexiblePage,
        null=True,
        blank=True,
        on_delete=models.CASCADE)


class LandingPageField(BaseField):
    MAINFIELD = 'MF'
    SUBFIELD = 'SF'
    FIELD_TYPES = [
        (MAINFIELD, 'Main field (h2)'),
        (SUBFIELD, 'Sub field (h3)')
    ]
    field_type = models.CharField(
        max_length=2,
        choices=FIELD_TYPES,
        default=MAINFIELD,
    )


# Cross-Reference Tables


class CompositePage(models.Model):
    page_order = models.PositiveSmallIntegerField(
        default=0)
    scaffold_page = models.ForeignKey(
        to=ScaffoldPage,
        on_delete=models.CASCADE,
        related_name='composite_scaffold_page')
    content_page = models.ForeignKey(
        to=FlexiblePage,
        on_delete=models.CASCADE,
        related_name='composite_content_page')

    def __str__(self):
        return '({}) - {} - {}'.format(
            self.page_order,
            self.scaffold_page.title,
            self.content_page.title)


class FlexiblePageField(models.Model):
    order_link = models.PositiveSmallIntegerField(
        default=0)
    in_page = models.ForeignKey(
        FlexiblePage,
        verbose_name='From',
        on_delete=models.CASCADE)
    to_field = models.ForeignKey(
        BaseField,
        verbose_name='Has field',
        related_name='has_field',
        on_delete=models.CASCADE)
