from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('user', views.UserViewSet)
router.register('my-images', views.BaseImageViewSet)
router.register('account-plans', views.AccountPlanViewSet)
router.register('expiring-link', views.ExpiringLinkViewSet,
                basename='ExpireLinks')

app_name = 'hexocean_api'
urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view()),
    path('images/<access_str>', views.ImageAPIView.as_view(), name='images'),
    path('logout/', views.Logout.as_view()),
]
