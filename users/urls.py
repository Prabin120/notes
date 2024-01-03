from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import SignUpView

urlpatterns = [
    path('signup', SignUpView.as_view(), name='auth-signup'),
    path('login', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('login/refresh', jwt_views.TokenRefreshView.as_view(), name='login_refresh'),
]   
