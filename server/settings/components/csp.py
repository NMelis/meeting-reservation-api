"""
This file contains a definition for Content-Security-Policy headers.

Read more about it:
https://developer.mozilla.org/ru/docs/Web/HTTP/Headers/Content-Security-Policy

We are using `django-csp` to provide these headers.
Docs: https://github.com/mozilla/django-csp
"""

# These values might and will be redefined in `development.py` env:
CSP_SCRIPT_SRC: tuple[str, ...] = (
    "'self'",
    "'unsafe-eval'",
    "'unsafe-inline'",
    "http://ajax.googleapis.com",
    "https://meeting.nmelis.com",
    "https://cdnjs.cloudflare.com"
)
CSP_IMG_SRC: tuple[str, ...] = ("'self'", "data:", "https://example.com")
CSP_FONT_SRC: tuple[str, ...] = ("'self'", "https://fonts.gstatic.com")
CSP_STYLE_SRC: tuple[str, ...] = (
    "'self'",
    "'unsafe-inline'",
    "https://fonts.googleapis.com",
    "https://cdnjs.cloudflare.com",
    "https://meeting.nmelis.com",
)
CSP_DEFAULT_SRC: tuple[str, ...] = ("'none'",)
CSP_CONNECT_SRC: tuple[str, ...] = ("'self'", "https://api.example.com")
