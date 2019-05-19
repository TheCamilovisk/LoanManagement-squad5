from django.contrib import admin
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('loans/', views.loans),
    path('loans/<int:pk>/payments/', views.payments, name='payments'),
    path('loans/<int:pk>/balance/', views.balance),
    path('clients/', views.clients),
    path('admin/', admin.site.urls),
    path('', include('core.urls'), name='index'),
    path('api/token/', obtain_jwt_token),
]