from django.db.models import Avg
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework import viewsets, status, filters
from rest_framework.pagination import (
    PageNumberPagination, LimitOffsetPagination)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Review, Title, Genre, Category
from users.models import User
from .filters import TitleFilter
from .permissions import (
    AdminOnly, AdminOrAuthorOnly,
    AdminOrReadOnly, IsAuthorOrReadOnlyPermission)
from .serializers import (
    SignUpSerializer, UsersSerializer, UsersMeSerializer,
    GetTokenSerializer, CategorySerializer, GenreSerializer,
    TitleReadSerializer, TitlePostSerializer, ReviewSerializer,
    CommentSerializer)
from api_yamdb.settings import FROM_EMAIL
from .mixins import CustomViewSet
from django.utils.crypto import get_random_string
from rest_framework.decorators import action


class SignupApiView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        def confirmation_code_generate():
            return get_random_string(length=6, allowed_chars='1234567890')

        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save(
                confirmation_code=confirmation_code_generate())
        except IntegrityError:
            return Response('Такой логин или email уже существуют',
                            status=status.HTTP_400_BAD_REQUEST)

        send_mail(
            subject='Код подтверждения для yamdb',
            message=f'Ваш код подтверждения - {user.confirmation_code}',
            from_email=FROM_EMAIL,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenApiView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response({'username': 'Пользователь не найден!'},
                            status=status.HTTP_404_NOT_FOUND)

        if data.get('confirmation_code') == user.confirmation_code:
            token = AccessToken.for_user(user)
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)

        return Response({'confirmation_code': 'Неверный код подтверждения!'},
                        status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOnly,)
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    filter_fields = ('username',)
    search_fields = ['username']

    @action(
        detail=False, methods=['get', 'patch'],
        permission_classes=(AdminOrAuthorOnly,), url_path='me')
    def me_get_patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UsersSerializer(user)

        if request.method == 'PATCH':
            serializer = UsersMeSerializer(
                user, data=request.data, partial=True,
                context={'role': request.user.role})

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (AdminOrReadOnly,)
    filter_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,
                          permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
        )
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        new_queryset = review.comments.all()
        return new_queryset
