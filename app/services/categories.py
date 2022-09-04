from django.contrib.auth.models import User

from app.models import Category


def get_top_categories_by_user(user: User) -> list[Category]:
    """Returns top categories by user
    TODO:
        - deal something with many requests to db (serializer, etc.)
    """
    return Category.objects.filter(user=user, parent=None).all()
