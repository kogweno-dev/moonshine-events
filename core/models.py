from django.conf import settings
from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=120)
    summary = models.TextField()
    features = models.TextField(help_text="One feature per line.")
    image = models.CharField(max_length=200, help_text="Path under static/, e.g. images/red-aisle.jpg")
    cta_label = models.CharField(max_length=60, default="Get a quote")
    link = models.CharField(max_length=200, default="#contact", help_text="Where the tile leads, e.g. #contact or /catering/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def feature_list(self):
        return [f.strip() for f in self.features.splitlines() if f.strip()]


class GalleryItem(models.Model):
    CATEGORIES = [
        ("wedding", "Weddings"),
        ("corporate", "Corporate"),
        ("tents", "Tents & Decor"),
        ("catering", "Catering"),
        ("celebration", "Celebrations"),
    ]
    title = models.CharField(max_length=120)
    caption = models.CharField(max_length=220, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    image = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    event = models.CharField(max_length=160)
    quote = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=220)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "FAQ"

    def __str__(self):
        return self.question


class CateringPackage(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)
    price_per_guest = models.DecimalField(max_digits=8, decimal_places=0, help_text="Starting price in KSh per guest.")
    min_guests = models.PositiveIntegerField(default=50)
    includes = models.TextField(help_text="One item per line.")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

    @property
    def include_list(self):
        return [i.strip() for i in self.includes.splitlines() if i.strip()]

    @property
    def top_includes(self):
        return self.include_list[:4]


class MenuItem(models.Model):
    CATEGORIES = [
        ("starters", "Starters"),
        ("mains", "Mains"),
        ("sides", "Sides & Salads"),
        ("desserts", "Desserts"),
        ("drinks", "Drinks"),
    ]
    category = models.CharField(max_length=20, choices=CATEGORIES)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=220, blank=True)
    is_vegetarian = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.get_category_display()}: {self.name}"


class Enquiry(models.Model):
    EVENT_TYPES = [
        ("wedding", "Wedding"),
        ("corporate", "Corporate / public function"),
        ("tents", "Tents & decor hire only"),
        ("catering", "Catering only"),
        ("baby_shower", "Baby shower / gender reveal"),
        ("birthday", "Birthday / anniversary"),
        ("dowry", "Dowry / ruracio"),
        ("graduation", "Graduation"),
        ("celebration_of_life", "Celebration of life"),
        ("other", "Other"),
    ]
    BUDGETS = [
        ("", "Prefer not to say"),
        ("<100k", "Under 100,000"),
        ("100-300k", "100,000 – 300,000"),
        ("300-600k", "300,000 – 600,000"),
        ("600k-1m", "600,000 – 1,000,000"),
        (">1m", "Above 1,000,000"),
    ]
    STATUSES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("quoted", "Quote sent"),
        ("booked", "Booked"),
        ("closed", "Closed"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="enquiries")
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    event_date = models.DateField(null=True, blank=True)
    guests = models.PositiveIntegerField(null=True, blank=True)
    budget = models.CharField(max_length=20, choices=BUDGETS, blank=True)
    venue = models.CharField(max_length=160, blank=True)
    catering_package = models.ForeignKey(CateringPackage, null=True, blank=True, on_delete=models.SET_NULL, related_name="enquiries")
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default="new")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "enquiries"

    def __str__(self):
        return f"{self.name} · {self.get_event_type_display()}"
