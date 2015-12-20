__author__ = 'elaine'

from ..models import *
from django import template
from django.core.cache import cache

register = template.Library()

@register.simple_tag
def get_all_cities():
    all_cities = cache.get("cities", "expired")
    if all_cities == "expired":
        all_cities = City.objects.all()
        cache.set("cities", all_cities, 60*60)

    return all_cities

