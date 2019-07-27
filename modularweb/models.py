from django.db import models
from polymorphic.models import PolymorphicModel
import os


class BaseField(PolymorphicModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class IconField(BaseField):
    faIcon = models.CharField(max_length=50)
    faIconType = models.CharField(max_length=50, default="fab")
    isVisible = models.BooleanField(default=True)

    def __str__(self):
        return self.baseField.name + 'icon'


class Image(BaseField):
    url = models.ImageField(
        upload_to='uploads/imgs/')


class BasePage(PolymorphicModel):
    slug = models.SlugField(max_length=25, unique=True)
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def full_url(self):
        return os.path.join(self.url, self.slug)

    def get_page(slugPage):
        return BasePage.objects.filter(slug=slugPage).first()

    def get_links(self):
        return LinkField.objects.filter(
            basePage=self
        )


class ScaffoldPage(BasePage):

    def get_content_pages(self):
        content_pages = ScaffoldContentPages.objects.filter(
            scaffold_page=self).all()
        return [
            (mcp.section_order, mcp.section)
            for mcp in content_pages]


class ContentPage(BasePage):
    body = models.TextField(blank=True)
    background = models.ForeignKey(
        to=Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def get_main_fields(self):
        return HeaderPageField.get_fields(
            self,
            HeaderPageField.MAINFIELD)

    def get_sub_fields(self):
        return HeaderPageField.get_fields(
            self,
            HeaderPageField.SUBFIELD)


class ScaffoldContentPages(models.Model):
    section_order = models.PositiveSmallIntegerField(default=0)
    scaffold_page = models.ForeignKey(
        to=ScaffoldPage,
        related_name='main_page'
    )
    section = models.ForeignKey(
        to=BasePage,
        related_name='scaffold_section'
    )

    def __str__(self):
        return '{} - ({}) - {}'.format(
            self.scaffold_page.title,
            self.section_order,
            self.section.title)


class PageField(BaseField):
    basePage = models.ForeignKey(
        to=BasePage,
        on_delete=models.CASCADE)


class LinkField(PageField):
    order_link = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return '({}) - {} - {}'.format(
            self.order_link,
            self.name,
            self.basePage.title)


class ExternalLink(LinkField):
    target = models.URLField()


class InternalLink(LinkField):
    target = models.ForeignKey(
        to=BasePage,
        on_delete=models.CASCADE)


class SimpleField(PageField):
    value = models.CharField(max_length=50)

    def __str__(self):
        return '(Text) ' + self.name


class HeaderPageField(SimpleField):
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

    @staticmethod
    def get_fields(BasePage, FieldType):
        HeaderPageField.objects.filter(
            fieldType=FieldType,
            basePage=BasePage).all()
