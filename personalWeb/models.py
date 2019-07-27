from django.db import models
from polymorphic.models import PolymorphicModel
import os


class FlexiblePage(PolymorphicModel):
    slug = models.SlugField(max_length=25, unique=True)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def get_page(slugPage):
        return FlexiblePage.objects.filter(slug=slugPage).first()


class ScaffoldPage(models.Model):
    slug = models.SlugField(max_length=25, unique=True)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def get_content_pages(self):
        return CompositePage.objects.filter(
            scaffold_page=self
        ).all()


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


class BaseField(models.Model):
    name = models.CharField(max_length=50)
    text_value = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class LandingPageField(BaseField):
    MAINFIELD = 'MF'
    SUBFIELD = 'SF'
    FIELD_TYPES = [
        (MAINFIELD, 'Main field (h2)'),
        (SUBFIELD, 'Sub field (h3)')
    ]
    fieldType = models.CharField(
        max_length=2,
        choices=FIELD_TYPES,
        default=MAINFIELD,
    )

    def get_main_fields():
        return LandingPageField.objects.filter(
            fieldType=LandingPageField.MAINFIELD).all()

    def get_sub_fields():
        return LandingPageField.objects.filter(
            fieldType=LandingPageField.SUBFIELD).all()


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


class PageLink(BaseField):
    order_link = models.PositiveSmallIntegerField(default=0)
    iconField = models.ForeignKey(
        to=MediaIcon,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)


class InternalLink(PageLink):
    basePage = models.ForeignKey(
        to=FlexiblePage,
        on_delete=models.CASCADE)


class ContentPage(FlexiblePage):
    body = models.TextField(blank=True)
    linkedPages = models.ManyToManyField(
        PageLink,
        blank=True,
        related_name='linked_pages')
    fields = models.ManyToManyField(
        BaseField,
        blank=True)

    background = models.ForeignKey(
        MediaImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def get_background_url(self):
        if self.background is None:
            return ''
        return self.background.url

    def get_landing_fields(self, ofType):
        return LandingPageField.objects.filter(
            contentpage=self,
            fieldType=ofType)

    def get_icon_fields(self):
        return IconField.objects.filter(contentpage=self)

    def get_linked_pages(self):
        if self.linkedPages.exists():
            return self.linkedPages.all()
        return None

    def get_library_list(self):
        linked_pages = self.get_linked_pages()
        if not linked_pages:
            return

        subset = [
            page_link
            for page_link in linked_pages
            if isinstance(page_link.basePage, LibraryPage)]

        return subset
