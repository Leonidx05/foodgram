import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data/ingredients.csv', 'r',
                  encoding='utf-8',
                  ) as file:
            data = csv.reader(file)
            for name, measurement_unit in data:
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=measurement_unit
                )
