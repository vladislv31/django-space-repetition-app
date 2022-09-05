import datetime

from django.contrib.auth.models import User

from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):

    name = models.CharField(max_length=30)
    parent = TreeForeignKey("self", default=None, blank=True, null=True,
                            on_delete=models.SET_NULL, related_name="subcategories")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        db_table = "categories"

    def __str__(self):
        return f"{self.name} | {self.user}"


class Card(models.Model):

    question = models.TextField()
    answer = models.TextField()
    started_date = models.DateField(auto_now_add=True)
    last_repeated_date = models.DateField(auto_now_add=True)
    before_repeat_days = models.IntegerField(default=1)
    category = TreeForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name="cards")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")

    class Meta:
        db_table = "cards"

    def __str__(self):
        return f"{self.question} | {self.before_repeat_days}"
