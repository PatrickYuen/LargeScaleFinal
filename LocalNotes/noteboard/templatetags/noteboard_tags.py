__author__ = 'elaine'

from ..models import *
from django import template

register = template.Library()

@register.simple_tag
def get_all_cities():
    return City.objects.all()

