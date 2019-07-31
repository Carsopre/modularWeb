from django.contrib import admin

from polymorphic.admin import \
    PolymorphicParentModelAdmin, \
    PolymorphicChildModelAdmin, \
    PolymorphicChildModelFilter, \
    PolymorphicInlineSupportMixin, \
    StackedPolymorphicInline

from portFolioApp.models import *


# Register your models here.
class PortFolioPageLibraryCollectionInline(admin.StackedInline):
    model = PortFolioPageLibraryCollection
    extra = 1


class PortFolioLibraryTagCollectionInline(admin.StackedInline):
    model = PortFolioLibraryTagCollection
    extra = 1


class PortFolioEntryTagCollectionInline(admin.StackedInline):
    model = PortFolioEntryTagCollection
    extra = 1


@admin.register(PortFolioPage)
class PortFolioPageAdmin(admin.ModelAdmin):
    base_model = PortFolioPage
    inlines = (PortFolioPageLibraryCollectionInline,)


@admin.register(PortFolioLibrary)
class PortFolioLibraryAdmin(admin.ModelAdmin):
    base_model = PortFolioLibrary
    exclude = ('portfolio_tags',)
    inlines = (
        PortFolioLibraryTagCollectionInline,
        )


@admin.register(PortFolioEntry)
class PortFolioEntryAdmin(admin.ModelAdmin):
    base_model = PortFolioEntry
    exclude = ('entry_tags',)
    inlines = (
        PortFolioEntryTagCollectionInline,
        )

@admin.register(EntryTag)
class EntryTagAdmin(admin.ModelAdmin):
    base_model = EntryTag
    inlines =(
        PortFolioLibraryTagCollectionInline,
    )