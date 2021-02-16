from django.urls import path
from .views import *
from rest_framework import routers
from . import views
from django.urls import include, path
from django.urls import path
from .views import home

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', FileUploadView.as_view()),
    
    # path('home/', views.home, name='home'),
]