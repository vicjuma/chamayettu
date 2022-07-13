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
import imp
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required, permission_required
from authentication.views import forgetPass, index, register, login_view, logout_user, new_password, activate, forgetPass, CompletePasswordReset
from account.views import handle_404, home, contribution_frequency, account, savings_contribute, reset_password
from step1.views import personal_info_step1
from step2.views import personal_info_step2
from step3.views import personal_info_step3
from backoffice.views import DuesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('dues/', login_required(DuesView.as_view())),
    path('auth/register/', register, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/password_reset/', forgetPass, name='password_reset'),
    path('auth/password_new/<uidb64>/<token>', CompletePasswordReset, name='new_password'),
    path('auth/reset/', reset_password, name='reset'),
    path('auth/logout/', logout_user, name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('auth/login/account/home/', home, name='home'),
    path('auth/login/account/step1/', personal_info_step1, name='step1'),
    path('auth/login/account/step2/', personal_info_step2, name='step2'),
    path('auth/login/account/step3/', personal_info_step3, name='step3'),
    path('auth/login/account/frequency', contribution_frequency, name='frequency'),
    path('auth/login/account/user/', account, name='account'),
    path('auth/login/account/savings/contibute/', savings_contribute, name="savings_contribute"),
    path('api/v1/', include('daraja.urls')),
    path('verification/', include('verify_email.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handle_404 = 'account.views.handle_404'
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

