"""
URL configuration for ivaskin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from ivaapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #visual
    path('admin/', admin.site.urls),
    path('', views.ind, name='index'),
    path('<int:description_id>/', views.desc, name='description'),
    path('add_review/', views.add_review, name='add_review'),
    path('appointment/', include('appointment.urls')),
    path('reviews/<int:id>/', views.read_fuul_review, name='reviews'),
    path('faq/', views.faq, name='faq'),
    #auth
    path('signup/', views.signup_user, name='signupuser'),
    path('logout/', views.logout_user, name='logoutuser'),
    path('login/', views.login_user, name='loginuser'),
    path('profile/', include('userprofile.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
