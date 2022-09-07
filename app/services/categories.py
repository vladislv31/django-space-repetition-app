from app.models import Category


def get_top_categories_by_user(user):
    """Returns parent categories by user"""
    return Category.objects.filter(user=user).all()


def get_subcategories_of_category(category_id):
    """Returns subcategories_ids of specific category"""
    categories = Category.objects.select_related('parent').all()
    to_lookup = [category_id]

    subcategories = []

    while to_lookup:
        current_category_id = to_lookup.pop()
        for category in categories:
            if category.parent:
                if category.parent.id == current_category_id:
                    to_lookup.append(category.pk)
                    subcategories.append(category.pk)

    return subcategories
