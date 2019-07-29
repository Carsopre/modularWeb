from django.db import models
from django.forms import ModelForm
from polymorphic.models import PolymorphicModel
import os


class MediaItem(PolymorphicModel):
    title = models.CharField(
        max_length=50)

    def __str__(self):
        return self.title


class MediaImage(MediaItem):
    description = models.TextField(
        blank=True)
    img = models.ImageField(
        upload_to='uploads/imgs/')


class MediaIcon(MediaItem):
    faIcon = models.CharField(
        max_length=50)
    faIconType = models.CharField(
        max_length=50,
        default="fab")
    isVisible = models.BooleanField(
        default=True)


class ContentPageType(models.Model):
    INTRO_PAGE = 'IP'
    BLOG_PAGE = 'BP'
    OUTRO_PAGE = 'OP'
    FIELD_TYPES = [
        (INTRO_PAGE, 'Intro'),
        (BLOG_PAGE, 'Blog'),
        (OUTRO_PAGE, 'Outro'),
    ]


class BasePage(PolymorphicModel):
    slug = models.SlugField(
        max_length=25,
        unique=True)
    title = models.CharField(
        max_length=50)

    def __str__(self):
        return self.title

    def get_page(slug_page):
        return BasePage.objects.filter(
            slug=slug_page).first()

    def get_url(self):
        return self.slug


class ScaffoldPage(BasePage):
    def get_content_pages(self):
        content_pages = CompositePage.objects.filter(
            scaffold_page=self).all()
        return [
            (mcp.page_order, mcp.content_page)
            for mcp in content_pages]

    def get_url(self):
        return 'scaffold/' + super().get_url()


class FlexiblePage(BasePage):
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

    @property
    def background_url(self):
        if self.background is None:
            return ''
        return self.background.img.url

    @property
    def internal_links(self):
        return [
            lp
            for lp in self.fields.all()
            if isinstance(lp, PageLink) and
            lp.internal_link]

    @property
    def external_links(self):
        return [
            lp
            for lp in self.fields.all()
            if isinstance(lp, PageLink) and
            not lp.internal_link]

    @property
    def libraries(self):
        return [
            (fpf.order_link, fpf.to_field.entries_collection)
            for fpf in FlexiblePageField.objects.filter(
                in_page=self
            ).all()
            if isinstance(fpf.to_field, Library)
        ]

    def get_property_dict(self):
        # to be overriden by subclasses
        return {
            'title': self.title,
            'slug': self.slug,
            'background': self.background_url,
            'internal_links': self.internal_links,
            'external_links': self.external_links,
            'libraries': self.libraries,
        }

    def get_url(self):
        return 'section/' + super().get_url()


class IntroPage(FlexiblePage):
    def get_property_dict(self):
        intro_page_dict = {
            'main_fields': self.main_fields,
            'sub_fields': self.sub_fields,
        }
        upper_dict = super().get_property_dict()
        # merge the dictionaries
        return {**upper_dict, **intro_page_dict}

    def __get_landing_fields(self, of_type):
        return [
            lp
            for lp in self.fields.all()
            if isinstance(lp, LandingPageField) and
            lp.field_type == of_type]

    @property
    def main_fields(self):
        return self.__get_landing_fields(
            of_type=LandingPageField.MAINFIELD)

    @property
    def sub_fields(self):
        return self.__get_landing_fields(
            of_type=LandingPageField.SUBFIELD)


class BlogPage(FlexiblePage):
    blog_body = models.TextField(
        blank=True)

    def get_property_dict(self):
        blog_page_dict = {
            'blog_body': self.blog_body,
        }
        upper_dict = super().get_property_dict()
        # merge the dictionaries
        return {**upper_dict, **blog_page_dict}


class OutroPage(FlexiblePage):
    outro_text = models.TextField(
        blank=True)

    def get_property_dict(self):
        blog_page_dict = {
            'outro_text': self.outro_text,
        }
        upper_dict = super().get_property_dict()
        # merge the dictionaries
        return {**upper_dict, **blog_page_dict}


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
        to=MediaItem,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    internal_link = models.ForeignKey(
        to=FlexiblePage,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    @property
    def page_url(self):
        if self.internal_link:
            return self.internal_link.get_url()
        return self.text_value


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


class Library(BaseField):
    entries = models.ManyToManyField(
        'LibraryEntry',
        blank=True,
        related_name='has_entries',
        through='LibraryEntryCollection')

    @property
    def entries_collection(self):
        collection = {
            'dict': self.name,
            'dict_values': [
                entry
                for entry in self.entries.all()
            ]
        }

        return collection


class LibraryEntry(PageLink):
    summary = models.TextField(
        blank=True
    )
    status = models.CharField(
        blank=True,
        max_length=50)


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


class LibraryEntryCollection(models.Model):
    library = models.ForeignKey(
        to=Library,
        related_name='has_collection',
        on_delete=models.CASCADE)
    entry = models.ForeignKey(
        to=LibraryEntry,
        related_name='has_entry',
        on_delete=models.CASCADE)
