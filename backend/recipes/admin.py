from django.contrib import admin

from .models import (Favorites, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite_list')
    list_filter = ('author', 'name', 'tags__name',)

    def favorite_list(self, obj):
        return obj.favorites.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Favorites)
admin.site.register(ShoppingCart)
