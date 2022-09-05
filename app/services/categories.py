from app.models import Category


def get_top_categories_by_user(user):
    """Returns top categories by user"""
    return Category.objects.filter(user=user).all()
