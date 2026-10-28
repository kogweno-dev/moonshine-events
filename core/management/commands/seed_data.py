from django.core.management.base import BaseCommand

from core.models import (CateringPackage, FAQ, GalleryItem, MenuItem, Service,
                         Testimonial)

CATERING_SERVICE = ("Catering & Hospitality",
     "In-house kitchen, trained waiting staff and menus built around your guests, from a plated dinner for forty to a buffet line for a thousand.",
     "Kenyan, continental and nyama choma menus\nBuffet, plated or cocktail service\nSoft drinks, mocktails and bar setup\nCrockery, cutlery and waiting staff",
     "images/kente-table.jpg", "See menus and prices")

SERVICES = [
    ("Wedding Planning & Styling",
     "Full coordination for traditional, church and garden weddings, or day-of management if you have already planned it yourself.",
     "Budget, timeline and vendor sourcing\nAisle, altar and reception decor\nBridal cars and entourage logistics\nRehearsal and wedding-day coordination",
     "images/red-aisle.jpg", "Plan a wedding"),
    ("Corporate & Public Functions",
     "Launches, AGMs, field days, county and NGO functions, graduations and staff parties, organised to a programme and a budget you can report on.",
     "VIP and press seating plans\nBranded tents, backdrops and signage\nPA, podium, staging and generator\nUshers, registration and protocol",
     "images/gold-black-tents.jpg", "Request a proposal"),
    ("Tents, Draping & Decor",
     "Our own tents, chairs, tables, carpets and fabric, styled to your colours instead of whatever happens to be in the store.",
     "Frame and stretch tents of all sizes\nCeiling draping and fabric backdrops\nChairs, tiffany seats, tables and linen\nFloral, lighting and centrepieces",
     "images/teal-tent.jpg", "Check availability"),
    ("Private Celebrations",
     "Baby showers, birthdays, dowry and ruracio ceremonies, anniversaries and graduations, with themed backdrops and balloon installs.",
     "Themed backdrops and balloon installs\nCake, dessert and gift tables\nGames, MC and entertainment\nPhoto corners guests actually queue for",
     "images/orange-blue-wedding.jpg", "Book a celebration"),
    ("Celebrations of Life",
     "Sensitive, well-run funeral and memorial services, handled quickly and quietly so the family can grieve instead of organise.",
     "Rapid tent, chair and PA mobilisation\nFloral tributes and tribute boards\nProgramme printing and ushering\nCatering for mourners and vigils",
     "images/green-balloons.jpg", "Talk to us today"),
]

GALLERY = [
    ("Garden wedding aisle", "Red carpet aisle with floral pedestals under a matching tent.", "wedding", "images/red-aisle.jpg"),
    ("Church entrance arch", "Red and white rose arch for a church ceremony.", "wedding", "images/flower-arch.jpg"),
    ("Bridal car", "Dressed bridal car, timed to the programme.", "wedding", "images/bridal-car.jpg"),
    ("Gold and black function", "Branded tenting and head-table service for a public function.", "corporate", "images/gold-black-tents.jpg"),
    ("Head table in gold", "VIP head table with gold fringe backdrop and fresh florals.", "corporate", "images/head-table-gold.jpg"),
    ("Exhibition booth", "Green, yellow and black draping for a national exhibition stand.", "corporate", "images/exhibition-booth.jpg"),
    ("Teal and gold draping", "Ceiling draping and round tables for a formal reception.", "tents", "images/teal-tent.jpg"),
    ("Red and white reception", "Lined tents, white tiffany chairs and a red carpet.", "tents", "images/red-tent-chairs.jpg"),
    ("Red sash chairs", "Stretch covers with red sashes and sequin table runners.", "tents", "images/red-chairs-sash.jpg"),
    ("Orange and blue wedding", "Floral entrance frame and fabric-lined tents in orange and blue.", "celebration", "images/orange-blue-wedding.jpg"),
    ("Celebration of life", "Green and yellow balloon garlands with a tribute board.", "celebration", "images/green-balloons.jpg"),
    ("Yellow and black table", "Banquet table with yellow sashes, black runner and fresh flowers.", "catering", "images/yellow-tent.jpg"),
    ("Kente table setting", "Woven mats, gold cutlery and kente runner.", "catering", "images/kente-table.jpg"),
    ("Orange banquet setting", "Folded napkins, crystal glassware and matching sashes.", "catering", "images/orange-table.jpg"),
    ("Head-table service", "Drinks station and dressed dining area.", "catering", "images/red-head-table.jpg"),
]

TESTIMONIALS = [
    ("Faith & Kevin", "Garden wedding, Njoro", "Madam Doreen and her team set up the day before and everything was already beautiful by the time we arrived. I actually got to sit down and eat at my own wedding."),
    ("Programme Officer", "NGO field day, Nakuru County", "We needed tents, PA and seating for four hundred people with ten days' notice. Moonshine quoted the same day and the setup was clean and professional."),
    ("The Wanjiru Family", "Celebration of life, Bahati", "They handled my mother's send-off with so much respect. We were grieving and they simply took over the logistics without us having to ask twice."),
]

FAQS = [
    ("How far in advance should I book?", "For weddings and large corporate functions, three to six months gives us the most room to negotiate on your behalf. We regularly deliver good events on two or three weeks' notice, and we mobilise funeral and memorial setups within a day or two."),
    ("Do you travel outside Nakuru?", "Yes. We work regularly in Naivasha, Njoro, Gilgil, Molo, Eldoret, Nyahururu and Nairobi. Anything beyond Nakuru County carries a transport and logistics line on the quote."),
    ("Can I hire only tents and chairs, without planning?", "Absolutely. Equipment hire is available on its own: tents, chairs, tables, linen, carpets, draping and PA."),
    ("How much does an event cost?", "It depends on guest numbers, venue and how much decor you want. Tell us your guest count and budget ceiling and we will show you the best possible event within it, itemised line by line."),
    ("What deposit do you require?", "A booking deposit secures your date and the equipment for it, with the balance settled before setup. The exact split is written into your quotation."),
    ("Do you provide catering yourselves?", "Yes. In-house catering with Kenyan and continental menus, buffet or plated service, waiting staff, crockery and a bar setup. If you already have a caterer you love, we will coordinate with them instead."),
]

# Prices are placeholders: edit them in /admin/ before going live.
PACKAGES = [
    ("Classic Buffet", "Honest, generous Kenyan food for everyday celebrations.", 850, 50,
     "One starter\nTwo mains (one meat, one vegetarian)\nTwo sides and a fresh salad\nSoft drinks and water\nBuffet line, crockery and cutlery\nWaiting staff", False),
    ("Signature Feast", "Our most-booked menu for weddings, dowries and graduations.", 1350, 80,
     "Two starters\nThree mains including nyama choma\nThree sides and two salads\nDessert and fruit platter\nSoft drinks, juices and a mocktail\nBuffet or plated service\nWaiting staff and a stewarded cake table", True),
    ("Grand Occasion", "Plated, multi-course service for the days that need to be perfect.", 2200, 100,
     "Welcome drinks and canapés\nThree-course plated dinner\nLive carving station\nDessert table and cake service\nFull bar setup with bartender\nHead-table service\nCaterer, head waiter and trained stewards", False),
]

MENU = [
    ("starters", "Beef and vegetable samosas", "Crisp pastry, served warm with chilli dip.", False),
    ("starters", "Chicken wings", "Grilled and glazed, passed around at cocktail hour.", False),
    ("starters", "Soup of the day", "Butternut, tomato or chicken broth.", True),
    ("mains", "Nyama choma", "Goat or beef roasted over charcoal, with kachumbari.", False),
    ("mains", "Pilau", "Spiced rice slow-cooked with beef.", False),
    ("mains", "Chicken stew", "Tomato and herb base, served on the bone.", False),
    ("mains", "Beef stew", "Slow-simmered with carrots and potatoes.", False),
    ("mains", "Vegetable curry", "Coconut-based, with chickpeas and seasonal vegetables.", True),
    ("sides", "Chapati", "Soft, layered and freshly cooked.", True),
    ("sides", "Ugali and mukimo", "Maize meal and mashed greens with potato.", True),
    ("sides", "Sukuma wiki", "Sautéed collard greens.", True),
    ("sides", "Kachumbari and garden salad", "Tomato, onion and coriander; mixed leaves.", True),
    ("desserts", "Fruit platter", "Seasonal fruit, cut and arranged.", True),
    ("desserts", "Cake table service", "We cut, plate and serve your cake to guests.", True),
    ("desserts", "Mandazi and pastries", "Light, golden and not too sweet.", True),
    ("drinks", "Soft drinks and bottled water", "Served chilled.", True),
    ("drinks", "Fresh juice and mocktails", "Passion, mango, and a signature mocktail.", True),
    ("drinks", "Tea and coffee station", "Kenyan chai and filter coffee.", True),
]


class Command(BaseCommand):
    help = "Fill the database with starter content for Moonshine Events."

    def handle(self, *args, **opts):
        services = list(SERVICES)
        services.insert(3, CATERING_SERVICE)
        for i, (t, s, f, img, cta) in enumerate(services):
            link = "/catering/" if t.startswith("Catering") else "#contact"
            Service.objects.get_or_create(title=t, defaults=dict(summary=s, features=f, image=img, cta_label=cta, link=link, order=i))
        for i, (t, c, cat, img) in enumerate(GALLERY):
            GalleryItem.objects.get_or_create(title=t, defaults=dict(caption=c, category=cat, image=img, order=i))
        for i, (n, e, q) in enumerate(TESTIMONIALS):
            Testimonial.objects.get_or_create(name=n, defaults=dict(event=e, quote=q, order=i))
        for i, (q, a) in enumerate(FAQS):
            FAQ.objects.get_or_create(question=q, defaults=dict(answer=a, order=i))
        for i, (n, t, p, g, inc, feat) in enumerate(PACKAGES):
            CateringPackage.objects.get_or_create(name=n, defaults=dict(tagline=t, price_per_guest=p, min_guests=g, includes=inc, is_featured=feat, order=i))
        for i, (c, n, d, v) in enumerate(MENU):
            MenuItem.objects.get_or_create(name=n, defaults=dict(category=c, description=d, is_vegetarian=v, order=i))
        self.stdout.write(self.style.SUCCESS("Starter content loaded."))
