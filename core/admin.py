from django.contrib import admin
from . import models


@admin.register(models.Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "event_type", "event_date", "guests", "catering_package", "status", "created")
    list_filter = ("status", "event_type", "catering_package")
    list_editable = ("status",)
    search_fields = ("name", "phone", "email", "venue", "message")
    date_hierarchy = "created"


@admin.register(models.CateringPackage)
class CateringPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "price_per_guest", "min_guests", "is_featured", "order")
    list_editable = ("price_per_guest", "is_featured", "order")


@admin.register(models.MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_vegetarian", "order")
    list_filter = ("category", "is_vegetarian")
    list_editable = ("order",)


@admin.register(models.GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "order")
    list_filter = ("category",)
    list_editable = ("order",)


for m in (models.Service, models.Testimonial, models.FAQ):
    admin.site.register(m)
