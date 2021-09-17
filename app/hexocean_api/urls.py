from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import user_related_views, object_related_views

router = DefaultRouter()
router.register('user', user_related_views.UserViewSet)
router.register('my-images', object_related_views.BaseImageViewSet)
router.register('account-plans', object_related_views.AccountPlanViewSet)
router.register('expiring-link', object_related_views.ExpiringLinkViewSet,
                basename='ExpireLinks')
router.register('my-thumbnails', object_related_views.MyThumbnails)

app_name = 'hexocean_api'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', user_related_views.UserLoginApiView.as_view()),
    path('images/<access_str>', object_related_views.ImageAPIView.as_view(),
         name='images'),
    path('logout/', user_related_views.Logout.as_view()),
]
