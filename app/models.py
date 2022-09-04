import datetime

from django.contrib.auth.models import User

from django.db.models import F
from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=30)
    parent = models.ForeignKey("self", default=None, blank=True, null=True,
                               on_delete=models.SET_NULL, related_name="subcategories")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")

    class Meta:
        db_table = "categories"

    def __str__(self):
        return f"{self.name} | {self.user}"

    def get_cards_full_count(self):
        """TODO:
        - deal something with many requests to db (serializer, etc.)
        """
        cards_count = self._get_cards_count()
        subcategories = self.subcategories.all()

        for subcategory in subcategories:
            cards_count += subcategory.get_cards_full_count()

        return cards_count

    def get_to_repeat_cards_full_count(self):
        """TODO:
        - deal something with many requests to db (serializer, etc.)
        """
        cards_count = self._get_cards_count(to_repeat=True)
        subcategories = self.subcategories.all()

        for subcategory in subcategories:
            cards_count += subcategory.get_cards_full_count()

        return cards_count

    def _get_cards_count(self, to_repeat=False):
        if to_repeat:
            return self.cards.filter(last_repeated_date__lte=datetime.date.today() - datetime.timedelta(days=1) * F(
                "before_repeat_days")).count()
        else:
            return self.cards.count()


class Card(models.Model):

    question = models.TextField()
    answer = models.TextField()
    started_date = models.DateField(auto_now_add=True)
    last_repeated_date = models.DateField(auto_now_add=True)
    before_repeat_days = models.IntegerField(default=1)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name="cards")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")

    class Meta:
        db_table = "cards"

    def __str__(self):
        return f"{self.question} | {self.before_repeat_days}"
