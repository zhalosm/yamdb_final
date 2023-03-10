from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    SignupApiView, GetTokenApiView, UsersViewSet, CategoryViewSet,
    GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet,)

router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignupApiView.as_view()),
    path('v1/auth/token/', GetTokenApiView.as_view()),
]
