from django.conf import settings


def business(request):
    b = settings.BUSINESS
    wa = f"https://wa.me/{b['whatsapp']}?text=Hello%20Moonshine%20Events%2C%20I%20would%20like%20a%20quote%20for%20my%20event."
    return {"biz": b, "whatsapp_url": wa}
