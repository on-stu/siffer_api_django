from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, LogoutView, ProductViewSet, RegisterView, SiteViewSet, UserView, UserViewSet, CustomTokenObtainPairView, get_user_token, getSize, site_list
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


router = DefaultRouter()
router.register('user', UserViewSet)
router.register('site', SiteViewSet)
router.register('product', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('getsize/', getSize),

]
