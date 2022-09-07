import datetime

from django.db.models import F

from app.models import Card
from app.exceptions import IncorrectRememberTypeError
from app.services.categories import get_subcategories_of_category


def get_card_to_learn(category_id):
    """Returns random card to learn by category"""
    return Card.objects.filter(
        last_repeated_date__lte=datetime.date.today() - datetime.timedelta(days=1) * F('before_repeat_days')).filter(
        category__id__in=get_subcategories_of_category(category_id) + [category_id]).order_by('?').first()


def remember_card(card_id, remember_type):
    """Updates card according to user's choice:
    - easy: repeat after days * 2
    - hard: repeat after days / 2
    - very_hard: repeat today"""
    card = Card.objects.get(pk=card_id)
    before_repeat_days = card.before_repeat_days

    if remember_type == 'easy':
        card.before_repeat_days = before_repeat_days * 2 if before_repeat_days > 0 else 1
    elif remember_type == 'hard':
        card.before_repeat_days = int(before_repeat_days / 2)
    elif remember_type == 'very_hard':
        card.before_repeat_days = 0
    else:
        raise IncorrectRememberTypeError()

    card.last_repeated_date = datetime.date.today()
    card.save()
