# Security configuration notes

- DEBUG must be False in production.
- SECRET_KEY must be set in env var DJANGO_SECRET_KEY.
- CSP configured via django-csp in settings.py.
- CSRF and SESSION cookies set to secure and httponly in production.
- All forms must use {% csrf_token %} and Django Form validation.
- Use ORM filters — never raw SQL without parameterization.
