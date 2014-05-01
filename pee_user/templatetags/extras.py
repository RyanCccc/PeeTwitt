from django import template

register = template.Library()

@register.filter(name='is_following')
def is_following(pee_user, other):
    return pee_user.is_following(other)

@register.filter(name='equal')
def equal(pee_user, other):
    return pee_user==other