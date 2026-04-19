from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(  # pyright: ignore[reportUnknownMemberType]
    model_or_iterable=models.All_Tables,
    admin_class=None,
)
