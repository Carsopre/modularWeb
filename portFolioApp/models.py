from django.db import models

from polymorphic.models import PolymorphicModel

from mainApp.models import *


# Create your models here.
class PortFolioPage(ScaffoldPage):
    portfolio_libraries = models.ManyToManyField(
        to="portFolioApp.PortFolioLibrary",
        verbose_name="Has library",
        through="portFolioApp.PortFolioPageLibraryCollection")


class PortFolioLibrary(Library):
    portfolio_tags = models.ManyToManyField(
        to="portFolioApp.EntryTag",
        verbose_name="Has tags")

    @property
    def portfolio_entries(self):
        filtered = [
            pfe
            for pfe in PortFolioEntry.objects
            if not set(pfe.entry_tags).isdisjoint(self.portfolio_tags)]
        return filtered


class PortFolioEntry(LibraryEntry):
    entry_tags = models.ManyToManyField(
        to="portFolioApp.EntryTag",
        verbose_name="Has tags",
        through="portFolioApp.PortFolioEntryTagCollection")


class EntryTag(models.Model):
    tag = models.CharField(
        "Entry Tag",
        unique=True,
        max_length=25)


# Cross-Reference Tables
class PortFolioPageLibraryCollection(models.Model):
    page = models.ForeignKey(
        to=PortFolioPage,
        related_name='has_page',
        on_delete=models.CASCADE)
    library = models.ForeignKey(
        to=PortFolioLibrary,
        related_name='has_library',
        on_delete=models.CASCADE)


class PortFolioLibraryTagCollection(models.Model):
    library = models.ForeignKey(
        to=PortFolioLibrary,
        related_name='has_library_collection',
        on_delete=models.CASCADE)
    tag = models.ForeignKey(
        to=EntryTag,
        related_name='has_entrytag',
        on_delete=models.CASCADE)


class PortFolioEntryTagCollection(models.Model):
    entry = models.ForeignKey(
        to=PortFolioEntry,
        related_name='has_entry_collection',
        on_delete=models.CASCADE)
    tag = models.ForeignKey(
        to=EntryTag,
        related_name='has_entry',
        on_delete=models.CASCADE)
