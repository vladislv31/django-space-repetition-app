from django.db.models import Count

from app.models import Category


def get_categories_by_user(user, parent_category_id=None):
    """Returns categories by user"""
    query_set = Category.objects.filter(user=user)

    if parent_category_id:
        subcategories_ids = get_subcategories_of_category(parent_category_id)
        query_set = query_set.filter(id__in=subcategories_ids + [parent_category_id])

    return query_set.select_related('parent').annotate(cards_count=Count('cards__id'))


def get_subcategories_of_category(category_id):
    """Returns subcategories_ids of specific category"""
    categories = Category.objects.select_related('parent').all()

    categories_dict = {}
    for category in categories:
        if category.parent:
            if category.parent.id in categories_dict.keys():
                categories_dict[category.parent.id].append(category.pk)
            else:
                categories_dict[category.parent.id] = [category.pk]

    to_lookup = [category_id]
    subcategories = []

    while to_lookup:
        current_category_id = to_lookup.pop()
        if current_category_id in categories_dict.keys():
            to_lookup.extend(categories_dict[current_category_id])
            subcategories.extend(categories_dict[current_category_id])

    return subcategories
