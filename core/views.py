from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect, render

from .forms import EnquiryForm, SignupForm
from .models import (CateringPackage, Enquiry, FAQ, GalleryItem, MenuItem,
                     Service, Testimonial)


def _handle_enquiry(request, initial=None):
    """Returns (form, response). response is a redirect when saved, else None."""
    if request.method == "POST" and request.POST.get("form_name") == "enquiry":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            if request.user.is_authenticated:
                enquiry.user = request.user
            enquiry.save()
            messages.success(request, "Thank you. We have your enquiry and will reply the same working day.")
            return form, redirect(f"{request.path}#contact")
        messages.error(request, "Please fix the highlighted fields and send again.")
        return form, None
    return EnquiryForm(initial=initial or {}), None


def home(request):
    initial = {k: request.GET[k] for k in ("event_type", "event_date", "guests") if request.GET.get(k)}
    form, response = _handle_enquiry(request, initial)
    if response:
        return response
    return render(request, "home.html", {
        "form": form,
        "event_types": Enquiry.EVENT_TYPES,
        "services": Service.objects.all(),
        "gallery": GalleryItem.objects.all(),
        "gallery_categories": GalleryItem.CATEGORIES,
        "testimonials": Testimonial.objects.all(),
        "faqs": FAQ.objects.all(),
        "packages": CateringPackage.objects.all(),
    })


def catering(request):
    initial = {"event_type": "catering"}
    pkg = request.GET.get("package")
    if pkg and pkg.isdigit():
        initial["catering_package"] = pkg
    form, response = _handle_enquiry(request, initial)
    if response:
        return response
    menu = []
    items = MenuItem.objects.all()
    for key, label in MenuItem.CATEGORIES:
        group = [i for i in items if i.category == key]
        if group:
            menu.append({"key": key, "label": label, "items": group})
    return render(request, "catering.html", {
        "form": form,
        "packages": CateringPackage.objects.all(),
        "menu": menu,
        "gallery": GalleryItem.objects.filter(category="catering"),
    })


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome to Moonshine Events. Your account is ready.")
        return redirect("dashboard")
    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    if request.user.is_staff:
        enquiries = Enquiry.objects.select_related("catering_package")
        counts = dict(Enquiry.objects.values_list("status").annotate(n=Count("id")))
        stats = [(label, counts.get(key, 0)) for key, label in Enquiry.STATUSES]
    else:
        enquiries = request.user.enquiries.select_related("catering_package")
        stats = None
    return render(request, "dashboard.html", {"enquiries": enquiries[:100], "stats": stats})
