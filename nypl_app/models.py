from django.db import models


class Item(models.Model):
    """Single item. Stores uuid, genre."""

    uuid = models.CharField("uuid", max_length=50, unique=True)
    name = models.CharField("Name", max_length=256)

    def __str__(self):
        return self.name


class SearchTerm(models.Model):
    """
    Stores search term, date found, and id, so we can check here before we
    decide to search on the same term again.
    """

    text = models.CharField("text", max_length=50)
    date = models.DateTimeField()

    def __str__(self):
        return self.text


class ItemSearchTerm(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    search_term = models.ForeignKey(SearchTerm, on_delete=models.PROTECT)

