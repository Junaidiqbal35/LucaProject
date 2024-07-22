from django.urls import path
from .views import index, LoginView

urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', index, name='home'),
]
