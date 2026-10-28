# Moonshine Events – Django site

## Run it
```bash
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations core
python manage.py migrate
python manage.py seed_data          # starter services, gallery, menus, FAQs
python manage.py createsuperuser    # your admin login
python manage.py runserver
```
- Site: http://127.0.0.1:8000/   Admin: http://127.0.0.1:8000/admin/
- Customers register at /signup/ and log in at /login/. They see their own enquiries at /dashboard/; staff see all of them.
- Edit phone numbers, email and hours in `BUSINESS` inside `moonshine/settings.py`.
- Edit catering packages, prices and menu items in the admin (seeded prices are placeholders).

## Deploying
Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, `DJANGO_ALLOWED_HOSTS=yourdomain` and run `python manage.py collectstatic`.
Netlify only hosts static files, so use Render, Railway, PythonAnywhere or a VPS for a Django site.
