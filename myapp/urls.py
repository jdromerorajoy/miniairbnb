from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('reservations/', views.reservations, name='reservations'),
    path('detail/', views.detail, name='detail'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('thanks/', views.thanks, name='thanks'),
    path('thanks/<int:id>/', views.thanks, name='thanks'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

