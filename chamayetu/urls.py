"""chamayetu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from authentication.views import index, register, login_view, password_reset, logout_user, verify_phone_number
from account.views import home, personal_info_step1, personal_info_step2, personal_info_step3, verify_guarantor, contribution_frequency, account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('auth/register/', register, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/register/verify/', verify_phone_number, name='verify'),
    path('auth/password_reset/', password_reset, name='password_reset'),
    path('auth/logout/', logout_user, name='logout'),
    path('auth/login/account/home/', home, name='home'),
    path('auth/login/account/step1/', personal_info_step1, name='step1'),
    path('auth/login/account/step2/', personal_info_step2, name='step2'),
    path('auth/login/account/step3/', personal_info_step3, name='step3'),
    path('auth/login/account/verify', verify_guarantor, name='verify_guarantor'),
    path('auth/login/account/frequency', contribution_frequency, name='frequency'),
    path('auth/login/account/user/', account, name='account'),
    path('api/v1/', include('daraja.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
