import csv

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data/tags.csv', 'r',
                  encoding='utf-8',
                  ) as file:
            data = csv.reader(file)
            for name, color, slug in data:
                Tag.objects.get_or_create(
                    name=name, color=color, slug=slug
                )
