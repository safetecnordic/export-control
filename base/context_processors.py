from django.conf import settings


def metadata(request):
    """
    Add some generally useful metadata to the template context
    """
    return {
        "site_name": settings.SITE_NAME,
        "site_tagline": settings.SITE_TAGLINE,
        "homepage_url": settings.HOMEPAGE,
    }
