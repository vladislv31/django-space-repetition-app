from django.db import models


class Category(models.Model):

    class Meta:
        db_table = "categories"

    name = models.CharField(max_length=30)
    parent = models.ForeignKey("self", default=None, null=True, on_delete=models.SET_NULL)


class Card(models.Model):

    class Meta:
        db_table = "cards"

    question = models.TextField()
    answer = models.TextField()
    started_date = models.DateField(auto_now_add=True)
    last_repeated_date = models.DateField(auto_now_add=True)
    before_repeat_days = models.IntegerField(default=1)
