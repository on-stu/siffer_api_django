from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SiteViewSet, UserViewSet, CustomTokenObtainPairView, getSize, site_list
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


router = DefaultRouter()
router.register('user', UserViewSet)
router.register('site', SiteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('getsize/', getSize),
    path('sitelist/', site_list)
]
