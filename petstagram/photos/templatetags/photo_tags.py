from django import template

register = template.Library()


@register.simple_tag
def has_liked(photo, user):
    if user.is_authenticated:
        return photo.like_set.filter(user=user).first()

    return False
