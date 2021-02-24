import random, string
from django.utils.text import slugify

def ramdom_str_gen(size = 4, choices = string.digits):
    return "".join([random(choices) for i in range(size)])

def unique_slug_gen(instance, slug_field, new_slug = None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(slug_field)

    exists = instance.__class__.objects.filter(slug = slug).exists()

    if exists:
        slug = "{0}_{1}".format(slug, ramdom_str_gen())
        slug = unique_slug_gen(instance, slug_field, slug)
    return slug