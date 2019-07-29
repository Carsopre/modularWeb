from django.contrib import admin

from polymorphic.admin import \
    PolymorphicParentModelAdmin, \
    PolymorphicChildModelAdmin, \
    PolymorphicChildModelFilter, \
    PolymorphicInlineSupportMixin, \
    StackedPolymorphicInline

from mainApp.models import *


# Media admin


class MediaItemPolyAdmin(PolymorphicChildModelAdmin):
    base_model = MediaItem


@admin.register(MediaIcon)
class MediaIconAdmin(MediaItemPolyAdmin):
    base_model = MediaIcon


@admin.register(MediaImage)
class MediaImageAdmin(MediaItemPolyAdmin):
    base_model = MediaImage


@admin.register(MediaItem)
class MediaItemAdmin(PolymorphicParentModelAdmin):
    base_model = FlexiblePage
    child_models = (
        MediaIcon,
        MediaImage,
    )
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.


# Base page admin

class FlexiblePageFieldInline(admin.StackedInline):
    model = FlexiblePageField
    extra = 1


class CompositePageInline(admin.StackedInline):
    model = CompositePage
    extra = 1


@admin.register(ScaffoldPage)
class ScaffoldAdmin(admin.ModelAdmin):
    base_model = ScaffoldPage
    inlines = (CompositePageInline,)


class FlexiblePagePolyAdmin(PolymorphicChildModelAdmin):
    base_model = FlexiblePage
    inlines = (
        FlexiblePageFieldInline,
    )

@admin.register(IntroPage)
class IntroPageAdmin(FlexiblePagePolyAdmin):
    base_model = IntroPage


@admin.register(BlogPage)
class BlogPageAdmin(FlexiblePagePolyAdmin):
    base_model = BlogPage


@admin.register(OutroPage)
class OutroPageAdmin(FlexiblePagePolyAdmin):
    base_model = OutroPage

@admin.register(FlexiblePage)
class FlexiblePageAdmin(
        PolymorphicParentModelAdmin,
        PolymorphicInlineSupportMixin,
        admin.ModelAdmin):

    base_model = FlexiblePage
    child_models = (
        BlogPage,
        IntroPage,
        OutroPage,
    )
    exclude = ['linked_pages']
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.


class BaseFieldPolyAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = BaseField  # Optional, explicitly set here.


@admin.register(PageLink)
class PageLinkAdmin(BaseFieldPolyAdmin):
    base_model = PageLink  # Explicitly set here!
    show_in_index = False  # makes child model admin visible in main admin site


@admin.register(LandingPageField)
class LandingPageFieldAdmin(BaseFieldPolyAdmin):
    base_model = LandingPageField
    show_in_index = False


class LibraryEntryCollectionInline(admin.StackedInline):
    model = LibraryEntryCollection
    extra = 1


@admin.register(Library)
class LibraryAdmin(BaseFieldPolyAdmin):
    base_model = Library
    show_in_index = False
    inlines = (
        LibraryEntryCollectionInline,
    )


@admin.register(LibraryEntry)
class LibraryEntryAdmin(PageLinkAdmin):
    base_model = LibraryEntry
    show_in_index = False
    inlines = (
        LibraryEntryCollectionInline,
    )


@admin.register(BaseField)
class BaseFieldAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = BaseField  # Optional, explicitly set here.
    child_models = (
        PageLink,
        LandingPageField,
        Library,
        LibraryEntry)
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.
