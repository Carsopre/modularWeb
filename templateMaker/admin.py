from django.contrib import admin
from templateMaker.models import *


class TemplateTemplateFieldInLine(admin.TabularInline):
    model = TemplateTemplateField
    extra = 1


class TemplateAdmin(admin.ModelAdmin):
    inlines = [
        TemplateTemplateFieldInLine,
    ]


admin.site.register(Template, TemplateAdmin)
admin.site.register(TemplateField)