from django.contrib import admin

from polymorphic.admin import \
    PolymorphicParentModelAdmin, \
    PolymorphicChildModelAdmin, \
    PolymorphicChildModelFilter, \
    PolymorphicInlineSupportMixin, \
    StackedPolymorphicInline

from personalWeb.models import *

admin.site.register(MediaIcon)
admin.site.register(MediaImage)


class FlexiblePageFieldInline(admin.StackedInline):
    model = FlexiblePageField
    extra = 1


class CompositePageInline(admin.StackedInline):
    model = CompositePage
    extra = 1


@admin.register(ScaffoldPage)
class ScaffoldAdmin(admin.ModelAdmin):
    inlines = (CompositePageInline,)


@admin.register(FlexiblePage)
class FlexiblePageAdmin(admin.ModelAdmin):
    inlines = (
        FlexiblePageFieldInline,
        # CompositePageInline,
    )
    exclude = ['linked_pages']


class BaseFieldPolyAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = BaseField  # Optional, explicitly set here.


@admin.register(PageLink)
class PageLinkPolyAdmin(BaseFieldPolyAdmin):
    base_model = PageLink  # Explicitly set here!
    show_in_index = False  # makes child model admin visible in main admin site


@admin.register(LandingPageField)
class ModelCAdmin(BaseFieldPolyAdmin):
    base_model = LandingPageField  # Explicitly set here!
    show_in_index = False  # makes child model admin visible in main admin site


@admin.register(BaseField)
class BaseFieldAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = BaseField  # Optional, explicitly set here.
    child_models = (PageLink, LandingPageField)
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.
