from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (Favorites, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Subscriptions, User

from .filters import IngredientFilter, RecipeFilter
from .pagination import Pagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          RecipeShortSerializer, SubscriptionsSerializer,
                          TagSerializer)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = Pagination
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly | IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    @staticmethod
    def add_to(model, user, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        content = model.objects.filter(user=user, recipe=recipe)
        if content.exists():
            return Response('Этот рецепт уже в добавлен',
                            status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_from(model, user, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        content = model.objects.filter(user=user, recipe=recipe)
        if content.exists():
            content.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('Рецепт уже удален',
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['POST'],
            permission_classes=[IsAuthenticated]
            )
    def favorite(self, request, pk):
        return self.add_to(Favorites, request.user, pk)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_from(Favorites, request.user, pk)

    @action(detail=True,
            methods=['POST'],
            permission_classes=[IsAuthenticated]
            )
    def shopping_cart(self, request, pk):
        return self.add_to(ShoppingCart, request.user, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_from(ShoppingCart, request.user, pk)

    @action(methods=['GET'],
            detail=False,
            permission_classes=[IsAuthenticated]
            )
    def download_shopping_cart(self, request):
        user = request.user
        queryset = RecipeIngredient.objects.filter(
            recipe__shoppingcart__user=user
        )
        queryset_sort = queryset.values('ingredient__name',
                                        'ingredient__measurement_unit',
                                        ).annotate(
            quantity=Sum('amount')).order_by()
        shopping_list = (
            f'Список покупок для: {user.username}\n\n'
        )
        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]}'
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["quantity"]}'
            for ingredient in queryset_sort
        ])
        shopping_list += '\n\nFoodgram'

        filename = f'{user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = Pagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=True,
            methods=['POST'],
            permission_classes=[IsAuthenticated]
            )
    def subscribe(self, request, **kwargs):
        user = request.user
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        serializer = SubscriptionsSerializer(author,
                                             data=request.data,
                                             context={'request': request})
        serializer.is_valid(raise_exception=True)
        Subscriptions.objects.create(user=user, author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, **kwargs):
        user = request.user
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        subscription = get_object_or_404(Subscriptions,
                                         user=user,
                                         author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['GET'],
            permission_classes=[IsAuthenticated]
            )
    def subscriptions(self, request):
        subscribers = User.objects.filter(subscribers__user=request.user)
        pages = self.paginate_queryset(subscribers)
        serializer = SubscriptionsSerializer(
            pages,
            many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)
