from django import template

register = template.Library()

@register.filter
def is_liked_by(achievement, user):
    """Return True if this achievement is liked by the given user."""
    try:
        return achievement.is_liked_by(user)
    except Exception:
        return False
